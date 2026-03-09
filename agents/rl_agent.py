import numpy as np
import random
import pickle
from typing import List, Tuple
from .base_agent import Agent

# Define the action space (matching the environment's directions)
ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)] # UP, DOWN, LEFT, RIGHT

class RLAgent(Agent):
    def __init__(self):
        # Hyperparameters from your Cahier des Charges
        self.alpha = 0.1          # Learning rate
        self.gamma = 0.99         # Discount factor
        self.epsilon = 1.0        # Initial exploration rate
        self.epsilon_min = 0.01   # Minimum exploration rate
        self.epsilon_decay = 0.995 # Decay factor per episode
        
        # Q-Table: Maps state-tuples to a NumPy array of 4 Q-values
        self.q_table = {}

    def _get_q_values(self, state: List[int]) -> np.ndarray:
        """Helper to get Q-values for a state, initializing to zeros if new."""
        state_tuple = tuple(state)
        if state_tuple not in self.q_table:
            self.q_table[state_tuple] = np.zeros(len(ACTIONS))
        return self.q_table[state_tuple]

    def obtenir_action(self, etat: List[int]) -> Tuple[int, int]:
        """Chooses an action using the epsilon-greedy strategy."""
        # Exploration: Random action
        if random.uniform(0, 1) < self.epsilon:
            action_idx = random.randint(0, len(ACTIONS) - 1)
        # Exploitation: Best known action
        else:
            q_values = self._get_q_values(etat)
            action_idx = np.argmax(q_values)
            
        return ACTIONS[action_idx]

    def entrainer(self, etat: List[int], action: Tuple[int, int], recompense: float, etat_suiv: List[int]):
        """Updates the Q-Table using the Bellman equation."""
        state_tuple = tuple(etat)
        next_state_tuple = tuple(etat_suiv)
        action_idx = ACTIONS.index(action)
        
        # Get current Q-value
        q_values = self._get_q_values(etat)
        current_q = q_values[action_idx]
        
        # Get max Q-value for the next state
        next_q_values = self._get_q_values(etat_suiv)
        max_next_q = np.max(next_q_values)
        
        # Bellman Equation update
        new_q = (1 - self.alpha) * current_q + self.alpha * (recompense + self.gamma * max_next_q)
        self.q_table[state_tuple][action_idx] = new_q

    def decay_epsilon(self):
        """Reduces epsilon after each episode."""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def sauvegarder_modele(self, filepath: str):
        """Saves the Q-table to a file."""
        with open(filepath, 'wb') as f:
            pickle.dump(dict(self.q_table), f)

    def charger_modele(self, filepath: str):
        """Loads the Q-table from a file."""
        with open(filepath, 'rb') as f:
            self.q_table = pickle.load(f)