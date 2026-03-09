import pygame
from interface import GameInterface, NIGHT_BLUE, WHITE
# from environment import GameEnvironment
# from agents.rl_agent import RLAgent

def main():
    ui = GameInterface(grid_size=20, cell_size=25)
    
    # State Machine Variables
    state = "MENU" # Can be: "MENU", "SIM_ASTAR", "SIM_RL", "COMPARISON"
    
    # Flags to unlock the Comparison button
    astar_tested = False
    rl_tested = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle Mouse Clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
                mouse_pos = event.pos
                
                if state == "MENU":
                    if ui.btn_astar.collidepoint(mouse_pos):
                        state = "SIM_ASTAR"
                        astar_tested = True # Mark as tested
                        # TODO: Initialize Env and A* Agent here
                        
                    elif ui.btn_rl.collidepoint(mouse_pos):
                        state = "SIM_RL"
                        rl_tested = True # Mark as tested
                        # TODO: Initialize Env and load RL Agent here
                        
                    elif ui.btn_compare.collidepoint(mouse_pos) and astar_tested and rl_tested:
                        state = "COMPARISON"
                        
                elif state in ["SIM_ASTAR", "SIM_RL", "COMPARISON"]:
                    # Check if they clicked the back arrow in the header
                    if ui.btn_back.collidepoint(mouse_pos):
                        state = "MENU" # Return to homepage

        # Draw the correct screen based on current state
        if state == "MENU":
            ui.draw_menu(astar_tested, rl_tested)
            
        elif state == "SIM_ASTAR":
            # Replace with real environment data
            ui.draw_simulation("Algorithme A*", 0, [(5,5)], (10,10)) 
            
        elif state == "SIM_RL":
            # Replace with real environment data
            ui.draw_simulation("Renforcement", 150, [(5,5), (4,5)], (10,10))
            
        elif state == "COMPARISON":
            # Mock data to test the table rendering
            fake_astar_data = {"M01": "1.0 ratio", "M02": "15 ms", "M03": "450", "M04": "12 KB", "M05": "100%"}
            fake_rl_data = {"M01": "1.2 ratio", "M02": "2 ms", "M03": "N/A", "M04": "500 KB", "M05": "85%"}
            
            ui.draw_comparison(fake_astar_data, fake_rl_data)
            
        ui.update_display()
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()