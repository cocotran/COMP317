# CMPT 317 A Python implementation of node queues for uninformed search.

# Copyright (c) 2016-2019 Michael C Horsch,
# Department of Computer Science, University of Saskatchewan

# This file is provided solely for the use of CMPT 317 students.  Students are permitted
# to use this file for their own studies, and to make copies for their own personal use.

# This file should not be posted on any public server, or made available to any party not
# enrolled in CMPT 317.

# This implementation is provided on an as-is basis, suitable for educational purposes only.

# This module defines the classes:
#     SearchNode (inherits from Python object class)
#     SearchTerminationRecord (inherits from Python object class)
#     Search (inherits from Python object class)

# Assumes a problem class with the methods:
#   is_goal(problem_state): returns True if the state is the goal state
#   actions(problem_state): returns a list of all valid actions in state
#                           (the actions are only passed to result())
#   result(state, action): returns a new state that is the result of doing action in state.
#
# Search methods are based on TreeSearch (no repeated state checking):
# 1. DepthFirstSearch(s)
# 2. BreadthFirstSearch(s)
# 3. DepthLimitedSearch(s, dlimit)
# 4. IDS(s)
# These methods return a SearchTerminationRecord object, containing information about the search.  See the definition below.
#
# Usage:
#   import UninformedSearch as Search
#   pi = <create a problem instance from some Problem class>
#   searcher = Search.Search(pi, <timelimit>)
#   s = <create an initial state for the problem, possibly a method from the Problem class>
#   result = searcher.DepthFirstSearch(s)
#            # or any of the methods above
#   print(str(result))
#   or public access to any of the data stored in the result.

# ALL SEARCH IS SUBJECT TO A TIME LIMIT.

import time as time
import Frontier as Frontiers


class SearchNode(object):
    """A data structure to store search information"""

    def __init__(self, state, parent_node, step_cost=1):
        """A SearchNode stores
             a single Problem state,
             a parent node
             the node's depth
             the node's path cost
        """
        self.state = state
        self.parent = parent_node
        if parent_node is None:
            self.path_cost = 0
            self.depth = 0
        else:
            self.path_cost = parent_node.path_cost + step_cost
            self.depth = parent_node.depth + 1

    def __str__(self):
        """ Create and return a string representation of the object"""
        return '<{}> {} ({})'.format(str(self.depth), str(self.state), str(self.path_cost))

    def display_steps(self):
        """Because a SearchNode stores a parent Node, we can trace the actions from
           initial state to the current state by stepping backwards up the tree.
           This does assume that your state stores the action that caused it to be
           created, as an attribute.
        """
        def disp(node):
            """ recursive function that displays actions
            """
            if node.parent is not None:
                disp(node.parent)
                print(str(node.state.action))

        print("Solution:")
        disp(self)


class SearchTerminationRecord(object):
    """A record to return information about how the search turned out.
       All the details are provided in a record, to avoid needing to print out the details
       at different parts of the code.
    """

    def __init__(self, success=False, result=None, time=0, nodes=0, space=0, cutoff=False):
        self.success = success  # Boolean: True if a solution was found
        self.result = result    # SearchNode: a node containing a goal state, or None if no solution found
        self.time = time        # float: time was spent searching.  Not scientifically accurate, but good enough for fun
        self.nodes = nodes      # integer: number of nodes expanded during the search
        self.space = space      # integer: maximum size of the frontier during search
        self.cutoff = cutoff    # Boolean: For IDS, True if depth limited search reach the depth limit before failing

    def __str__(self):
        """Create a string representation of the Result data
           This string doesn't show everything it could.
        """
        text = 'Search {} ({} sec, {} nodes, {} queue)'
        if self.success:
            textsuccess = 'successful'
        else:
            textsuccess = 'failed'
        return text.format(textsuccess, str(self.time), str(self.nodes), str(self.space))


