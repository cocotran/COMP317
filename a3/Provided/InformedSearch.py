# CMPT 317: A Python implementation of node queues for informed search.

# Copyright (c) 2016-2019 Michael C Horsch,
# Department of Computer Science, University of Saskatchewan

# This file is provided solely for the use of CMPT 317 students.  Students are permitted
# to use this file for their own studies, and to make copies for their own personal use.

# This file should not be posted on any public server, or made available to any party not
# enrolled in CMPT 317.

# This implementation is provided on an as-is basis, suitable for educational purposes only.

# Search methods are based on TreeSearch (no repeated state checking):
# 1. UCSSearch(s)
# 2. BestFirstSearch(s)
# 3. AStarSearch(s)
# These methods return a SearchTerminationRecord object, containing information about the search.
# See the definition in UninformedFrontier.

# Assumes a problem class with the methods:
#   is_goal(problem_state): returns True if the state is the goal state
#   actions(problem_state): returns a list of all valid actions in state
#                           (the actions are only passed to result())
#   result(state, action): returns a new state that is the result of doing action in state.
#
# Search methods are based on TreeSearch (no repeated state checking):
# 1. UCSSearch(s)
# 2. BestFirstSearch(s)
# 3. AStarSearch(s)
# These methods return a SearchTerminationRecord object, containing information about the search.
# See the definition in UninformedSearch.
#
# Usage:
#   import InformedSearch as Search
#   pi = <create a problem instance>
#   searcher = Search.Search(pi, <timelimit>)
#   s = <create an initial state for the problem>
#   result = searcher.AStarSearch(s)
#            # or any of the methods above
#   print(str(result))
#   # or public access to any of the data stored in the result.

import InformedFrontier as Frontiers
import UninformedSearch as BlindSearch


class InformedSearch(BlindSearch.Search):
    """A class to contain informed search algorithms."""

    def __init__(self, problem, timelimit=10):
        """The Search object needs to be given:
            the search Problem,
            a queue for Node(s) to explore
            possibly a depth limit to terminate search
        """
        BlindSearch.Search.__init__(self, problem, timelimit=timelimit)

    def BestFirstSearch(self, initialState):
        # configure search
        self._frontier = Frontiers.FrontierGBFS()
        # run search
        return self._tree_search(initialState)

    def UCSSearch(self, initialState):
        # configure search
        self._frontier = Frontiers.FrontierUCS()
        # run search
        return self._tree_search(initialState)

    def AStarSearch(self, initialState):
        # configure search
        self._frontier = Frontiers.GFrontierAStar()
        # run search
        return self._tree_search(initialState)
