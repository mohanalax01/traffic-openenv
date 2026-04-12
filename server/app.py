import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sys
import os
import importlib

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import TrafficEnv
import baseline  # Import as module for reloading
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
def reset(data: ResetRequest = None):
    if data is None:
        data = ResetRequest()
    observation = env.reset(task=data.task, seed=data.seed)
    return {"observation": observation}

@app.post("/step")
def step(data: StepRequest):
    obs, reward, done, info = env.step(data.action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}

@app.get("/baseline")
def baseline_endpoint():
    # CRITICAL: Reloads baseline to catch the API_KEY injected by the validator
    importlib.reload(baseline)
    return baseline.run_baseline()

@app.get("/grader")
def grader_endpoint():
    return {"score": grade(env)}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
