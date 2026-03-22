import random
from collections import deque
from typing import Tuple, List, Dict
from utils.state_encoder import StateEncoder

# Define absolute directions (x, y)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self, start_pos: Tuple[int, int]):
        # Deque allows O(1) appends and pops at both ends
        self.body = deque([start_pos])
        self.direction = RIGHT

    def move(self, new_head: Tuple[int, int]):
        """Moves the snake forward by adding a new head and removing the tail."""
        self.body.appendleft(new_head)
        self.body.pop()

    def grow(self, new_head: Tuple[int, int]):
        """Grows the snake by adding a new head without removing the tail."""
        self.body.appendleft(new_head)

    def get_head(self) -> Tuple[int, int]:
        """Returns the current coordinates of the head."""
        return self.body[0]


class GameEnvironment:
    def __init__(self, grid_size: int = 20):
        self.grid_size = grid_size
        self.snake = None
        self.food = None
        self.score = 0
        self.steps_without_food = 0
        self.reset()

    def reset(self):
        """Resets the environment for a new episode."""
        self.score = 0
        self.steps_without_food = 0
        center = self.grid_size // 2
        self.snake = Snake((center, center))
        self._place_food()
        # Return the initial state for the RL agent by default
        return self.get_rl_state()

    def _place_food(self):
        """Places food randomly on an empty grid space."""
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake.body:
                self.food = (x, y)
                break

    def _check_collision(self, head: Tuple[int, int]) -> bool:
        """Checks if the head hits a wall or the snake's own body."""
        x, y = head
        # Check walls
        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
            return True
        # Check self (excluding the very end of the tail, as it moves forward)
        # We check self.snake.body dynamically in the step function usually, 
        # but a simple 'in' check works if we assume the new head position.
        if head in list(self.snake.body)[:-1]: 
            return True
        return False

    def step(self, action: Tuple[int, int]) -> Tuple[List[int], float, bool]:
        """
        Executes one frame of the game.
        Returns: (next_state, reward, done)
        """
        # Prevent the snake from reversing instantly into itself
        if (action[0] * -1, action[1] * -1) == self.snake.direction:
            action = self.snake.direction
        
        self.snake.direction = action
        current_head = self.snake.get_head()
        new_head = (current_head[0] + action[0], current_head[1] + action[1])
        self.steps_without_food += 1

        # 1. Check for failure (Collision)
        if self._check_collision(new_head):
            return self.get_rl_state(), -100.0, True # CHANGED to -100.0

        # 2. Check for success (Eating food)
        if new_head == self.food:
            self.snake.grow(new_head)
            self.score += 1
            self.steps_without_food = 0
            self._place_food()
            return self.get_rl_state(), 50.0, False  # CHANGED to +50.0

        # 3. Normal step
        self.snake.move(new_head)
        # Give a tiny survival bonus so it prefers empty space over walls
        return self.get_rl_state(), 0.0, False       # CHANGED to +0.1

    # ==========================================
    # VISION FOR A* (Lina's API)
    # ==========================================
    def get_full_state(self) -> Dict:
        """Returns exact coordinates for A* pathfinding."""
        return {
            "head": self.snake.get_head(),
            "body": list(self.snake.body),
            "food": self.food,
            "grid_size": self.grid_size
        }

    # ==========================================
    # VISION FOR RL (Ruowen API)
    # ==========================================
    def get_rl_state(self) -> list:
        """
        Delegates the state calculation to the dedicated StateEncoder.
        """
        # Pass 'self' (the whole environment) to the encoder
        return StateEncoder.get_rl_state(self)
    

if __name__ == "__main__":
    print("--- Starting Environment Test ---")
    
    # 1. Initialize a small grid to force a quick collision
    env = GameEnvironment(grid_size=5)
    
    print(f"Initial Snake Head: {env.snake.get_head()}")
    print(f"Initial Food Location: {env.food}")
    print(f"Initial RL State: {env.get_rl_state()}\n")

    # 2. Force the snake to move in a circle (Right, Down, Left, Up)
    test_moves = [
        ("RIGHT", (1, 0)),
        ("DOWN", (0, 1)),
        ("LEFT", (-1, 0)),
        ("UP", (0, -1)),
        ("UP", (0, -1)),
        ("UP", (0, -1)),
        ("UP", (0, -1)) # This last UP should cause it to hit the top wall (y < 0)
    ]

    for name, direction in test_moves:
        print(f"Moving: {name}")
        next_state, reward, done = env.step(direction)
        
        print(f"  New Head: {env.snake.get_head()}")
        print(f"  RL State: {next_state}")
        print(f"  Reward: {reward}")
        print(f"  Done (Game Over): {done}\n")
        
        if done:
            print("Crash detected! Environment is working correctly.")
            break