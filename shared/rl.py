"""shared.rl — a minimal casualty-evacuation GridWorld built from datasets.load_evac()."""
from __future__ import annotations

import numpy as np

ACTIONS = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}  # up, down, left, right


class EvacGrid:
    """Point of injury → Role 2. Terrain slows, threat lanes risk a mission-ending hit, Role 1 stabilises."""

    def __init__(self, spec: dict, seed: int = 42):
        self.s = spec; self.n = spec["size"]; self.rng = np.random.RandomState(seed); self.reset()

    def reset(self):
        self.pos = self.s["start"]; self.t = 0; self.stabilised = False; return self.state()

    def state(self):
        return self.pos[0] * self.n + self.pos[1]

    @property
    def n_states(self):
        return self.n * self.n

    def step(self, a: int):
        dr, dc = ACTIONS[a]
        r, c = self.pos
        nr, nc = min(max(r + dr, 0), self.n - 1), min(max(c + dc, 0), self.n - 1)
        self.pos = (nr, nc); self.t += 1
        reward = self.s["step_cost"] + self.s["terrain_cost"] * self.s["terrain"][nr, nc]
        done = False
        if self.s["threat"][nr, nc] and self.rng.random() < self.s["threat_risk"]:
            return self.state(), reward - 1.0, True, {"hit": True}
        if self.pos == self.s["role1"] and not self.stabilised:
            reward += self.s["role1_reward"]; self.stabilised = True
        if self.pos == self.s["goal"]:
            reward += self.s["goal_reward"]; done = True
        if self.t >= self.s["clock_limit"]:
            done = True
        return self.state(), reward, done, {}

    def render(self, ax, values=None, policy=None):
        import matplotlib.pyplot as plt  # noqa
        g = np.zeros((self.n, self.n)); g[self.s["terrain"] == 1] = 0.4; g[self.s["threat"] == 1] = 0.8
        ax.imshow(g, cmap="Greys", vmin=0, vmax=1); ax.grid(False)
        if values is not None:
            for i in range(self.n):
                for j in range(self.n):
                    ax.text(j, i, f"{values[i * self.n + j]:.2f}", ha="center", va="center", fontsize=8)
        if policy is not None:
            for i in range(self.n):
                for j in range(self.n):
                    dr, dc = ACTIONS[int(policy[i * self.n + j])]
                    ax.arrow(j, i, dc * 0.3, dr * 0.3, head_width=0.12, color="#0072B2")
        for key, mk, col in [("start", "o", "#009E73"), ("role1", "s", "#E69F00"), ("goal", "*", "#D55E00")]:
            r, c = self.s[key]; ax.plot(c, r, mk, ms=14, color=col)
        ax.set_xticks([]); ax.set_yticks([])
        return ax