class Search(object):
    """A class to contain uninformed search algorithms.
       API users should call the public methods.
       Subclasses inheriting this class can call _treeSearch() or _dltree_search()
    """

    def __init__(self, problem, timelimit=10):
        """The Search object needs to be given:
            the search Problem
            an optional timelime (default set above)
        """
        self._problem = problem
        self._frontier = None
        self._time_limit = timelimit


    def _tree_search(self, initial_state):
        """Search through the State space starting from an initial State.
           Simple tree search algorithm, used by API methods below.
           Monitors:
                time so as not to exceed a time limit.
                number of nodes expanded
                size of the frontier at any point
        """

        start_time = time.time()
        now = start_time
        self._frontier.add(SearchNode(initial_state, None))
        node_counter = 0
        max_space = 0

        # keep searching if there are nodes in the Frontier, and time left before the limit
        while not self._frontier.is_empty() and now - start_time < self._time_limit:
            max_space = max(max_space, len(self._frontier))
            this_node = self._frontier.remove()
            node_counter += 1
            now = time.time()
            if self._problem.is_goal(this_node.state):
                # Jeffnote, 2020-07-28: I started getting division-by-zero with time - was the search too fast?

                return SearchTerminationRecord(success=True, result=this_node,
                                    nodes=node_counter, space=max_space, time=max(now - start_time, 0.00001))
            else:
                for act in self._problem.actions(this_node.state):
                    child = self._problem.result(this_node.state, act)
                    self._frontier.add(SearchNode(child, this_node))

        # didn't find a solution!
        now = time.time()
        # Jeffnote, 2020-07-28: I started getting division-by-zero with time - was the search too fast?

        return SearchTerminationRecord(success=False, result=None,
                            nodes=node_counter, space=max_space, time=max(now - start_time, 0.00001))


    def DepthFirstSearch(self, initial_state, search_type):
        """
        Perform depth-first search of the problem,
        starting at a given initial state.
        :param initial_state: a Problem State
        :param search_type: either "tree" or "graph" to determine whether 
                            treesearch or graphsearch should be used
        :return: SearchTerminationRecord
        """
        # configure search: for DFS, we want the Frotnier with the LIFO Stack
        if search_type == "tree":
            self._frontier = Frontiers.FrontierLIFO()
        elif search_type == "graph":
            self._frontier = Frontiers.GFrontierLIFO()

        # run search
        return self._tree_search(initial_state)

    def BreadthFirstSearch(self, initial_state, search_type):
        """
        Perform breadth-first search of the problem,
        starting at a given initial state.
        :param initial_state: a Problem State
        :param search_type: either "tree" or "graph" to determine whether 
                            treesearch or graphsearch should be used
        :return: SearchTerminationRecord
        """
        # configure search: for BFS, we want the Frontier with the FIFO Queue
        if search_type == "tree":
            self._frontier = Frontiers.FrontierFIFO()
        elif search_type == "graph":
            self._frontier = Frontiers.GFrontierFIFO()

        # run search
        return self._tree_search(initial_state)

    def DepthLimitedSearch(self, initial_state, limit, search_type):
        """
        Perform depth-limited search of the problem,
        starting at a given initial state.
        :param initial_state: a Problem State
        :param limit: the maximum allowable depth
                    search_type: either "tree" or "graph" to determine whether 
                            treesearch or graphsearch should be used
        :return: SearchTerminationRecord
        """
        # configure search: We want the FIFO Frontier with the depth limit
        # self._frontier = Frontiers.FrontierLIFO_DL(limit)
        # Jeffnote, 2020-12-03: We'll REALLY want to use Graph search for the WaterJug problem
        if search_type == "tree":
            self._frontier = Frontiers.FrontierLIFO_DL(limit)
        elif search_type == "graph":
            self._frontier = Frontiers.GFrontierLIFO_DL(limit)


        # run search
        result = self._tree_search(initial_state)

        # another attribute to indicate whether we ran out of time (cutoff = True)
        # or if the search space was less deep than the limit, and we searched it all
        # (cutoff = False)
        # This is needed by Iterative Deepening, so that we know to stop searching deeper.
        result.cutoff = self._frontier._cutoff
        return result

    def IDS(self, initial_state, search_type):
        """Iterative deepening Search successively increases the search depth
           the search depth until a solution is found.
           :param search_type: either "tree" or "graph" to determine whether 
                            treesearch or graphsearch should be used
           :return: SearchTerminationRecord
                            """
        limit = 0
        nodes = 0
        time = 0
        space = 0
        while time < self._time_limit:
            answer = self.DepthLimitedSearch(initial_state, limit, search_type)
            if answer.success:
                answer.time += time
                answer.nodes += nodes
                answer.space = max(answer.space, space)
                return answer
            elif not self._frontier._cutoff:
                return SearchTerminationRecord(success=False, result=None, nodes=nodes, space=space, time=time)
            else:
                nodes += answer.nodes
                time += answer.time    # this could result in search that is substantial longer than the limit
                limit += 1
                space = max(answer.space, space)

        return SearchTerminationRecord(success=False, result=None, nodes=nodes, space=space, time=time)

# end of file
