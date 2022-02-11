# CMPT 317: Colored Tiles Problem Starter code
# Jennifer Dang

import math as math

class State(object):
    """
       Note: Each state will need to store the action that created that state
       in a class variable called "action" to get full use out of scripts such
       as see_solutions.py
    """
    def __init__(self, board: list):
        """
        Initialize a new State object.
        
        """
        self.action = 'Initial state'
        self.board = board

    def __str__(self):
        """ A string representation of the State """
        string = ""
        string += f"{self.action}\n"
        for row in self.board:
            string += f"{row}\n"
        return string

    def __eq__(self, other):
        """ Defining this function allows states to be compared
        using the == operator """    
        if len(self.board) != len(other):
            return False
        for i in range(len(self.board)):
            if len(self.board[i]) != len(other[i]):
                return False
            for j in range(len(i)):
                if self.board[i][j] != other[i][j]:
                    return False
        return True
        
    

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
        
            :param nrows: number of rows in the tile puzzle
            :param ncols: number of columns in the tile puzzle
            :param start: a list of strings where each character is R or G.  Each string represents one row of the grid
        """
        self.start = start
        self.goal_state = State([["G" for _ in range(ncols)] for _ in range(nrows)])
        self.state = self.create_initial_state()
        self.actions = self.__get_actions__(nrows, ncols)
        return None       
    
    def __get_actions__(self, nrows: int, ncols: int) -> list:
        actions = []
        for row in range(nrows):
            for col in range(ncols):
                actions.append((row, col))
        return actions

    def create_initial_state(self) -> State:
        """ returns the initial state of othe problem
        """
        state = []
        for row in self.start:
            state.append(list(row))
        return state

    def is_goal(self, a_state:State) -> bool:
        """Returns True if the given state is a goal state"""
        return a_state == self.goal_state

    def actions(self, a_state:State) -> list:
        """ Returns all the actions that are legal in the given state.
            
        """
        return self.actions

    def result(self, a_state:State, an_action):
        """Given a state and an action, return the resulting state.
           
        """
        board = a_state.board
        row = an_action[0]
        col = an_action[1]

        get_color = lambda color: "G" if color == "R" else "G"

        board[row][col] = get_color(board[row][col])
        board[row-1][col] = get_color(board[row-1][col])
        board[row+1][col] = get_color(board[row+1][col])
        board[row][col-1] = get_color(board[row][col-1])
        board[row][col+1] = get_color(board[row][col+1])
         
        next_state = State(board)
        next_state.action = an_action
        return None



            
# end of file

