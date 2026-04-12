import os
import re
import time
from openai import OpenAI
from env import TrafficEnv

# We keep the client empty until the first request
_client = None

def get_active_client():
    """
    Ensures we only create the client once the validator 
    has injected the API credentials.
    """
    global _client
    if _client is None:
        api_key = os.environ.get("API_KEY")
        base_url = os.environ.get("API_BASE_URL")
        
        # If the validator is still setting up, we return None to trigger a wait
        if not api_key or not base_url:
            return None
            
        _client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
    return _client

def smart_policy(state):
    # Attempt to get the client
    client = get_active_client()
    
    # If the client isn't ready (no API_KEY yet), wait briefly
    if client is None:
        time.sleep(0.5)
        client = get_active_client()
        if client is None:
            # Absolute fallback if API is still unavailable
            return 0 if (state["cars"][0] + state["cars"][2]) > (state["cars"][1] + state["cars"][3]) else 1

    model_name = os.environ.get("LLM_MODEL", "gpt-4o")
    
    prompt = (
        f"North-South cars: {state['cars'][0] + state['cars'][2]}. "
        f"East-West cars: {state['cars'][1] + state['cars'][3]}. "
        "Choose '0' (NS Green) or '1' (EW Green). Reply with just the digit."
    )

    try:
        # This specific call registers on the LiteLLM proxy
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2,
            timeout=10.0 # Prevent hanging if the proxy is slow
        )
        content = response.choices[0].message.content.strip()
        match = re.search(r'\d', content)
        return int(match.group()) if match else 0
    except Exception as e:
        print(f"Proxy API Error: {e}")
        # Mathematical fallback
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
