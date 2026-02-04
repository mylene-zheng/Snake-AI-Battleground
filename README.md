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
2. **Install dependencies:**
   ```bash
   pip install pygame numpy
   ```
3. **Run the simulation:**
   ```bash
   python main.py
   ```

## ⚙️ Hyperparameters (RL)
| Parameter | Value | Justification |
| :--- | :--- | :--- |
| **Learning Rate ($\alpha$)** | 0.1 | Ensures stable learning by avoiding Q-Table oscillations. |
| **Discount Factor ($\gamma$)** | 0.99 | Gives high importance to achieving long-term goals (eating apples). |
| **Exploration Rate ($\epsilon$)** | $1.0 \rightarrow 0.01$ | Encourages exploration initially, then shifts to exploitation over time. |
| **Decay Rate ($\epsilon_{decay}$)** | 0.995 | Multiplicative factor applied to $\epsilon$ after each episode. |
## 👥 Authors
Ruowen ZHENG 

Lina BERBOUCHA
