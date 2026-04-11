def grade(env):
    total_wait = sum(env.state["cars"])
    emergency_cleared = env.state["emergency"] == 0

    score = max(0, 1 - (total_wait / 100))

    if emergency_cleared:
        score += 0.2

    return min(round(score, 3), 1.0)