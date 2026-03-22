import random
from environment import GameEnvironment
from agents.rl_agent import RLAgent
from agents.astar_agent import AgentAStar
from metrics import PerformanceTracker
from data import plot_algorithm_comparison

def get_manhattan_distance(pos1, pos2):
    """Calculates the absolute grid distance between two points."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def run_automated_benchmark(num_games=100):
    print(f"🚀 Démarrage du benchmark automatisé ({num_games} parties)...")
    
    env = GameEnvironment(grid_size=10)
    tracker = PerformanceTracker()
    
    # 1. Load Agents
    rl_agent = RLAgent()
    try:
        rl_agent.charger_modele("models/qtable_v1.pkl")
        rl_agent.epsilon = 0.0 # Exploit only!
    except FileNotFoundError:
        print("⚠️ Attention: Modèle RL introuvable.")

    astar_agent = AgentAStar()

    # Measure RAM footprint immediately
    tracker.measure_memory("rl", rl_agent.q_table)
    tracker.measure_memory("astar", astar_agent)

    # Generate a fixed set of seeds so both algorithms face the exact same 100 maps
    seeds = [42 + i for i in range(num_games)]

    # ==========================================
    # TEST 1 : ALGORITHME A*
    # ==========================================
    print("⏳ Évaluation de l'Algorithme A* en cours...")
    for seed in seeds:
        random.seed(seed)
        env.reset()
        tracker.add_optimal_distance("astar", get_manhattan_distance(env.snake.body[0], env.food))
        done = False
        
        while not done:
            tracker.start_timer()
            action = astar_agent.obtenir_action(env)
            tracker.stop_timer("astar")
            
            # Accumulate nodes explored
            tracker.data["astar"]["nodes"] += astar_agent.nodes_explored
            
            _, reward, done = env.step(action)
            tracker.record_step("astar")
            
            if reward > 0:
                tracker.add_optimal_distance("astar", get_manhattan_distance(env.snake.body[0], env.food))

    # ==========================================
    # TEST 2 : APPRENTISSAGE PAR RENFORCEMENT
    # ==========================================
    print("⏳ Évaluation de l'Apprentissage RL en cours...")
    for seed in seeds:
        random.seed(seed)
        env.reset()
        tracker.add_optimal_distance("rl", get_manhattan_distance(env.snake.body[0], env.food))
        done = False
        
        while not done:
            current_state = env.get_rl_state()
            
            tracker.start_timer()
            action = rl_agent.obtenir_action(current_state)
            tracker.stop_timer("rl")
            
            _, reward, done = env.step(action)
            tracker.record_step("rl")
            
            if reward > 0:
                tracker.add_optimal_distance("rl", get_manhattan_distance(env.snake.body[0], env.food))

    # ==========================================
    # CALCUL DES MOYENNES ET AFFICHAGE
    # ==========================================
    print("✅ Simulations terminées ! Calcul des statistiques...")
    d_astar = tracker.data["astar"]
    d_rl = tracker.data["rl"]

    # Calculate Time per move (ms)
    astar_time = d_astar["time_ms"] / d_astar["steps"] if d_astar["steps"] > 0 else 0
    rl_time = d_rl["time_ms"] / d_rl["steps"] if d_rl["steps"] > 0 else 0

    # Calculate Average Nodes explored per move
    astar_nodes_avg = d_astar["nodes"] / d_astar["steps"] if d_astar["steps"] > 0 else 0
    
    # Get Memory in KB
    astar_mem = d_astar["memory_kb"]
    rl_mem = d_rl["memory_kb"]

    print("\n📊 RÉSULTATS FINAUX :")
    print(f"A* -> Temps: {astar_time:.3f} ms | Nœuds moyens: {astar_nodes_avg:.0f} | Mémoire: {astar_mem:.2f} KB")
    print(f"RL -> Temps: {rl_time:.3f} ms | Nœuds moyens: 0 | Mémoire: {rl_mem:.2f} KB")

    print("\n🎨 Génération des graphiques...")
    plot_algorithm_comparison(astar_time, rl_time, astar_mem, rl_mem, astar_nodes_avg)

if __name__ == "__main__":
    # Runs 100 completely fair, identical games as fast as your CPU can handle
    run_automated_benchmark(num_games=100)