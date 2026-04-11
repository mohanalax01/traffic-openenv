from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Adds root to path so it can find env.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import TrafficEnv
from baseline import run_baseline
from grader import grade

app = FastAPI(title="Traffic OpenEnv API")
env = TrafficEnv()

class ResetRequest(BaseModel):
    task: Optional[str] = "easy"
    seed: Optional[int] = None

class StepRequest(BaseModel):
    action: int

@app.get("/")
def home():
    return {"message": "Traffic OpenEnv API is online"}

@app.post("/reset")
def reset(data: ResetRequest):
    observation = env.reset(task=data.task, seed=data.seed)
    return {"observation": observation}

@app.post("/step")
def step(data: StepRequest):
    obs, reward, done, info = env.step(data.action)
    return {
        "observation": obs, 
        "reward": reward, 
        "done": done, 
        "info": info
    }

@app.get("/baseline")
def baseline_endpoint():
    return run_baseline()

@app.get("/grader")
def grader_endpoint():
    return {"score": grade(env)}
