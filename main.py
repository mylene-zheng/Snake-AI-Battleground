import pygame
import random
from interface import GameInterface, NIGHT_BLUE, WHITE
from environment import GameEnvironment
from agents.rl_agent import RLAgent
from metrics import PerformanceTracker
from agents.astar_agent import AgentAStar

def get_manhattan_distance(pos1, pos2):
    """Calculates the absolute grid distance between two points."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def main():
    # Initialize UI and Environment
    # Using a 10x10 grid with 35px cells so the RL agent performs well
    ui = GameInterface(grid_size=10, cell_size=35)
    env = GameEnvironment(grid_size=10)
    
    # Initialize and Load the RL Agent
    rl_agent = RLAgent()
    # Initialize and Load the A* Agent
    astar_agent = AgentAStar()
    tracker = PerformanceTracker()
    tracker.measure_memory("rl", rl_agent.q_table) # Measure Q-Table RAM instantly
    try:
        # Attempt to load the trained Q-Table
        rl_agent.charger_modele("models/qtable_v1.pkl")
        # Force the agent to EXPLOIT its knowledge (no random moves during demo)
        rl_agent.epsilon = 0.0 
    except FileNotFoundError:
        print("Warning: No trained model found. The RL snake will move randomly.")

    # State Machine Variables
    state = "MENU"
    astar_tested = False
    rl_tested = False
    
    # Simulation control flag
    sim_active = False

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle Mouse Clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                if state == "MENU":
                    # Clicked A* Button
                    if ui.btn_astar.collidepoint(mouse_pos):
                        state = "SIM_ASTAR"
                        astar_tested = True
                        
                        # --- THE FAIR START ---
                        random.seed(42) # Locks the randomness
                        env.reset()
                        sim_active = True
                        
                    # Clicked RL Button
                    elif ui.btn_rl.collidepoint(mouse_pos):
                        state = "SIM_RL"
                        rl_tested = True
                        
                        # --- THE FAIR START ---
                        random.seed(42) # Locks the randomness to the exact same sequence
                        env.reset()
                        sim_active = True

                        # Record the perfect distance to the very first apple
                        tracker.add_optimal_distance("rl", get_manhattan_distance(env.snake.body[0], env.food))
                        tracker.add_optimal_distance("astar", get_manhattan_distance(env.snake.body[0], env.food))
                        
                    # Clicked Compare Button (Only works if both are tested)
                    elif ui.btn_compare.collidepoint(mouse_pos) and astar_tested and rl_tested:
                        state = "COMPARISON"
                        
                elif state in ["SIM_ASTAR", "SIM_RL", "COMPARISON"]:
                    # Back button clicked
                    if ui.btn_back.collidepoint(mouse_pos):
                        state = "MENU"
                        sim_active = False # Stop the simulation if running

        # ==========================================
        # GAME LOGIC (The Animation)
        # ==========================================
        if sim_active:
            if state == "SIM_RL":
                current_state = env.get_rl_state()
                
                # --- START THE STOPWATCH ---
                tracker.start_timer() 
                action = rl_agent.obtenir_action(current_state)
                # --- STOP THE STOPWATCH ---
                tracker.stop_timer("rl") 
                
                _, reward, done = env.step(action)
                
                # Record the step
                tracker.record_step("rl")
                # If the snake gets a positive reward, it ate an apple and a new one spawned!
                if reward > 0: 
                    tracker.add_optimal_distance("rl", get_manhattan_distance(env.snake.body[0], env.food))
                
                if done:
                    sim_active = False 
                    tracker.set_score("rl", env.score) # Save final score

            elif state == "SIM_ASTAR":
                # --- START STOPWATCH ---
                tracker.start_timer()
                action = astar_agent.obtenir_action(env)
                tracker.stop_timer("astar")
                
                # Record how many nodes A* explored
                tracker.set_nodes("astar", astar_agent.nodes_explored)
                
                _, reward, done = env.step(action)
                tracker.record_step("astar")
                
                # If we ate an apple, record the perfect distance to the NEXT apple
                if reward > 0:
                    tracker.add_optimal_distance("astar", get_manhattan_distance(env.snake.body[0], env.food))
                    
                if done:
                    sim_active = False
                    tracker.set_score("astar", env.score)

        # ==========================================
        # DRAWING THE SCREEN
        # ==========================================
        if state == "MENU":
            ui.draw_menu(astar_tested, rl_tested)
            
        elif state == "SIM_ASTAR":
            ui.draw_simulation("Algorithme A*", env.score, list(env.snake.body), env.food)
            
        elif state == "SIM_RL":
            ui.draw_simulation("Renforcement", env.score, list(env.snake.body), env.food)
            
        elif state == "COMPARISON":
            # PULL THE REAL CALCULATED DATA!
            real_astar_data = tracker.get_formatted_metrics("astar")
            real_rl_data = tracker.get_formatted_metrics("rl")
            
            ui.draw_comparison(real_astar_data, real_rl_data)
            
        ui.update_display()
        
        # Frame Rate Control: Set to 10 FPS so you can actually watch it move!
        # If this is too fast, lower it to 5. If too slow, raise to 15.
        clock.tick(10)

    ui.close()

if __name__ == "__main__":
    main()