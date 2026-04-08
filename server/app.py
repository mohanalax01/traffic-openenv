from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from env import TrafficEnv
from grader import grade
from baseline import run_baseline

app = FastAPI()
env = TrafficEnv()

# Pydantic model for the Action
class Action(BaseModel):
    action: int

@app.get("/")
def home():
    return {"message": "Traffic OpenEnv API is live and healthy"}

# CHANGED: Now using @app.post as required by the OpenEnv spec
@app.post("/reset")
def reset(task: str = "easy", seed: Optional[int] = None):
    # Returns the initial observation
    observation = env.reset(task=task, seed=seed)
    return {"observation": observation}

# CHANGED: Return key changed from "state" to "observation"
@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action.action)
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
            "0": "North-South green (lanes 0 & 2 move)",
            "1": "East-West green (lanes 1 & 3 move)"
        }
    }

@app.get("/grader")
def grader():
    # Helper endpoint for manual score checking
    return {"score": grade(env)}

@app.get("/baseline")
def baseline():
    # Helper endpoint to run the baseline agent
    return run_baseline()

# ... your existing FastAPI code ...

def main():
    import uvicorn
    # This matches the "main" function the validator is looking for
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
