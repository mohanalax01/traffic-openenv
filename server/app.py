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

# Changed to allow testing via browser if needed, 
# though POST is better for production.
@app.get("/step/{action_id}")
def step_get(action_id: int):
    state, reward, done, _ = env.step(action_id)
    return {"state": state, "reward": reward, "done": done}

@app.post("/step")
def step_post(action: Action):
    state, reward, done, _ = env.step(action.action)
    return {"state": state, "reward": reward, "done": done}

@app.get("/reset")
def reset(task: str = "easy", seed: int = None):
    # Added basic error handling to prevent crash if env fails
    try:
        return env.reset(task, seed)
    except Exception as e:
        return {"error": str(e)}

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
def grader():
    return {"score": grade(env)}

@app.get("/baseline")
def baseline():
    return run_baseline()
