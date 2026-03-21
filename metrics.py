import time
import sys

class PerformanceTracker:
    def __init__(self):
        # Store raw data for both algorithms
        self.data = {
            "astar": {"steps": 0, "optimal_dist": 0, "time_ms": 0.0, "nodes": 0, "memory_kb": 0.0, "score": 0},
            "rl": {"steps": 0, "optimal_dist": 0, "time_ms": 0.0, "nodes": 0, "memory_kb": 0.0, "score": 0}
        }
        self._start_time = 0

    def start_timer(self):
        """Starts the high-precision stopwatch."""
        self._start_time = time.perf_counter()

    def stop_timer(self, algo: str):
        """Stops the stopwatch and adds the elapsed time in milliseconds."""
        elapsed_ms = (time.perf_counter() - self._start_time) * 1000
        self.data[algo]["time_ms"] += elapsed_ms

    def record_step(self, algo: str):
        """Counts how many actual moves the snake makes."""
        self.data[algo]["steps"] += 1

    def add_optimal_distance(self, algo: str, distance: int):
        """Adds the theoretical perfect Manhattan distance to the food."""
        self.data[algo]["optimal_dist"] += distance

    def set_nodes(self, algo: str, nodes: int):
        """Records the number of nodes explored (mostly for A*)."""
        self.data[algo]["nodes"] = nodes

    def measure_memory(self, algo: str, obj):
        """Calculates the RAM footprint of the AI model in Kilobytes."""
        # sys.getsizeof returns bytes, so we divide by 1024 for KB
        self.data[algo]["memory_kb"] = sys.getsizeof(obj) / 1024.0

    def set_score(self, algo: str, score: int):
        """Records the final score to determine success."""
        self.data[algo]["score"] = score

    def get_formatted_metrics(self, algo: str) -> dict:
        """Translates the raw data into the exact format your UI table expects."""
        d = self.data[algo]
        
        # M01: Optimalité (Ratio of Actual Steps to Perfect Steps)
        # 1.0 is perfect. Higher than 1.0 means it took a longer, safer route.
        if d["optimal_dist"] > 0:
            m01 = f"{d['steps'] / d['optimal_dist']:.2f}x"
        else:
            m01 = "N/A"
            
        # M02: Temps de Calcul (Average time per move)
        avg_time = d["time_ms"] / d["steps"] if d["steps"] > 0 else 0
        m02 = f"{avg_time:.2f} ms"
        
        # M03: Coût d'Exploration (Nodes)
        m03 = str(d["nodes"]) if d["nodes"] > 0 else "N/A"
        
        # M04: Consommation Mémoire
        m04 = f"{d['memory_kb']:.1f} KB"
        
        # M05: Taux de Réussite (We will use the Score for the visual demo)
        m05 = f"Score: {d['score']}"
        
        return {
            "M01": m01,
            "M02": m02,
            "M03": m03,
            "M04": m04,
            "M05": m05
        }