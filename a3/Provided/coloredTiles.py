# CMPT 317: Colored Tiles Problem Model Solution

# Copyright (c) 2022, Jeff Long
# Department of Computer Science, University of Saskatchewan

# This file is provided solely for the use of CMPT 317 students.  Students are permitted
# to use this file for their own studies, and to make copies for their own personal use.

# This file should not be posted on any public server, or made available to any party not
# enrolled in CMPT 317.

# This implementation is provided on an as-is basis, suitable for educational purposes only.
# Jennifer Dang

import random as rand
import math as math

class State(object):
    """The Problem State is an array of Boolean values, which we represent by a nested list.  True means a green tile, False a red tile.
       The State also stores some convenience information about the state.
       An important aspect of the State representation is the action that
       caused this state to be created.
    """
    def __init__(self, puzzle):
        """
        Initialize the State object.
        :param puzzle: A nested list of rows, representing the tile grid.  Each value is a boolean.
        """
        self.action = 'Initial state'
        self.puzzle = [[col for col in row] for row in puzzle]
        self.nrows = len(self.puzzle)
        self.ncols = len(self.puzzle[0])

    def __str__(self):
        """ A string representation of the State """
        return '<{}>'.format(str(self.puzzle))

    def __eq__(self, other):
        """ Defining this function allows states to be compared
        using the == operator """        
        return self.puzzle == other.puzzle   
        
    def touch(self, x, y):
        """ touchs the grid at location (x, y), flipping the color of that
        space and all adjacent spaces"""
        self.puzzle[x][y] = not self.puzzle[x][y]
        if x-1 >= 0:
            self.puzzle[x-1][y] = not self.puzzle[x-1][y]
        if x+1 < self.ncols:
            self.puzzle[x+1][y] = not self.puzzle[x+1][y]
        if y-1 >= 0:
            self.puzzle[x][y-1] = not self.puzzle[x][y-1]
        if y+1 < self.nrows:
            self.puzzle[x][y+1] = not self.puzzle[x][y+1]

    def display(self):
        """ display state in more human readable format
        """
        for row in self.puzzle:
            line = ""
            for col in row:
                if col:
                    line += "G"
                else:
                    line += "R"
            print(line)
            
class InformedState(State):
    """We add an attribute to the state, namely a place to
        store the estimated path cost to the goal state.
    """
    def __init__(self, puzzle, hval=0):
        """Initialize the State.
           The hval attribute estimates the path cost to the goal state from the current state
           It should be calculated by the InformedProblem class, ans stored here for use.
        """
        super().__init__(puzzle)
        self.hval = hval


class Problem(object):
    """The Problem class defines aspects of the problem.
       One of the important definitions is the transition model for states.
       To interact with search classes, the transition model is defined by:
            is_goal(s): returns true if the state is the goal state.
            actions(s): returns a list of all legal actions in state s
            result(s,a): returns a new state, the result of doing action a in state s

    """

    def __init__(self, nrows, ncols, start=None):
        """ The problem is defined by an initial grid of tiles.
        It is assumed the goal state is an all-green grid.

            :param nrows: number of rows in the tile puzzle
            :param ncols: number of columns in the tile puzzle
            :param start: a list of strings where each character is R or G.  Each string represents one row of the grid
        """
        self.nrows = nrows
        self.ncols = ncols
        # convert from strings to nested list of booleans
        # in order to create a State
        start = [[col=="G" for col in row] for row in start]
        if start is not None: self.init_state = State(start)
        
        goalpuzzle = []
        for i in range(nrows):
            row = []
            for j in range(ncols):
                row.append(True)
            goalpuzzle.append(row)
        self.goal_state = State(goalpuzzle)  
        
        # legal actions based only on dimensions, so cache actions in advance for performance
        self.actions_cache = []
        for r in range(self.nrows):
            for c in range(self.ncols):
                # actions are just a coordinate pair for the square being touched
                a = (r, c)
                self.actions_cache.append(a)  # left
            

    def create_initial_state(self):
        """ returns an initial state.
            Here, we return the stored initial state.
        """
        return self.init_state

    def is_goal(self, a_state:State):
        """The target value is stored in the Problem instance."""
        return a_state == self.goal_state

    def actions(self, a_state:State):
        """ Returns all the actions that are legal in the given state.
            An action is a tuple representing a coordinate pair
            of the tile being touched to toggle its color.
            The actions are the same in every state, so we can just return the same
            list of actions every time rather than re-building it
        """
        return self.actions_cache

    def result(self, a_state:State, an_action):
        """Given a state and an action, return the resulting state.
           An action is a tuple representing a coordinate pair
           of the tile being touched to toggle its color.
        """

        new_state = State(a_state.puzzle)
        new_state.action = an_action
        new_state.touch(an_action[0], an_action[1])
    
        return new_state

class InformedProblem(Problem):
    """We add the ability to calculate an estimate to the goal state.
    """
    def __init__(self, nrows, ncols, start=None):
        """ The problem is defined by an initial grid of tiles.
        It is assumed the goal state is an all-green grid.

            :param nrows: number of rows in the tile puzzle
            :param ncols: number of columns in the tile puzzle
            :param start: a list of strings where each character is R or G.  Each string represents one row of the grid
        """
        super().__init__(nrows, ncols, start)

    def create_initial_state(self):
        """ returns an initial state.
            Here, we return the stored initial state.
            And we calculate the hval, and remember it.
        """
        hval = self.calc_h(self.init_state.puzzle)
        return InformedState(self.init_state.puzzle, hval)

    def calc_h(self, puzzle):
        """This function computes the heuristic function h(n)
        """
        # this trivial version returns 0, a trivial estimate, but consistent and admissible
        return 0

    def result(self, a_state, an_action):
        """Given a state and an action, return the resulting state.
           The super class does most of the work.
           We add the heuristic value to the informed state here.
        """
        astate = super().result(a_state, an_action)
        astate.hval = self.calc_h(astate.puzzle)
        return astate


class InformedProblemV1(InformedProblem):
    """ This version implements an admissible heuristic 
    """
    def __init__(self, nrows, ncols, start=None, goal=None):
        """ The problem is defined by an initial grid of tiles.
        It is assumed the goal state is an all-green grid.

            :param nrows: number of rows in the tile puzzle
            :param ncols: number of columns in the tile puzzle
            :param start: a list of strings where each character is R or G.  Each string represents one row of the grid
        """
        super().__init__(nrows, ncols, start)
       
    def calc_h(self, puzzle):
        # TODO: Implement this function with an admissible heuristic
        return 0

class InformedProblemV2(InformedProblem):
    """ This version implements a non-admissible heuristic
    """
    def __init__(self, nrows, ncols, start=None, goal=None):
        """ The problem is defined by an initial grid of tiles.
        It is assumed the goal state is an all-green grid.

            :param nrows: number of rows in the tile puzzle
            :param ncols: number of columns in the tile puzzle
            :param start: a list of strings where each character is R or G.  Each string represents one row of the grid
        """
        super().__init__(nrows, ncols, start)

        
    
    def calc_h(self, puzzle):
        #TODO: Implement a non-admissible heuristic
        return 0
 
            
            
# end of file

