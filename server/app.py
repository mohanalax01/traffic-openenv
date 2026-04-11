from fastapi import FastAPI
from pydantic import BaseModel
from env import TrafficEnv
from baseline import run_baseline

app = FastAPI(title="Traffic OpenEnv API")
env = TrafficEnv()

# These models prevent the "missing field" error by clearly defining the body 
class ActionRequest(BaseModel):
    action: int

class ResetRequest(BaseModel):
    task: str = "easy"
    seed: int = None

@app.get("/")
def home():
    return {"message": "Traffic OpenEnv API running"}

@app.post("/reset")
def reset(data: ResetRequest):
    # Extracts 'task' and 'seed' from the JSON body 
    observation = env.reset(task=data.task, seed=data.seed)
    return {"observation": observation}

@app.post("/step")
def step(data: ActionRequest):
    # Extracts 'action' from the JSON body 
    state, reward, done, _ = env.step(data.action)
    return {"state": state, "reward": reward, "done": done}

@app.get("/baseline")
def baseline():
    return run_baseline()
