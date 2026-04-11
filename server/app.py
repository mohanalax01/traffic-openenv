from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from env import TrafficEnv
from baseline import run_baseline
from grader import grade

app = FastAPI(title="Traffic OpenEnv API")
env = TrafficEnv()

# These models define the "Fields" required in the POST body
# Adding Optional and default values prevents the "Field required" error
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
    # This matches the POST request in inference.py
    observation = env.reset(task=data.task, seed=data.seed)
    return {"observation": observation}

@app.post("/step")
def step(data: StepRequest):
    # This matches the POST request in inference.py
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
        "action_space": {"0": "North-South green", "1": "East-West green"}
    }

@app.get("/grader")
def grader_endpoint():
    return {"score": grade(env)}

@app.get("/baseline")
def baseline_endpoint():
    return run_baseline()
