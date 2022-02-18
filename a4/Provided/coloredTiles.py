# CMPT 317: Colored Tiles Problem Model Starter for Local Search

# Copyright (c) 2022, Jeff Long
# Department of Computer Science, University of Saskatchewan

# This file is provided solely for the use of CMPT 317 students.  Students are permitted
# to use this file for their own studies, and to make copies for their own personal use.

# This file should not be posted on any public server, or made available to any party not
# enrolled in CMPT 317.

# This implementation is provided on an as-is basis, suitable for educational purposes only.
#

import random as rand
import math as math


class State(object):
    """The Problem State is an array of Boolean values, which we represent by a nested list.  True means a green tile, False a red tile."""

    def __init__(self, puzzle, touchpoints):
        """
        Initialize the State object.
        :param puzzle: A nested list of rows, representing the tile grid.  Each value is a boolean.
        :param touchpoints: list of tuples represeting (row, col)
        coordinates on the tile grid
        """
        # CAREFUL!  For performance reasons, we are NOT
        # making a copy of the puzzle board, thus all states
        # are referencing the same board.  So DON'T CHANGE IT!
        # CONST
        self.puzzle = puzzle
        self.nrows = len(self.puzzle)
        self.ncols = len(self.puzzle[0])

        # The touchpoints are the main part of the state, so do make a copy
        self.touchpoints = [x for x in touchpoints]

    def __str__(self):
        """A string representation of the State"""
        return "<{} {}>".format(str(self.puzzle), str(self.touchpoints))

    def __eq__(self, other):
        """Defining this function allows states to be compared
        using the == operator"""
        return self.puzzle == other.puzzle and self.touchpoints == other.touchpoints

    def is_better_than(self, other):
        """
        Return True if self is a better solution than other
        :param: other: a State object
        :return: boolean
        """
        count = 0
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.puzzle[row][col]:
                    count += 1
                if other[row][col]:
                    count -= 1

        if count == 0:
            # The number of red tiles is equal
            return len(self.touchpoints) < len(other.touchpoints)

        return count > 0

    def is_equal_to(self, other):
        """
        Return True if self is as good a solution as other
        :param: other: a State object
        :return: boolean
        """
        count = 0
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.puzzle[row][col]:
                    count += 1
                if other[row][col]:
                    count -= 1

        if count == 0:
            # The number of red tiles is equal
            return len(self.touchpoints) == len(other.touchpoints)

        return False


class Problem(object):
    """The Problem class defines aspects of the problem."""

    def __init__(self, nrows, ncols, start=None):
        """The problem is defined by an initial grid of tiles.
        It is assumed the goal state is an all-green grid.

            :param nrows: number of rows in the tile puzzle
            :param ncols: number of columns in the tile puzzle
            :param start: a list of strings where each character is R or G.  Each string represents one row of the grid
        """
        self.nrows = nrows
        self.ncols = ncols
        # convert from strings to nested list of booleans
        # in order to create a State
        # initially, there are no touch points
        start = [[col == "G" for col in row] for row in start]

        if start is not None:
            self.init_state = State(start, [])

        # legal actions based only on dimensions, so cache actions in advance for performance
        self.actions_cache = []
        for r in range(self.nrows):
            for c in range(self.ncols):
                # actions are just a coordinate pair for the square being touched
                a = (r, c)
                self.actions_cache.append(a)  # left

    def create_initial_state(self):
        """returns an initial state.
        Here, we return the stored initial state.
        """
        return self.init_state

    def objective_function(self, state):
        """
        returns the value of the given state according
        to the objective function
        """
        count = 0
        for row in state.puzzle:
            for tile in row:
                if not tile:  # count red tiles
                    count += 1
        steps = 1 / len(state.touchpoints)
        return count - steps

    def random_state(self):
        """Return a random State, completely independent of any other State."""
        random_puzzle = []
        random_touchpoints = []

        for r in range(self.nrows):
            new_row = []
            for c in range(self.ncols):
                new_row.append(bool(rand.randint(0, 1)))
            random_puzzle.append(new_row)

        for step in range(rand.randint(1, self.nrows * self.ncols)):
            random_touchpoints.append(
                (
                    rand.randint(0, self.nrows * self.ncols - 1),
                    rand.randint(0, self.nrows * self.ncols - 1),
                )
            )

        return State(random_puzzle, random_touchpoints)

    def neighbors(self, state):
        """return a list of all neighbors of the given state."""
        # list of states that are neighbors to the given state
        neighbors = []

        # TODO: Implement this

        return neighbors

    def random_step(self, state):
        """Return a State that is a random neighbour of the given State.
        :param: state: A State object
        """
        # TODO: Implement this
        return None

    def best_step(self, state):
        """Return the best neighbouring State for the given State.
        It doesn't have to be better than the given State!
        :param: state: A State object
        """
        # TODO: Implement this
        return None

    def random_better(self, state):
        """Return a State that is a random BETTER neighbour of the given State.
        Should return None if there isn't one!
        :param: state: A State object
        """
        # TODO: Implement this
        return None


# end of file
