from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Ensure the root directory is in the path so we can find env.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import TrafficEnv
from baseline import run_baseline

app = FastAPI()
env = TrafficEnv()

class Action(BaseModel):
    action: int

class ResetConfig(BaseModel):
    task: str = "easy"
    seed: int = None

@app.get("/")
def home():
    return {"status": "Traffic API Online"}

@app.post("/reset")
def reset(config: ResetConfig):
    # This matches the POST request in your inference.py
    obs = env.reset(task=config.task, seed=config.seed)
    return {"observation": obs}

@app.post("/step")
def step(action: Action):
    state, reward, done, _ = env.step(action.action)
    return {"state": state, "reward": reward, "done": done}

@app.get("/baseline")
def baseline():
    return run_baseline()
