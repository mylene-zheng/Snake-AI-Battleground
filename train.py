import os
import csv
import time
from environment import GameEnvironment
from agents.rl_agent import RLAgent

def train_agent(num_episodes=1000):
    # Ensure our persistence directories exist 
    os.makedirs("models", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Initialize a smaller environment to speed up early learning 
    env = GameEnvironment(grid_size=10)
    agent = RLAgent()

    # Setup the CSV log file 
    csv_file_path = "data/training_logs.csv"
    
    print(f"Starting training for {num_episodes} episodes...")
    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Structure based on your specifications, adding Epsilon to track learning 
        writer.writerow(["Episode_ID", "Algorithm_Type", "Score", "Steps", "Duration_ms", "Epsilon"])

        for episode in range(num_episodes):
            start_time = time.time()
            
            state = env.reset()
            done = False
            steps = 0

            while not done:
                # 1. Agent observes state and chooses action 
                action = agent.obtenir_action(state)
                
                # 2. Environment processes action 
                next_state, reward, done = env.step(action)
                
                # 3. Agent learns from the result 
                agent.entrainer(state, action, reward, next_state)
                
                # 4. Update current state
                state = next_state
                steps += 1

            # End of episode updates
            agent.decay_epsilon()
            duration_ms = int((time.time() - start_time) * 1000)

            # Log the episode data to CSV 
            writer.writerow([episode + 1, "Q-Learning", env.score, steps, duration_ms, round(agent.epsilon, 4)])

            # Print progress to the console every 100 episodes
            if (episode + 1) % 100 == 0:
                print(f"Episode: {episode + 1:4} | Score: {env.score:3} | Steps: {steps:4} | Epsilon: {agent.epsilon:.3f}")

    # Save the trained model to the models folder
    model_path = "models/qtable_v1.pkl"
    agent.sauvegarder_modele(model_path)
    print(f"\nTraining complete! Q-Table saved to '{model_path}'.")
    print(f"Performance logs saved to '{csv_file_path}'.")

if __name__ == "__main__":
    # 1000 is a good starting point for a 10x10 grid. 
    # You will likely need 5000+ for a 20x20 grid later.
    train_agent(num_episodes=100000)