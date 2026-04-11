import os
import requests
from openai import OpenAI

# 1. Environment Variables (Required by your checklist)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1/")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")  # No default value for token

# The URL of your running environment (the Space you created)
ENV_URL = os.getenv("ENV_BASE_URL", "https://mohanalaxmi-traffic-openenv.hf.space")
import os
import requests
from openai import OpenAI

# 1. Environment Variables (Required by your checklist)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1/")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")  # No default value for token

# The URL of your running environment (the Space you created)
ENV_URL = os.getenv("ENV_BASE_URL", "https://mohanalaxmi-traffic-openenv.hf.space")

# 2. Initialize OpenAI Client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_traffic_agent():
    # --- REQUIRED LOGGING START ---
    print("START")

    # Step 1: Reset the environment (Using POST as required)
    try:
        reset_response = requests.post(f"{ENV_URL}/reset", json={"task": "easy"})
        reset_response.raise_for_status()
        obs = reset_response.json().get("observation")
        
        # Step 2: Run the simulation loop
        for i in range(5):  # Run for 5 steps as a test
            print("STEP")
            
            # Simple Logic: Alternate between action 0 and 1
            action_to_take = i % 2 
            
            # Send the action to your /step endpoint
            step_response = requests.post(
                f"{ENV_URL}/step", 
                json={"action": action_to_take}
            )
            step_response.raise_for_status()
            data = step_response.json()
            
            # Log progress (optional, for your debugging)
            # print(f"Step {i}: Reward: {data.get('reward')}")

            if data.get("done"):
                break

    except Exception as e:
        print(f"Error during inference: {e}")

    # --- REQUIRED LOGGING END ---
    print("END")

if __name__ == "__main__":
    run_traffic_agent()
# 2. Initialize OpenAI Client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_traffic_agent():
    # --- REQUIRED LOGGING START ---
    print("START")

    # Step 1: Reset the environment (Using POST as required)
    try:
        reset_response = requests.post(f"{ENV_URL}/reset", json={"task": "easy"})
        reset_response.raise_for_status()
        obs = reset_response.json().get("observation")
        
        # Step 2: Run the simulation loop
        for i in range(5):  # Run for 5 steps as a test
            print("STEP")
            
            # Simple Logic: Alternate between action 0 and 1
            action_to_take = i % 2 
            
            # Send the action to your /step endpoint
            step_response = requests.post(
                f"{ENV_URL}/step", 
                json={"action": action_to_take}
            )
            step_response.raise_for_status()
            data = step_response.json()
            
            # Log progress (optional, for your debugging)
            # print(f"Step {i}: Reward: {data.get('reward')}")

            if data.get("done"):
                break

    except Exception as e:
        print(f"Error during inference: {e}")

    # --- REQUIRED LOGGING END ---
    print("END")

if __name__ == "__main__":
    run_traffic_agent()
