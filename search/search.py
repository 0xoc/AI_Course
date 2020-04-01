# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    ds = util.Stack()
    visited = []
    node = (problem.getStartState(), None, None)
    
    ds.push(node)
    while not ds.isEmpty():
        # pop and unpack
        top = ds.pop()
        state, action, parent = top
        
        # ignore the state if visited before
        if state in visited:
            continue
        
        # mark the state as visited
        visited.append(state)
        
        # check for goal
        if problem.isGoalState(state):
            goal = top
            break
        
        # expand child nodes if not visited
        for nxtState, nxtAction, nxtCost in problem.getSuccessors(state):
            if nxtState not in visited:
                ds.push( (nxtState, nxtAction, top) )

    # travers the generated tree, to get a path
    node = goal
    actions = []
    # while there is an action
    while node[1]:
        actions.append(node[1])
        node = node[2]

    return actions[::-1]

def breadthFirstSearch(problem):
    
    ds = util.Queue()
    visited = []
    node = (problem.getStartState(), None, None)
    
    ds.push(node)
    while not ds.isEmpty():
        # pop and unpack
        top = ds.pop()
        state, action, parent = top
        
        # ignore the state if visited before
        if state in visited:
            continue
        
        # mark the state as visited
        visited.append(state)
        
        # check for goal
        if problem.isGoalState(state):
            goal = top
            break
        
        # expand child nodes if not visited
        for nxtState, nxtAction, nxtCost in problem.getSuccessors(state):
            if nxtState not in visited:
                ds.push( (nxtState, nxtAction, top) )

    # travers the generated tree, to get a path
    node = goal
    actions = []
    # while there is an action
    while node[1]:
        actions.append(node[1])
        node = node[2]

    return actions[::-1]


def uniformCostSearch(problem):
    
    ds = util.PriorityQueue()
    visited = []
    node = (problem.getStartState(), None, None, 0)    # state, action, parent, current cost
    
    ds.push(node, 0)

    while not ds.isEmpty():
        # pop and unpack
        top = ds.pop()
        state, action, parent, current_cost = top
        
        # ignore the state if visited before
        if state in visited:
            continue
        
        # mark the state as visited
        visited.append(state)
        
        # check for goal
        if problem.isGoalState(state):
            goal = top
            break
        
        # expand child nodes if not visited
        for nxtState, nxtAction, nxtCost in problem.getSuccessors(state):
            if nxtState not in visited:
                cost = current_cost + nxtCost
                ds.push( (nxtState, nxtAction, top, cost), cost )

    # travers the generated tree, to get a path
    node = goal
    actions = []
    # while there is an action
    while node[1]:
        actions.append(node[1])
        node = node[2]

    return actions[::-1]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    
    
    ds = util.PriorityQueue()
    visited = []
    node = (problem.getStartState(), None, None, 0)    # state, action, parent, current cost
    
    ds.push(node, 0)

    while not ds.isEmpty():
        # pop and unpack
        top = ds.pop()
        state, action, parent, current_cost = top
        
        # ignore the state if visited before
        if state in visited:
            continue
        
        # mark the state as visited
        visited.append(state)
        
        # check for goal
        if problem.isGoalState(state):
            goal = top
            break
        
        # expand child nodes if not visited
        for nxtState, nxtAction, nxtCost in problem.getSuccessors(state):
            if nxtState not in visited:
                cost = current_cost + nxtCost 
                ds.push( (nxtState, nxtAction, top, cost), cost + heuristic(nxtState, problem))

    # travers the generated tree, to get a path
    node = goal
    actions = []
    # while there is an action
    while node[1]:
        actions.append(node[1])
        node = node[2]

    return actions[::-1]



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
