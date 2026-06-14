"""gameMatch.py — State and logic of a Rock Paper Scissors match."""
import random
from .moveType import MoveType

class GameMatch:
    """Manages the state and logic of a Rock Paper Scissors match.

    Attributes:
        human_move:    Current move chosen by the human player.
        cpu_move:      Current move chosen by the CPU.
        human_score:   Human player's current score.
        cpu_score:     CPU's current score.
        best_of:       Total number of rounds in the match.
        current_round: Current round number.
        draws:         Number of draw rounds.
        game_over:     True if the match has ended.
    """
    
    MSG_WIN = "YOU WIN THE MATCH!"
    MSG_LOSS = "CPU WIN THE MATCH!"
    MSG_DRAW = "IT'S A DRAW!"
    
    WIN_CONDITIONS: dict[MoveType,MoveType] = {
        MoveType.ROCK: MoveType.SCISSOR,
        MoveType.PAPER: MoveType.ROCK,
        MoveType.SCISSOR: MoveType.PAPER,
    }
    
    MOVE_NAMES: dict[MoveType,MoveType] = {
        MoveType.ROCK: "rock",
        MoveType.PAPER: "paper",
        MoveType.SCISSOR: "scissor",
    }
    
    def __init__(self, best_of: int = 3) -> None:
        """Initializes the match state.

        Args:
            best_of: Total number of rounds to play.
        """
        self.human_move: MoveType | None = None
        self.cpu_move: MoveType | None = None
        self.human_score: int = 0
        self.cpu_score: int = 0
        self.best_of: int = best_of
        self.current_round: int = 1
        self.draws: int = 0
        self.game_over: bool = False
        
    def play_round(self,human_move: MoveType) -> None:
        """Plays a single round given the human's move.

        Args:
            human_move: The move chosen by the human player.
        """
        if self.game_over:
            return
        
        self.human_move = human_move
        self.cpu_move = random.choice(list(MoveType))
        
        if self.human_move == self.cpu_move:
            self.draws += 1
            
        elif self.WIN_CONDITIONS[self.human_move] == self.cpu_move:
            self.human_score += 1
            
        else:
            self.cpu_score += 1
            
        if self.current_round < self.best_of:
            self.current_round += 1
            
        else:
            self.game_over = True
            
        
    def get_final_winner(self) -> str:
        """Returns the final match result as a string.

        Returns:
            A string describing who won the match.
        """
        if self.human_score > self.cpu_score:
            return self.MSG_WIN
        
        elif self.cpu_score > self.human_score:
            return self.MSG_LOSS
        
        else:
            return self.MSG_DRAW  