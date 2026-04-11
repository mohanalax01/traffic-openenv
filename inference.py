import os
import requests

# Use your Hugging Face Space URL
ENV_URL = os.getenv("ENV_BASE_URL", "https://mohanalaxmi-traffic-openenv.hf.space")

def run_traffic_agent():
    print("START")
    try:
        # Sending 'task' and 'seed' as JSON to match ResetRequest 
        reset_response = requests.post(
            f"{ENV_URL}/reset", 
            json={"task": "easy", "seed": 42}
        )
        reset_response.raise_for_status()
        obs = reset_response.json().get("observation")
        print(f"Initial Observation: {obs}")

        # Run 5 test steps
        for i in range(5):
            print("STEP")
            action_to_take = i % 2 
            
            # Sending 'action' as JSON to match ActionRequest 
            step_response = requests.post(
                f"{ENV_URL}/step", 
                json={"action": action_to_take}
            )
            step_response.raise_for_status()
            data = step_response.json()
            
            if data.get("done"):
                break

    except Exception as e:
        print(f"Error: {e}")

    print("END")

if __name__ == "__main__":
    run_traffic_agent()
