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
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    from game import Directions
    
    # in Need2Visit, we store Alternative nodes by Stack
    # VisitedNode and Path can save states and path
    
    Need2Visit = Stack()

    # Structure Stack like ((x,y),[path])
    
    VisitedNode = []
    Path = []

    # Find the goal
    if problem.isGoalState(problem.getStartState()):
        return []
    
    # Check the state initial node & Add it in Need2Visit
    
    Need2Visit.push((problem.getStartState(),[]))

    while not Need2Visit.isEmpty():
        
        # Get the position's coordinate and path
        cur_node, Path = Need2Visit.pop()

        # Arrival
        if problem.isGoalState(cur_node):
            return Path

        # cur_node has been visited
        if cur_node not in VisitedNode:
            
            successor = problem.getSuccessors(cur_node)
            # after visiting currency node
            VisitedNode.append(cur_node)

            # successor will return a tuple (position, action, stepCost)
            for location, action, cost in successor:
                if (location not in VisitedNode):
                    Need2Visit.push((location, Path + [action] ))
        
    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    from game import Directions
    # in Need2Visit, we store Alternative nodes by Queue
    # VisitedNode and Path can save states and path
    
    Need2Visit = Queue()

    # Structure Queue like ((x,y),[path])
    
    VisitedNode = []
    Path = []
    
    if problem.isGoalState(problem.getStartState()):
        return []
    
    # Check the state initial node & Add it in Need2Visit
    
    Need2Visit.push((problem.getStartState(),[]))
    
    while not Need2Visit.isEmpty():
        
        # Get the position's coordinate and path
        cur_node, Path = Need2Visit.pop()

        # Arrival
        if problem.isGoalState(cur_node):
            return Path

        # cur_node has been visited
        if cur_node not in VisitedNode:
            
            successor = problem.getSuccessors(cur_node)
            
            # after visiting currency node
            VisitedNode.append(cur_node)

            # successor will return a tuple (position, action, stepCost)
            for location, action, cost in successor:
                if (location not in VisitedNode):
                    Need2Visit.push((location, Path + [action] ))
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    
    # in Need2Visit, we store Alternative nodes by PriorityQueue
    # VisitedNode and Path can save states and path
    
    Need2Visit = PriorityQueue()

    # Structure Priority Queue like ((x,y),[path],cost)
    VisitedNode = []
    Path = []
    
    if problem.isGoalState(problem.getStartState()):
        return []
    
    # Check the state initial node & Add it in Need2Visit
    # With the cheapest priority and add the cost = 0
    Need2Visit.push((problem.getStartState(),[]),0)
    
    while not Need2Visit.isEmpty():
        
        # Get the position's coordinate and path
        cur_node, Path = Need2Visit.pop()
        VisitedNode.append(cur_node)

        # Arrival
        if problem.isGoalState(cur_node):
            return Path

        # Get the successor or kids in the tree
        successor = problem.getSuccessors(cur_node)
            
        # after visiting currency node
        if successor:
            
            # Add new states in PriorityQueue and return path
            for location, action, cost in successor:

                # in Need2Visit.heap, the structure likes (priority, count and item))
                # item = position, path


                # haven't been visited and without a path from start to it
                if location not in VisitedNode and (location not in (state[2][0] for state in Need2Visit.heap)):

                    priority = problem.getCostOfActions((Path + [action]))
                    Need2Visit.push((location, (Path + [action]) ), priority)

                # haven't been visited and with a path from start to it
                elif (location not in VisitedNode) and (location in (state[2][0] for state in Need2Visit.heap)):
                    for state in Need2Visit.heap:
                        if state[2][0] == location:
                            oldPriority = problem.getCostOfActions(state[2][1])

                    newPriority = problem.getCostOfActions((Path + [action]))

                    # update the path which has a lower cost new path
                    if oldPriority > newPriority:
                        
                        Need2Visit.update((location,(Path + [action])),newPriority)

    # can't find solution
    return []

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    # We used PriorityQueue(heap) and select the least cost path
    # The direction in the head of team
    Need2Visit = PriorityQueue()

    
    VisitedNode = []
    Path = []
    
    if problem.isGoalState(problem.getStartState()):
        return Path

    # Structure Priority Queue like ((x,y),[path], heuristic)
    
    Need2Visit.push((problem.getStartState(),Path), 0)

    while Need2Visit:
        
        # Get the position's coordinate and path
        cur_node, Path = Need2Visit.pop()
        
        # Arrival
        if problem.isGoalState(cur_node):
            break

            
        # after visiting currency node.
        # If cur_node hasn't been visited, we will find all the successors and store them in PriorityQueue.
        # It means next time we will access the least cost node in the present situation.
        if cur_node not in VisitedNode :

            VisitedNode.append(cur_node)
            # Get the successor or kids in the tree
            successor = problem.getSuccessors(cur_node)
                
            for location, action, cost in successor:
                
                nextCost = problem.getCostOfActions((Path + [action])) + heuristic(location, problem)
                
                if location not in VisitedNode:
                    
                    Need2Visit.push((location, (Path + [action])),nextCost)
                    
    # if we find the goal state or all of the nodes in priorityqueue have been visited, we will return the path.
    
    return Path
        
    util.raiseNotDefined()

          

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
