import os
from openai import OpenAI
from env import TrafficEnv

def get_client():
    """
    Initializes the client ONLY when needed. 
    This prevents the 'api_key not set' error at startup.
    """
    api_key = os.environ.get("API_KEY")
    base_url = os.environ.get("API_BASE_URL")
    
    # If variables aren't there yet, use a dummy key so it doesn't crash
    if not api_key:
        return OpenAI(api_key="temporary_key_for_startup")
        
    return OpenAI(base_url=base_url, api_key=api_key)

def smart_policy(state):
    # Initialize client inside the function
    client = get_client()
    model_name = os.environ.get("LLM_MODEL", "gpt-4o")
    
    prompt = f"Traffic State: {state}. Decide 0 or 1."

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5
        )
        content = response.choices[0].message.content.strip()
        return int(''.join(filter(str.isdigit, content))[0])
    except Exception as e:
        # Standard fallback if LLM or API is unavailable
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

        final_queue = sum(env.state["cars"])
        score = max(0, 1 - (final_queue / 100))
        results[task] = {
            "final_queue": final_queue,
            "score": round(score, 3)
        }
    return results
