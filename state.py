from board import *

# List of possible moves
MOVES = ['up', 'down', 'left', 'right']

class State:
    """A class representing a state in the state-space search tree of an Eight Puzzle."""
    
    def __init__(self, board, predecessor=None, move=None):
        """
        Initializes a new State object.
        
        Args:
            board (Board): The Board object representing the current state of the puzzle.
            predecessor (State, optional): The State object representing the preceding state. Defaults to None.
            move (str, optional): The move that led to this state. Defaults to None.
        """
        self.board = board
        self.predecessor = predecessor
        self.move = move
        self.num_moves = 0 if predecessor is None else predecessor.num_moves + 1

    def is_goal(self):
        """
        Checks if the current state is the goal state.

        Returns:
            bool: True if this state is the goal state, otherwise False.
        """
        return self.board.tiles == GOAL_TILES

    def generate_successors(self):
        """
        Generates all valid successor states from the current state.

        Returns:
            list: A list of State objects representing successor states.
        """
        successors = []
        for move in MOVES:
            new_board = self.board.copy()
            if new_board.move_blank(move):
                new_state = State(new_board, self, move)
                successors.append(new_state)
        return successors

    def __repr__(self):
        """
        Returns a string representation of the State object.

        Returns:
            str: A string representation in the format "digit_string-move-num_moves".
        """
        return f"{self.board.digit_string()}-{self.move}-{self.num_moves}"

    def creates_cycle(self):
        """
        Checks if the current state creates a cycle in the sequence of moves.

        Returns:
            bool: True if a cycle is created, otherwise False.
        """
        state = self.predecessor
        while state is not None:
            if state.board == self.board:
                return True
            state = state.predecessor
        return False

    def __gt__(self, other):
        """
        Implements a > operator for State objects.
        Always returns True to ensure compatibility with priority queues.

        Args:
            other (State): Another State object.

        Returns:
            bool: Always True.
        """
        return True

    def print_moves_to(self):
        """
        Prints the sequence of moves from the initial state to this state.
        """
        if self.predecessor is None:
            print('Initial state:')
            print(self.board)
        else:
            self.predecessor.print_moves_to()
            print(f"Move the blank {self.move}:")
            print(self.board)

    def print_moves_to_list(self, result):
        """Appends the sequence of moves from the initial state to this state to a list.
        Args:result (list): A list to store the sequence of moves.
        """
        if self.predecessor is None:
            result.append('Initial state:')
            result.append(str(self.board))
        else:
            self.predecessor.print_moves_to_list(result)
            result.append(f"Move the blank {self.move}:")
            result.append(str(self.board))
