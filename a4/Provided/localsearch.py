# CMPT 317: A Python implementation of simple local search algorithms

# Copyright (c) 2016-2019 Michael C Horsch,
# Department of Computer Science, University of Saskatchewan

# This file is provided solely for the use of CMPT 317 students.  Students are permitted
# to use this file for their own studies, and to make copies for their own personal use.

# This file should not be posted on any public server, or made available to any party not
# enrolled in CMPT 317.

# This implementation is provided on an as-is basis, suitable for educational purposes only.

# Search methods as follows:
# 1. Random Guessing
# 2. Random Search
# 3. Hill-climbing
# 4. Stochastic Hill climbing
# 5. Random-restart Hill-climbing

# The search algorithms assume a Problem class with the methods:
#   random_state():
#       returns a completely random state
#   random_step(state): 
#       returns a neighbour one step away from the given state at random
#   best_step(state): 
#       returns the best neighbour one step away from the given state
#   random_better(state): 
#       returns a randomly chosen better neighbour of state

# The Local Search strategies also assume that a State class exists with the following methods:
#   is_better_than(self, other)
#       Returns True if the State object self is better, in terms of the objective function, 
#     than the State object other 
#   is_equal_to(self, other)
#       Returns True if the State object self is equal, in terms of the objective function, 
#       to the State object other.  


# Usage:
#   import localsearch as Search
#   pi = <create a problem instance according to the Problem class>
#   solution = Search.random_guessing(theProblem, 1000) 
#   #  solution is a State object

def random_guessing(problem, limit):
    """
    Solve the problem by proposing random states, always keeping the
    best state seen so far.
    :param problem: an instance of a class that responds to random_state() and is_better_than()
    :param limit: the number of proposals to try
    :return: the best of the states proposed, as judged by is_better_than()
    """

    count = 0
    # grab a random state to start with
    best_guess = problem.random_state()
    
    while count < limit:
        # propose a new random state
        guess = problem.random_state()
        count += 1

        # remember if it's better
        if guess.is_better_than(best_guess):
            best_guess = guess

    # return the best one
    return best_guess


def random_search(problem, limit):
    """
    Solve the problem by making a random change to the current state.
    Keep it if it the random change is better.

    :param problem: an instance of a class that responds to
                    random_state() is_better_than()  random_step()
    :param limit:  The number of times to try a random change
    :return: the best state seen during the process
    """

    count = 0
    # grab a random state to start with
    best_guess = problem.random_state()
    
    while count < limit:
        # ask for a random change to the current state
        guess = problem.random_step(best_guess)
        count += 1

        # keep it if it is better
        if guess.is_better_than(best_guess):
            best_guess = guess

    # return the best one
    return best_guess


def hillclimbing(problem, limit):
    """
    Solve a problem by taking the biggest uphill step at every state.
    Stop when there are no uphill steps, or you reached the limit.
    :param problem: an instance of a class that responds to
                    random_state() is_better_than() is_equal_to() best_step()
    :param limit: maximum number of uphill steps to try
    :return: the best state seen in the process
    """

    count = 0

    # grab a random state to start with
    best_guess = problem.random_state()

    while count < limit:
        # ask for the best state one step away from the current state
        best_neighbour = problem.best_step(best_guess)
        count += 1

        # if the best step is worse than the current state, stop looking (local maximum)
        if best_guess.is_better_than(best_neighbour):
            return best_guess
        # if the best step is equal to the current one, stop looking (plateau)
        elif best_neighbour.is_equal_to(best_guess):
            return best_guess
        # if the best step is uphill, remember it
        else:
            best_guess = best_neighbour

    # return the best one
    return best_guess


def stochastic_hillclimbing(problem, limit):
    """
    Solve a problem by taking a random uphill step at every state.
    Stop when there are no uphill steps, or you reached the limit.
    :param problem: an instance of a class that responds to
                    random_state() is_better_than()  random_better()
    :param limit: maximum number of uphill steps to try
    :return: the best state seen in the process
    """

    count = 0

    # grab a random state to start with
    best_guess = problem.random_state()

    while count < limit:
        # ask for a state that's better, chosen at random from the better states
        selection = problem.random_better(best_guess)
        count += 1

        # if a better state could not be found, stop looking
        if selection is None:
            return best_guess
        else:
            # remember the better one
            best_guess = selection

    # return the best one
    return best_guess


def random_restart(problem, rstarts=10, limit=10, stochastic=False):
    """
    Repeat hill-climbing by starting at several random locations.
    :param problem: an instance of a class that responds to
                    random_state() is_better_than()  best_step()
    :param rstarts: the number of times to start again from a random point
    :param limit: maximum number of uphill steps to try with each restart
    :return: the best state seen in the process
    """

    # do hill-climbing the first time,
    if stochastic:
        do_HC = stochastic_hillclimbing
    else:
        do_HC = hillclimbing
    
    best_guess = do_HC(problem, limit)

    for r in range(rstarts):
        # try again, maybe it's better?
        g = do_HC(problem, limit)

        # if it's better, remember it
        if g.is_better_than(best_guess):
            best_guess = g

    # return the best one
    return best_guess

# eof