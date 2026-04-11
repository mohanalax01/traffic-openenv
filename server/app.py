from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from env import TrafficEnv
from baseline import run_baseline
from grader import grade

app = FastAPI(title="Traffic OpenEnv API")
env = TrafficEnv()

# These models define the expected JSON structure for POST requests
# They prevent the "Field required" error by providing structure and defaults
class ResetRequest(BaseModel):
    task: Optional[str] = "easy"
    seed: Optional[int] = None

class StepRequest(BaseModel):
    action: int

@app.get("/")
def home():
    return {"message": "Traffic OpenEnv API running"}

@app.post("/reset")
def reset(data: ResetRequest):
    """
    Handles environment reset. 
    Matches the POST request from inference.py: requests.post(url, json={"task": "easy"})
    """
    observation = env.reset(task=data.task, seed=data.seed)
    return {"observation": observation}

@app.post("/step")
def step(data: StepRequest):
    """
    Handles environment steps.
    Matches the POST request from inference.py: requests.post(url, json={"action": 0})
    """
    obs, reward, done, info = env.step(data.action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/tasks")
def tasks():
    return {
        "tasks": ["easy", "medium", "hard"],
        "action_space": {
            "0": "North-South green",
            "1": "East-West green"
        }
    }

@app.get("/grader")
def grader_endpoint():
    # Returns the score based on the current environment state
    return {"score": grade(env)}

@app.get("/baseline")
def baseline_endpoint():
    # Runs the baseline policy and returns results
    return run_baseline()
