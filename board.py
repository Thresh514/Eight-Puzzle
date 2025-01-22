# board.py (Final project)
#
# A Board class for the Eight Puzzle
#
# name: Jiayong Tu
# email: jytu@bu.edu
#
# If you worked with a partner, put their contact info below:
# partner's name: Jinyu Liu
# partner's email: ljinyu@bu.edu
#

GOAL_TILES = [['0', '1', '2'],
                ['3', '4', '5'],
                ['6', '7', '8']]

class Board:
    """A class for objects that represent an Eight Puzzle board."""

    def __init__(self, digitstr: str):
        """
        Initializes a Board object with the given digit string.

        Args:
            digitstr (str): A 9-character string containing digits 0-8.

        Raises:
            AssertionError: If digitstr is not a valid 9-character permutation of '0'-'8'.
        """
        assert len(digitstr) == 9, "Input must be a 9-character string."
        assert set(digitstr) == set("012345678"), "Input must contain digits 0-8 exactly once."

        self.tiles = [[digitstr[3 * i + j] for j in range(3)] for i in range(3)]
        self.blank_r, self.blank_c = next(
            (i, j) for i in range(3) for j in range(3) if self.tiles[i][j] == '0'
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the Board.

        Returns:
            str: The board layout with '_' representing the blank tile.
        """
        return '\n'.join(
            ' '.join('_' if tile == '0' else tile for tile in row)
            for row in self.tiles
        ) + '\n'

    def move_blank(self, direction: str) -> bool:
        """
        Moves the blank tile in the specified direction if possible.

        Args:
            direction (str): The direction to move ('up', 'down', 'left', 'right').

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        moves = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }

        if direction not in moves:
            return False

        dr, dc = moves[direction]
        new_r, new_c = self.blank_r + dr, self.blank_c + dc

        if 0 <= new_r < 3 and 0 <= new_c < 3:
            self.tiles[self.blank_r][self.blank_c], self.tiles[new_r][new_c] = \
                self.tiles[new_r][new_c], self.tiles[self.blank_r][self.blank_c]
            self.blank_r, self.blank_c = new_r, new_c
            return True
        return False

    def digit_string(self) -> str:
        """
        Converts the board layout into a single string of digits.

        Returns:
            str: A 9-character string representing the board.
        """
        return ''.join(''.join(row) for row in self.tiles)

    def copy(self) -> 'Board':
        """
        Creates a deep copy of the current Board object.

        Returns:
            Board: A new Board object with the same layout.
        """
        return Board(self.digit_string())

    def num_misplaced(self) -> int:
        """
        Counts the number of misplaced tiles compared to the goal state.

        Returns:
            int: The number of misplaced tiles (excluding the blank tile).
        """
        return sum(
            1 for r in range(3) for c in range(3)
            if self.tiles[r][c] != GOAL_TILES[r][c] and self.tiles[r][c] != '0'
        )

    def goal_distance(self) -> int:
        """
        Computes the Manhattan distance of all tiles from their goal positions.

        Returns:
            int: The total Manhattan distance.
        """
        distance = 0
        for r in range(3):
            for c in range(3):
                value = self.tiles[r][c]
                if value != '0':
                    goal_r, goal_c = divmod(int(value), 3)
                    distance += abs(goal_r - r) + abs(goal_c - c)
        return distance

    def __eq__(self, other: 'Board') -> bool:
        """
        Checks if two Board objects are equal.

        Args:
            other (Board): Another Board object to compare.

        Returns:
            bool: True if the boards are equal, False otherwise.
        """
        return self.tiles == other.tiles

    def is_solvable(self):
        """
        Checks if the current board configuration is solvable.
        Returns:
        bool: True if solvable, False otherwise.
        """
        inversions = 0
        tiles = self.digit_string().replace('0', '')  # 忽略空格
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i] > tiles[j]:
                    inversions += 1
        return inversions % 2 == 0