# Snake AI: A* Pathfinding vs. Reinforcement Learning

This project is a comparative study of two artificial intelligence paradigms applied to the classic game "Snake": **Heuristic Planning (A*)** and **Autonomous Learning (Q-Learning)**.

## 🧠 The Agents

- **A* Agent:** Uses the **Manhattan Distance** heuristic to calculate the shortest path to the target in real-time. It includes a survival "fallback strategy" for when paths are blocked.
- **RL Agent:** Implements **Q-Learning** with a discrete state space (Danger, Direction) and an **$\epsilon$-Greedy** exploration strategy.

## 🏗️ Architecture
The system follows a strict **Agent-Environment** pattern to ensure modularity.

- **Noyau (Core):** A Python engine using `collections.deque` for $O(1)$ snake movement.
- **Orchestrator:** Manages the 33ms/frame simulation loop and data flow between the AI and the world.
- **Interface:** A Pygame-based GUI featuring a "Dark Mode" (Blue Night theme) and real-time KPI dashboard.


## 📊 Key Performance Indicators (KPIs)
The application tracks several metrics to compare the two approaches:
* **M-01: Optimality** – Ratio between path taken and theoretical minimum.
* **M-02: Execution Time** – CPU time per decision in ms.
* **M-03: Exploration Cost** – Number of nodes opened (A*).
* **M-04: Memory** – RAM usage of the Q-Table or OpenSet.

## 🛠️ Installation & Usage

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/your-username/Snake-AI-Battleground.git](https://github.com/your-username/Snake-AI-Battleground.git)
   ```
