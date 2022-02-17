# CMPT 317: A Python implementation of Frontier interfaces for informed search.

# Copyright (c) 2016-2019 Michael C Horsch,
# Department of Computer Science, University of Saskatchewan

# This file is provided solely for the use of CMPT 317 students.  Students are permitted
# to use this file for their own studies, and to make copies for their own personal use.

# This file should not be posted on any public server, or made available to any party not
# enrolled in CMPT 317.

# This implementation is provided on an as-is basis, suitable for educational purposes only.

# Simple implementations of the Frontier interface.
# Implementations in this module inherit from the Frontier class in the Frontier module
#   FrontierPQ: a base class
#   FrontierUCS(FrontierPQ):
#   FrontierGBFS(FrontierPQ):
#   FrontierAStar(FrontierPQ):
#   GFrontierAStar(FrontierPQ):

# Assumes a problem class with the methods:
#   is_goal(problem_state): returns True if the state is the goal state
#   actions(problem_state): returns a list of all valid actions in state
#                           (the actions are only passed to result())
#   result(state, action): returns a new state that is the result of doing action in state.
#   the State object is assumed to have a numeric attribute State.hval

# The Frontiers store SearchNodes.  SearchNOdes store ProblemStates.

import heapq as heapq
from Frontier import Frontier


class FrontierPQ(Frontier):
    """This version is a priority queue, and it is a base class for other
       Frontier classes in this module.

       We use heapq here, because it's convenient.
       heapq uses a list as its underlying data structure.
       heapq uses normal tuple-ordering, which is fine,
       except when there is a tie.

       The heapq module requires data to be stored as tuples
       (value, node), and the items are sorted according to value.
       However, when two values are equal, tuple ordering
       normally and reasonably looks at the rest of the tuple,
       and there's no good ordering for Nodes.

       So we play a little trick here, and we simply keep track
       of how many Nodes have been added to the queue, putting a unique
       counter value in the tuple after the value:

       (value, number, node)

       No two entries will have the same number, eliminating ties.
       This has the added benefit of ensuring that when there are ties
       for value, the queue will produce the states in the order they
       were generated.
    """

    def __init__(self):
        """ initialize the Frontier"""
        Frontier.__init__(self)
        self._counter = 0

    def remove(self):
        """remove a Node from the Frontier"""
        val = heapq.heappop(self._nodes)
        # return the state only
        return val[2]


class FrontierUCS(FrontierPQ):
    """This version looks at path-cost for ordering"""

    def __init__(self):
        """ initialize the Frontier"""
        FrontierPQ.__init__(self)

    def add(self, aNode):
        """add a Node to the Frontier"""
        self._counter += 1
        heapq.heappush(self._nodes, (aNode.path_cost, self._counter, aNode))


class FrontierGBFS(FrontierPQ):
    """This version looks at hval for ordering"""

    def __init__(self):
        """ initialize the Frontier"""
        FrontierPQ.__init__(self)

    def add(self, aNode):
        """add a Node to the Frontier"""
        self._counter += 1
        heapq.heappush(self._nodes, (aNode.state.hval, self._counter, aNode))


class FrontierAStar(FrontierPQ):
    """This version looks at path-cost + hval for ordering"""

    def __init__(self):
        """ initialize the Frontier"""
        FrontierPQ.__init__(self)

    def add(self, aNode):
        """add a Node to the Frontier"""
        self._counter += 1
        # print(aNode.path_cost, aNode.state.hval)
        heapq.heappush(self._nodes, (aNode.path_cost + aNode.state.hval, self._counter, aNode))


class GFrontierAStar(FrontierPQ):
    """This version looks at path-cost + hval for ordering, but discards any Node
       whose state also appears somewhere on the path from the initial state (i.e., a loop)"""

    def __init__(self):
        """ initialize the Frontier"""
        FrontierPQ.__init__(self)


    def add(self, aNode):
        """ Add a Node to the Frontier
            In Graph search, we will not add a Node to the Frontier if
            its state appears in some Node on the path from the initial state
            We can check this using the Node.parent attribute.
        """
        anc = aNode.parent
        while anc is not None:
            if anc.state == aNode.state:
                # a loop, so don't add this Node to the Frontier
                return
            anc = anc.parent
        # no parent state is the same, so no loop

        self._counter += 1
        # print(aNode.path_cost, aNode.state.hval)
        heapq.heappush(self._nodes, (aNode.path_cost + aNode.state.hval, self._counter, aNode))
