import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space search on an Eight Puzzle. """

    def __init__(self, depth_limit):
        """
        Initializes a Searcher object.
        
        Args:
            depth_limit (int): The maximum depth to search (-1 for no limit).
        """
        self.states = []  # List of untested states
        self.num_tested = 0  # Counter for tested states
        self.depth_limit = depth_limit  # Depth limit for the search
        self.visited = set()  # Set of visited states to prevent duplicates

    def should_add(self, state):
        """
        Determines whether a state should be added to the list of untested states.
        
        Args:
            state (State): The state to check.

        Returns:
            bool: True if the state should be added, False otherwise.
        """
        if self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        if state.creates_cycle():
            return False
        if state.board.digit_string() in self.visited:  # Check if state was already visited
            return False
        return True

    def add_state(self, new_state):
        """
        Adds a single State object to the list of untested states and marks it as visited.
        
        Args:
            new_state (State): The state to add.
        """
        self.states.append(new_state)
        self.visited.add(new_state.board.digit_string())  # Mark as visited

    def add_states(self, new_states):
        """
        Adds multiple states to the list of untested states.
        
        Args:
            new_states (list): A list of State objects to add.
        """
        for state in new_states:
            if self.should_add(state):
                self.add_state(state)

    def next_state(self):
        """
        Returns the next state to be tested (default implementation: random choice).
        
        Returns:
            State: The next state to test.
        """
        state = self.states.pop(0)  # FIFO for BFS
        return state

    def find_solution(self, init_state):
        """
        Performs a full state-space search starting from the initial state.
        
        Args:
            init_state (State): The initial state of the search.

        Returns:
            State: The goal state if found, otherwise None.
        """
        self.add_state(init_state)
        while len(self.states) > 0:
            s = self.next_state()
            self.num_tested += 1
            if s.is_goal():
                return s
            else:
                self.add_states(s.generate_successors())
        return None


class BFSearcher(Searcher):
    """Performs breadth-first search (BFS)."""
    def next_state(self):
        """Overrides the next_state method for BFS."""
        next_state = self.states.pop(0)
        return next_state


class DFSearcher(Searcher):
    def next_state(self):
        """
        Overrides the next_state method to implement DFS logic.
        Always returns the last state in the list (LIFO).
        """
        next_state = self.states[-1]
        self.states = self.states[:-1]
        return next_state

    def find_solution(self, init_state):
        """
        Performs a full state-space search starting from the initial state.
        """
        self.add_state(init_state)
        depth = 0  # 当前深度
        while len(self.states) > 0:
            depth += 1
            print(f"Depth: {depth}, States tested: {self.num_tested}, Remaining states: {len(self.states)}")
            s = self.next_state()
            self.num_tested += 1
            if s.is_goal():
                return s
            else:
                self.add_states(s.generate_successors())
        return None


def h0(state):
    """A heuristic function that always returns 0."""
    return 0


def h1(state):
    """Heuristic: Number of misplaced tiles."""
    return state.board.num_misplaced()


def h2(state):
    """Heuristic: Manhattan distance."""
    return state.board.goal_distance()


class GreedySearcher(Searcher):
    """Performs greedy state-space search."""
    def __init__(self, heuristic):
        super().__init__(-1)
        self.heuristic = heuristic

    def __repr__(self):
        s = f"{type(self).__name__}: {len(self.states)} untested, {self.num_tested} tested, heuristic {self.heuristic.__name__}"
        return s

    def priority(self, state):
        """Computes the priority of a state based on the heuristic."""
        return -self.heuristic(state)

    def add_state(self, state):
        """Adds a state as a [priority, state] pair."""
        self.states.append([self.priority(state), state])

    def next_state(self):
        """Chooses and returns the state with the highest priority."""
        high_priority_state = max(self.states)
        self.states.remove(high_priority_state)
        return high_priority_state[1]


class AStarSearcher(Searcher):
    """Performs A* state-space search."""
    def __init__(self, heuristic):
        super().__init__(-1)
        self.heuristic = heuristic

    def __repr__(self):
        s = f"{type(self).__name__}: {len(self.states)} untested, {self.num_tested} tested, heuristic {self.heuristic.__name__}"
        return s

    def priority(self, state):
        """Computes the priority of a state based on the heuristic and the cost."""
        return - (self.heuristic(state) + state.num_moves)

    def add_state(self, state):
        """Adds a state as a [priority, state] pair."""
        self.states.append([self.priority(state), state])

    def next_state(self):
        """Chooses and returns the state with the highest priority."""
        high_priority_state = max(self.states)
        self.states.remove(high_priority_state)
        return high_priority_state[1]
