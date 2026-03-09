from abc import ABC, abstractmethod
from typing import Any, Tuple

class Agent(ABC):
    """
    Abstract base class for all AI agents in the Snake game.
    This enforces the Agent-Environment paradigm.
    """

    @abstractmethod
    def obtenir_action(self, etat: Any) -> Tuple[int, int]:
        """
        Takes the current state of the environment and returns the optimal action.
        
        Args:
            etat (Any): The current state of the game. 
                        - For RL, this will be the 7-value boolean List.
                        - For A*, this will be the full grid Dict.
            
        Returns:
            Tuple[int, int]: The chosen direction vector (e.g., (0, -1) for UP).
        """
        pass