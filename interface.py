import pygame
from typing import List, Tuple, Dict

# === Color Palette ===
NIGHT_BLUE = (26, 26, 46)      # #1A1A2E
CYAN = (0, 255, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRID_LINE_COLOR = (40, 40, 60) # Slightly lighter than background for grid
DISABLED_GREY = (150, 150, 150) # For the locked comparison button

class GameInterface:
    def __init__(self, grid_size: int, cell_size: int = 25):
        pygame.init()
        self.grid_size = grid_size
        self.cell_size = cell_size
        
        self.board_width = self.grid_size * self.cell_size
        self.board_height = self.grid_size * self.cell_size
        self.header_height = 50
        
        # INCREASE THE MINIMUM WIDTH HERE (Change 400 to 650)
        self.window_width = max(self.board_width, 800)
        self.window_height = max(self.board_height + self.header_height, 450)
        
        # Calculate where to draw the board so it is always perfectly centered
        self.board_offset_x = (self.window_width - self.board_width) // 2
        
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Snake AI")
        
        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 20, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 18)  

        # 2. DYNAMIC CENTERING: Calculate button positions based on window size
        btn_w, btn_h = 450, 50
        center_x = (self.window_width // 2) - (btn_w // 2)
        start_y = self.window_height // 3  # Start a third of the way down
        
        self.btn_astar = pygame.Rect(center_x, start_y, btn_w, btn_h)
        self.btn_rl = pygame.Rect(center_x, start_y + 70, btn_w, btn_h)
        self.btn_compare = pygame.Rect(center_x, start_y + 140, btn_w, btn_h)
        self.btn_back = pygame.Rect(10, 10, 30, 30)

    # ==========================================
    # VIEW 1: MAIN MENU
    # ==========================================
    def draw_menu(self, astar_tested: bool, rl_tested: bool):
        self.screen.fill(WHITE) # White background for menu
        
        # Title
        title_surf = self.title_font.render("Snake game", True, NIGHT_BLUE)
        self.screen.blit(title_surf, (self.window_width//2 - title_surf.get_width()//2, 50))
        
        # Buttons
        pygame.draw.rect(self.screen, NIGHT_BLUE, self.btn_astar, border_radius=5)
        self._draw_centered_text("A* Algorithm", self.btn_astar, WHITE)

        pygame.draw.rect(self.screen, NIGHT_BLUE, self.btn_rl, border_radius=5)
        self._draw_centered_text("Reinforcement Learning", self.btn_rl, WHITE)

        # Comparison Button Logic (Locked vs Unlocked)
        compare_color = NIGHT_BLUE if (astar_tested and rl_tested) else DISABLED_GREY
        pygame.draw.rect(self.screen, compare_color, self.btn_compare, border_radius=5)
        self._draw_centered_text("Comparing the Two Approaches", self.btn_compare, WHITE)

    # ==========================================
    # VIEW 2: SIMULATION (Header + Grid)
    # ==========================================
    def draw_simulation(self, mode_name: str, score: int, snake_body: List, food: Tuple):
        # 1. Draw Header
        header_rect = pygame.Rect(0, 0, self.window_width, self.header_height)
        pygame.draw.rect(self.screen, WHITE, header_rect)
        
        # Draw Back Button (<-)
        pygame.draw.circle(self.screen, NIGHT_BLUE, self.btn_back.center, 15, width=3)
        pygame.draw.line(self.screen, NIGHT_BLUE, (15, 25), (32, 25), 2)
        pygame.draw.line(self.screen, NIGHT_BLUE, (15, 25), (20, 20), 2)  # Top arrow
        pygame.draw.line(self.screen, NIGHT_BLUE, (15, 25), (20, 30), 2)  # Bottom arrow
        
        # Header Text
        mode_surf = self.button_font.render(mode_name, True, NIGHT_BLUE)
        score_surf = self.button_font.render(f"Score: {score:04d}", True, NIGHT_BLUE)
        self.screen.blit(mode_surf, (self.window_width//2 - mode_surf.get_width()//2, 15))
        self.screen.blit(score_surf, (self.window_width - 120, 15))

        # 2. Draw Game Area 
        self.screen.fill(NIGHT_BLUE, (0, self.header_height, self.window_width, self.window_height))
        
        # Draw Grid Lines
        for x in range(0, self.board_width + 1, self.cell_size):
            line_x = self.board_offset_x + x
            pygame.draw.line(self.screen, GRID_LINE_COLOR, (line_x, self.header_height), (line_x, self.header_height + self.board_height))
        for y in range(0, self.board_height + 1, self.cell_size):
            line_y = self.header_height + y
            pygame.draw.line(self.screen, GRID_LINE_COLOR, (self.board_offset_x, line_y), (self.board_offset_x + self.board_width, line_y))

        # Draw Food & Snake (Offset by the centering math)
        if food:
            food_rect = (self.board_offset_x + food[0]*self.cell_size, self.header_height + food[1]*self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, RED, food_rect)
            
        for segment in snake_body:
            seg_rect = (self.board_offset_x + segment[0]*self.cell_size, self.header_height + segment[1]*self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, CYAN, seg_rect)

    # ==========================================
    # VIEW 3: COMPARISON TABLE
    # ==========================================
    def draw_comparison(self, metrics_astar: dict, metrics_rl: dict):
        """Draws the comparison dashboard with the back button and data table."""
        # 1. Draw Header
        header_rect = pygame.Rect(0, 0, self.window_width, self.header_height)
        pygame.draw.rect(self.screen, WHITE, header_rect)
        
        # Draw Back Button (<-)
        pygame.draw.circle(self.screen, NIGHT_BLUE, self.btn_back.center, 15, width=2)
        pygame.draw.line(self.screen, NIGHT_BLUE, (15, 25), (32, 25), 2)
        pygame.draw.line(self.screen, NIGHT_BLUE, (15, 25), (20, 20), 2)  # Top arrow
        pygame.draw.line(self.screen, NIGHT_BLUE, (15, 25), (20, 30), 2)  # Bottom arrow
        
        # Header Title
        title_surf = self.title_font.render("Comparison", True, NIGHT_BLUE)
        self.screen.blit(title_surf, (self.window_width//2 - title_surf.get_width()//2, 5))

        # 2. Draw Background (Dark Blue + Faint Grid)
        board_rect = pygame.Rect(0, self.header_height, self.window_width, self.window_height - self.header_height)
        pygame.draw.rect(self.screen, NIGHT_BLUE, board_rect)
        
        for x in range(0, self.window_width, self.cell_size):
            pygame.draw.line(self.screen, GRID_LINE_COLOR, (x, self.header_height), (x, self.window_height))
        for y in range(self.header_height, self.window_height, self.cell_size):
            pygame.draw.line(self.screen, GRID_LINE_COLOR, (0, y), (self.window_width, y))

        # 3. Draw the Table Structure
        table_width = self.window_width - 60
        table_height = 250
        table_x = 30
        table_y = self.header_height + 40

        # Main table background
        pygame.draw.rect(self.screen, (150, 180, 190), (table_x, table_y, table_width, table_height))
        
        # Headers
        col_width = table_width // 3
        headers = ["", "A* Algorithm", "Reinforcement Learning"]
        for i, text in enumerate(headers):
            surf = self.button_font.render(text, True, NIGHT_BLUE)
            self.screen.blit(surf, (table_x + (i * col_width) + 10, table_y + 10))

        # Draw Rows for M-01 to M-05
        row_labels = ["M01: Optimality", "M02: Time (ms)", "M03: Nodes", "M04: Memory (KB)", "M05: Success"]
        row_height = (table_height - 40) // 5
        
        for i, label in enumerate(row_labels):
            y_pos = table_y + 40 + (i * row_height)
            # Alternate row colors for readability
            if i % 2 == 0:
                pygame.draw.rect(self.screen, (170, 200, 210), (table_x, y_pos, table_width, row_height))
                
            # Row Label
            label_surf = self.text_font.render(label, True, NIGHT_BLUE)
            self.screen.blit(label_surf, (table_x + 10, y_pos + 10))
            
            # Placeholders for A* and RL Data (You will map the dicts here later)
            astar_val = self.text_font.render(str(metrics_astar.get(f"M0{i+1}", "-")), True, NIGHT_BLUE)
            rl_val = self.text_font.render(str(metrics_rl.get(f"M0{i+1}", "-")), True, NIGHT_BLUE)
            
            self.screen.blit(astar_val, (table_x + col_width + 10, y_pos + 10))
            self.screen.blit(rl_val, (table_x + (2 * col_width) + 10, y_pos + 10))

    # ==========================================
    # HELPER METHODS
    # ==========================================
    def _draw_centered_text(self, text: str, rect: pygame.Rect, color: Tuple):
        """Helper to draw text perfectly centered inside a button rectangle."""
        surf = self.button_font.render(text, True, color)
        text_x = rect.x + (rect.width - surf.get_width()) // 2
        text_y = rect.y + (rect.height - surf.get_height()) // 2
        self.screen.blit(surf, (text_x, text_y))

    def update_display(self):
        """Refreshes the screen."""
        pygame.display.flip()
        
    def close(self):
        """Safely shuts down Pygame."""
        pygame.quit()