from fastapi import FastAPI
from pydantic import BaseModel
from env import TrafficEnv
from grader import grade
from baseline import run_baseline

app = FastAPI()
env = TrafficEnv()

class Action(BaseModel):
    action: int

@app.get("/")
def home():
    return {"message": "Traffic OpenEnv API running"}

@app.get("/reset")
def reset(task: str = "easy", seed: int = None):
    return env.reset(task, seed)

@app.post("/step")
def step(action: Action):
    state, reward, done, _ = env.step(action.action)
    return {"state": state, "reward": reward, "done": done}

@app.get("/tasks")
def tasks():
    return {
        "tasks": ["easy", "medium", "hard"],
        "action_space": {
            "0": "North-South green (lanes 0 & 2 move)",
            "1": "East-West green (lanes 1 & 3 move)"
        }
    }

@app.get("/grader")
def grader():
    return {"score": grade(env)}

@app.get("/baseline")
def baseline():
    return run_baseline()