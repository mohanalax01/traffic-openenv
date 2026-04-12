import os
import re
from openai import OpenAI
from env import TrafficEnv

def smart_policy(state):
    """
    Makes a decision using the LLM via the required proxy.
    """
    # 1. Capture injected variables
    api_key = os.environ.get("API_KEY")
    api_base = os.environ.get("API_BASE_URL")
    model_name = os.environ.get("LLM_MODEL", "gpt-4o")

    # 2. Fallback only if the validator hasn't provided keys yet
    if not api_key or not api_base:
        return 0 if (state["cars"][0] + state["cars"][2]) > (state["cars"][1] + state["cars"][3]) else 1

    # 3. Initialize client locally to ensure proxy settings are fresh
    client = OpenAI(base_url=api_base, api_key=api_key)

    prompt = (
        f"Traffic counts: NS={state['cars'][0]+state['cars'][2]}, EW={state['cars'][1]+state['cars'][3]}. "
        "Reply with '0' for NS Green or '1' for EW Green. Digit only."
    )

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2,
            temperature=0
        )
        content = response.choices[0].message.content.strip()
        match = re.search(r'\d', content)
        return int(match.group()) if match else 0
    except Exception as e:
        print(f"Proxy Error: {e}")
        return 0 if (state["cars"][0] + state["cars"][2]) > (state["cars"][1] + state["cars"][3]) else 1

def run_baseline():
    results = {}
    for task in ["easy", "medium", "hard"]:
        env = TrafficEnv()
        state = env.reset(task, seed=42)
        done = False
        while not done:
            action = smart_policy(state)
            state, reward, done, _ = env.step(action)
        
        final_queue = sum(env.state.get("cars", [0,0,0,0]))
        score = max(0, 1 - (final_queue / 100))
        results[task] = {"score": round(score, 3)}
    return results
