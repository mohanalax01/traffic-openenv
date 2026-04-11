import os
import re
from openai import OpenAI
from env import TrafficEnv

# Global variable to store the client once it's created
_client = None

def get_client():
    """
    Initializes the client ONLY when the key is available.
    Prevents the 'api_key not set' crash during startup.
    """
    global _client
    if _client is None:
        api_key = os.environ.get("API_KEY")
        base_url = os.environ.get("API_BASE_URL")
        
        # If the key isn't ready yet, return a temporary dummy client
        if not api_key:
            return OpenAI(api_key="waiting_for_eval_key")
        
        # This points the traffic through the required LiteLLM proxy
        _client = OpenAI(
            base_url=base_url, 
            api_key=api_key
        )
    return _client

def smart_policy(state):
    client = get_client()
    
    # If we are still in the startup phase without a key, use math fallback
    if client.api_key == "waiting_for_eval_key":
        return 0 if (state["cars"][0] + state["cars"][2]) > (state["cars"][1] + state["cars"][3]) else 1

    model_name = os.environ.get("LLM_MODEL", "gpt-4o")
    
    prompt = (
        f"North-South lane cars: {state['cars'][0] + state['cars'][2]}. "
        f"East-West lane cars: {state['cars'][1] + state['cars'][3]}. "
        f"Goal: Minimize traffic. Reply with '0' for NS green or '1' for EW green. Digit only."
    )

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2
        )
        content = response.choices[0].message.content.strip()
        # Find the first digit in the response to be safe
        match = re.search(r'\d', content)
        return int(match.group()) if match else 0
    except Exception as e:
        print(f"LLM Error: {e}")
        # Mathematical fallback so the evaluation continues
        if state["cars"][0] + state["cars"][2] > state["cars"][1] + state["cars"][3]:
            return 0
        return 1

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
        results[task] = {
            "final_queue": final_queue,
            "score": round(score, 3)
        }
    return results
