import heapq

def manhattan_distance(pos1, pos2):
    """Calculates the absolute grid distance between two points."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class Node:
    """A tiny helper class to represent a square on the grid for A*."""
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start to this node
        self.h = 0  # Estimated cost from this node to food (Heuristic)
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        """Allows the priority queue to sort nodes by their lowest F-cost."""
        return self.f < other.f

class AgentAStar:
    def __init__(self):
        self.nodes_explored = 0 # To track M03 for the comparison table!

    def obtenir_action(self, env) -> tuple:
        """
        Calculates the optimal path to the food and returns the first step.
        """
        start = env.snake.body[0]
        target = env.food
        grid_size = env.grid_size
        
        # Treat the snake's body as solid walls
        obstacles = set(env.snake.body)
        
        # A* setup
        open_list = []
        closed_set = set()
        
        start_node = Node(start)
        start_node.h = manhattan_distance(start, target)
        start_node.f = start_node.h
        
        heapq.heappush(open_list, start_node)
        self.nodes_explored = 1
        
        path = []
        
        # The main A* loop
        while open_list:
            current_node = heapq.heappop(open_list)
            closed_set.add(current_node.position)
            
            # If we found the apple, trace the path back to the start!
            if current_node.position == target:
                curr = current_node
                while curr.parent is not None:
                    path.append(curr.position)
                    curr = curr.parent
                path.reverse() # Reverse it so it goes from Start -> Target
                break
                
            # Check Up, Down, Left, Right
            neighbors = [
                (current_node.position[0], current_node.position[1] - 1),
                (current_node.position[0], current_node.position[1] + 1),
                (current_node.position[0] - 1, current_node.position[1]),
                (current_node.position[0] + 1, current_node.position[1])
            ]
            
            for next_pos in neighbors:
                # 1. Skip if it hits a wall
                if next_pos[0] < 0 or next_pos[0] >= grid_size or next_pos[1] < 0 or next_pos[1] >= grid_size:
                    continue
                    
                # 2. Skip if it hits the snake's body
                if next_pos in obstacles:
                    continue
                    
                # 3. Skip if we already checked it
                if next_pos in closed_set:
                    continue
                    
                # Create the neighbor node
                neighbor_node = Node(next_pos, current_node)
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = manhattan_distance(next_pos, target)
                neighbor_node.f = neighbor_node.g + neighbor_node.h
                
                heapq.heappush(open_list, neighbor_node)
                self.nodes_explored += 1

        # ==========================================
        # DECISION TIME
        # ==========================================
        if path:
            # Normal Mode: We found a path! Take the first step.
            next_cell = path[0]
            action = (next_cell[0] - start[0], next_cell[1] - start[1])
            return action
        else:
            # SURVIVAL MODE: The apple is blocked off by our own body!
            # Pick ANY free adjacent cell just to survive one more turn.
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = start[0] + dx, start[1] + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and (nx, ny) not in obstacles:
                    return (dx, dy)
                    
            # Doomed. No safe moves. Just go right and accept death.
            return (1, 0)