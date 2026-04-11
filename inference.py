import os
import requests
import sys

# Use the environment variable or your specific Space URL
ENV_URL = os.getenv("ENV_BASE_URL", "http://localhost:7860")

def run_traffic_agent():
    task_name = "easy"
    total_reward = 0
    total_steps = 0
    
    try:
        # 1. Start/Reset
        reset_response = requests.post(f"{ENV_URL}/reset", json={"task": task_name})
        reset_response.raise_for_status()
        
        # REQUIRED OUTPUT: [START]
        print(f"[START] task={task_name}", flush=True)
        
        # 2. Run steps
        for i in range(1, 6):  # Run 5 steps for the validator
            action = i % 2 
            
            step_response = requests.post(f"{ENV_URL}/step", json={"action": action})
            step_response.raise_for_status()
            data = step_response.json()
            
            reward = data.get("reward", 0.0)
            total_reward += reward
            total_steps += 1
            
            # REQUIRED OUTPUT: [STEP]
            print(f"[STEP] step={i} reward={reward}", flush=True)
            
            if data.get("done"):
                break
        
        # 3. End
        # REQUIRED OUTPUT: [END]
        # Adjust the score logic based on your environment's grading
        score = total_reward / total_steps if total_steps > 0 else 0
        print(f"[END] task={task_name} score={score:.2f} steps={total_steps}", flush=True)

    except Exception as e:
        # If it fails, we still need to make sure we don't just hang
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    run_traffic_agent()
