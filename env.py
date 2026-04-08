import random

TASKS = {
    "easy": {"max_steps": 20, "traffic_level": "low"},
    "medium": {"max_steps": 30, "traffic_level": "medium"},
    "hard": {"max_steps": 40, "traffic_level": "high", "emergency_chance": 0.5}
}

class TrafficEnv:
    def __init__(self):
        self.prev_signal = 0
        self.time_since_last_change = 0
        self.reset()

    def reset(self, task="easy", seed=None):
        if seed is not None:
            random.seed(seed)  # ✅ reproducibility

        self.task = task
        config = TASKS[task]

        # traffic initialization
        if config["traffic_level"] == "low":
            cars = [random.randint(0, 5) for _ in range(4)]
        elif config["traffic_level"] == "medium":
            cars = [random.randint(5, 15) for _ in range(4)]
        else:
            cars = [random.randint(15, 30) for _ in range(4)]

        self.state = {
            "cars": cars,
            "signal": 0,
            "emergency": 1 if random.random() < config.get("emergency_chance", 0) else 0
        }

        self.steps = 0
        self.time_since_last_change = 0

        return self._get_obs()

    def _get_obs(self):
        return {
            "cars": self.state["cars"],
            "signal": self.state["signal"],
            "emergency": self.state["emergency"],
            "queue_length": sum(self.state["cars"]),
            "time_since_last_change": self.time_since_last_change
        }

    def step(self, action):
        reward = 0

        # movement logic
        for i in range(4):
            if (action == 0 and i in [0, 2]) or (action == 1 and i in [1, 3]):
                self.state["cars"][i] = max(0, self.state["cars"][i] - random.randint(3, 7))
            else:
                self.state["cars"][i] += random.randint(0, 3)

        # emergency handling
        if self.state["emergency"] == 1:
            if action == 0:
                reward += 20
                self.state["emergency"] = 0
            else:
                reward -= 20

        # imbalance penalty
        imbalance = max(self.state["cars"]) - min(self.state["cars"])
        reward -= imbalance * 0.5

        # switching penalty
        if action != self.prev_signal:
            reward -= 2
            self.time_since_last_change = 0
        else:
            self.time_since_last_change += 1

        self.prev_signal = action
        self.state["signal"] = action

        # congestion spike (hard realism)
        if random.random() < 0.3:
            lane = random.randint(0, 3)
            self.state["cars"][lane] += 15

        # waiting penalty
        reward -= sum(self.state["cars"]) * 0.1

        self.steps += 1
        done = self.steps >= TASKS[self.task]["max_steps"]  # ✅ termination

        return self._get_obs(), reward, done, {}