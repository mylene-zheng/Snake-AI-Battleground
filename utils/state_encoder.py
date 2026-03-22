from typing import List


# Define directions to match the environment's logic
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class StateEncoder:
    """
    Translates the complex game grid into a simplified array of numbers 
    (sensors) so the Reinforcement Learning agent can process it.
    """
    # ==========================================
    # VISION FOR RL (Ruowen API)
    # ==========================================
    @staticmethod
    def get_rl_state(env) -> List[int]:
        """
        Takes the environment object and returns the 7-value state array.
        Calculates the local vector state for the RL agent.
        Returns: [danger_straight, danger_right, danger_left, 
                  food_up, food_down, food_left, food_right]
        """
        head = env.snake.get_head()
        
        # Define the points immediately adjacent to the head
        point_l = (head[0] - 1, head[1])
        point_r = (head[0] + 1, head[1])
        point_u = (head[0], head[1] - 1)
        point_d = (head[0], head[1] + 1)
        
        # Identify current direction
        dir_l = env.snake.direction == LEFT
        dir_r = env.snake.direction == RIGHT
        dir_u = env.snake.direction == UP
        dir_d = env.snake.direction == DOWN

        # Calculate Danger based on relative direction
        # Danger Straight
        danger_straight = (dir_r and env._check_collision(point_r)) or \
                          (dir_l and env._check_collision(point_l)) or \
                          (dir_u and env._check_collision(point_u)) or \
                          (dir_d and env._check_collision(point_d))
                          
        # Danger Right (Relative to the snake's current facing)
        danger_right = (dir_u and env._check_collision(point_r)) or \
                       (dir_d and env._check_collision(point_l)) or \
                       (dir_l and env._check_collision(point_u)) or \
                       (dir_r and env._check_collision(point_d))

        # Danger Left (Relative to the snake's current facing)
        danger_left = (dir_d and env._check_collision(point_r)) or \
                      (dir_u and env._check_collision(point_l)) or \
                      (dir_r and env._check_collision(point_u)) or \
                      (dir_l and env._check_collision(point_d))

        # Food Location
        food_up = env.food[1] < head[1]
        food_down = env.food[1] > head[1]
        food_left = env.food[0] < head[0]
        food_right = env.food[0] > head[0]

        # Construct the final state vector
        state = [
            danger_straight,
            danger_right,
            danger_left,
            food_up,
            food_down,
            food_left,
            food_right
        ]
        
        # Convert booleans to integers (1 for True, 0 for False)
        return [int(s) for s in state]