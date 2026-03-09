import random
from collections import deque
from typing import Tuple, List, Dict

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
        self.reset()

    def reset(self):
        """Resets the environment for a new episode."""
        self.score = 0
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

        # 1. Check for failure (Collision)
        if self._check_collision(new_head):
            return self.get_rl_state(), -10.0, True

        # 2. Check for success (Eating food)
        if new_head == self.food:
            self.snake.grow(new_head)
            self.score += 1
            self._place_food()
            return self.get_rl_state(), 10.0, False

        # 3. Normal step
        self.snake.move(new_head)
        return self.get_rl_state(), -1.0, False

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
    def get_rl_state(self) -> List[int]:
        """
        Calculates the local vector state for the RL agent.
        Returns: [danger_straight, danger_right, danger_left, 
                  food_up, food_down, food_left, food_right]
        """
        head = self.snake.get_head()
        
        # Define the points immediately adjacent to the head
        point_l = (head[0] - 1, head[1])
        point_r = (head[0] + 1, head[1])
        point_u = (head[0], head[1] - 1)
        point_d = (head[0], head[1] + 1)
        
        # Identify current direction
        dir_l = self.snake.direction == LEFT
        dir_r = self.snake.direction == RIGHT
        dir_u = self.snake.direction == UP
        dir_d = self.snake.direction == DOWN

        # Calculate Danger based on relative direction
        # Danger Straight
        danger_straight = (dir_r and self._check_collision(point_r)) or \
                          (dir_l and self._check_collision(point_l)) or \
                          (dir_u and self._check_collision(point_u)) or \
                          (dir_d and self._check_collision(point_d))
                          
        # Danger Right (Relative to the snake's current facing)
        danger_right = (dir_u and self._check_collision(point_r)) or \
                       (dir_d and self._check_collision(point_l)) or \
                       (dir_l and self._check_collision(point_u)) or \
                       (dir_r and self._check_collision(point_d))

        # Danger Left (Relative to the snake's current facing)
        danger_left = (dir_d and self._check_collision(point_r)) or \
                      (dir_u and self._check_collision(point_l)) or \
                      (dir_r and self._check_collision(point_u)) or \
                      (dir_l and self._check_collision(point_d))

        # Food Location
        food_up = self.food[1] < head[1]
        food_down = self.food[1] > head[1]
        food_left = self.food[0] < head[0]
        food_right = self.food[0] > head[0]

        # Construct the final state vector
        state = [
            int(danger_straight),
            int(danger_right),
            int(danger_left),
            int(food_up),
            int(food_down),
            int(food_left),
            int(food_right)
        ]

        return state
    

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