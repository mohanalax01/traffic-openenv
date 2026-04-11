from env import TrafficEnv

def smart_policy(state):
    # prioritize heavier direction
    if state["cars"][0] + state["cars"][2] > state["cars"][1] + state["cars"][3]:
        return 0
    return 1

def run_baseline():
    results = {}

    for task in ["easy", "medium", "hard"]:
        env = TrafficEnv()
        state = env.reset(task, seed=42)  # ✅ fixed seed

        done = False

        while not done:
            action = smart_policy(state)
            state, reward, done, _ = env.step(action)

        final_queue = sum(env.state["cars"])
        score = max(0, 1 - (final_queue / 100))

        results[task] = {
            "final_queue": final_queue,
            "score": round(score, 3)
        }

    return results