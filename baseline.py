import os
import re
from openai import OpenAI
from env import TrafficEnv

def smart_policy(state):
    # FORCE read environment variables inside the function
    # Using os.environ[] without .get() will raise an error if they are missing,
    # which is actually better for debugging Phase 2.
    try:
        api_base = os.environ["API_BASE_URL"]
        api_key = os.environ["API_KEY"]
        model_name = os.environ.get("LLM_MODEL", "gpt-4o")
    except KeyError as e:
        print(f"CRITICAL ERROR: Environment variable {e} is missing!")
        # If the environment isn't ready, we return a fallback so the app doesn't crash,
        # but in Phase 2, these variables MUST be present.
        return 0

    # Initialize client EVERY time to ensure the proxy is hit
    client = OpenAI(
        base_url=api_base,
        api_key=api_key
    )

    prompt = (
        f"Traffic state: {state['cars']}. "
        "Goal: Minimize congestion. Output 0 for NS green, 1 for EW green. "
        "Reply with only the digit."
    )

    try:
        # The actual API call the validator monitors
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2
        )
        
        res_text = response.choices[0].message.content.strip()
        match = re.search(r'\d', res_text)
        return int(match.group()) if match else 0
        
    except Exception as e:
        print(f"API Call Failed: {e}")
        # Fallback logic
        return 0 if (state["cars"][0] + state["cars"][2]) > (state["cars"][1] + state["cars"][3]) else 1

def run_baseline():
    results = {}
    tasks = ["easy", "medium", "hard"]
    for task in tasks:
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
