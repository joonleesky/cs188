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

def reverse(direction):
    REVERSE = {'North': 'South',
               'South': 'North',
               'East': 'West',
               'West': 'East',
               'Stop': 'Stop'}
    return REVERSE[direction]
    

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    #Initialize
    memory  = util.Stack()
    startState = problem.getStartState()
    
    path = []
    visited = []
    
    visited.append(startState)
    startNode = (startState, 'Stop', 0)
    memory.push(startNode)
    
    #Iterate
    while(1):        
        #When the memory is empty
        if memory.isEmpty() == True:
            return []
        
        #Find Current State
        curState = memory.list[-1][0]
        
        #If the next state is the goal state, finish
        if problem.isGoalState(curState) == True:
            path = [node[1] for node in memory.list]
            return path
        
        
        #Get Successors that has not been visited
        successors = problem.getSuccessors(curState)
        successors = [node for node in successors if node[0] not in visited]
        
        #If there are no places to visit, pop from the memory and continue
        if len(successors) == 0:
            memory.pop()
            continue
        
        #Select action and get state
        nextNode = successors[0]
        nextState = nextNode[0]
        
        memory.push(nextNode)
        visited.append(nextState)
        

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    #Initialize
    memory  = util.Queue()
    startState = problem.getStartState()
    
    nodeDict = {} #Store the parent and the action of each node
    path = []
    visited = []
    
    startNode = (startState, 'Stop', 0)
    memory.push(startNode)
    visited.append(startState)
    
    #Iterate
    while(1):        
        #When the memory is empty
        if memory.isEmpty() == True:
            return []
        
        #Find Current State
        curNode = memory.pop()
        curState = curNode[0]
        
        #If the next state is the goal state, find the path
        if problem.isGoalState(curState) == True:
            #Recursively find the parent for the shortest path
            while(1):
                if curState == startState:
                    break
                action = nodeDict[curState][1]
                path.append(action)
                curState = nodeDict[curState][0]
                
            #Reverse the sequence of the actions
            return list(reversed(path))
        
        
        #Get Successors that has not been visited
        successors = problem.getSuccessors(curState)
        successors = [node for node in successors if node[0] not in visited]
        
        #If there are no places to visit,continue
        if len(successors) == 0:
            continue
        
        #Push child nodes to the memory
        for successor in successors:
            nextState = successor[0]
            nextAction = successor[1]

            memory.push(successor)
            nodeDict[nextState] = (curState, nextAction)
            visited.append(nextState)

            
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #Initialize
    memory  = util.PriorityQueue()
    startState = problem.getStartState()
    
    nodeDict = {} #Store the parent and the action of each node
    total_cost = 0
    path = []
    visited = []
    
    startNode = (startState, 'Stop')
    memory.push(startNode, 0)
    visited.append(startState)
    
    #Iterate
    while(1):        
        #When the memory is empty
        if memory.isEmpty() == True:
            return []

        #Find Current State
        curNode, curCost = memory.pop()
        curState = curNode[0]

        #If the next state is the goal state, find the path
        if problem.isGoalState(curState) == True:
            #Recursively find the parent for the shortest path
            while(1):
                if curState == startState:
                    break
                action = nodeDict[curState][1]
                path.append(action)
                curState = nodeDict[curState][0]
                
            #Reverse the sequence of the actions
            return list(reversed(path))

        #Get Successors that has not been visited
        successors = problem.getSuccessors(curState)
        successors = [node for node in successors if node[0] not in visited]
        
        #If there are no places to visit,continue
        if len(successors) == 0:
            continue
        
        #Push child nodes to the memory
        for successor in successors:
            nextState = successor[0]
            nextAction = successor[1]
            nextCost = curCost + successor[2]
            nextNode = (nextState, nextAction)
            
            #Prioirty of the node is the cumulative cost of the path
            memory.push(nextNode, nextCost)
            nodeDict[nextState] = (curState, nextAction)
            visited.append(nextState)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
        #Initialize
    
    memory  = util.PriorityQueue()
    startState = problem.getStartState()
    
    nodeDict = {} #Store the parent and the action of each node
    total_cost = 0
    path = []
    visited = []
    
    startNode = (startState, 'Stop')
    memory.push(startNode, 0)
    visited.append(startState)
    
    #Iterate
    while(1):        
        #When the memory is empty
        if memory.isEmpty() == True:
            return []

        #Find Current State
        curNode, curCost = memory.pop()
        curState = curNode[0]

        #If the next state is the goal state, find the path
        if problem.isGoalState(curState) == True:
            #Recursively find the parent for the shortest path
            while(1):
                if curState == startState:
                    break
                action = nodeDict[curState][1]
                path.append(action)
                curState = nodeDict[curState][0]
                
            #Reverse the sequence of the actions
            return list(reversed(path))

        #Get Successors that has not been visited
        successors = problem.getSuccessors(curState)
        successors = [node for node in successors if node[0] not in visited]
        
        #If there are no places to visit,continue
        if len(successors) == 0:
            continue
        
        #Push child nodes to the memory
        for successor in successors:
            nextState = successor[0]
            nextAction = successor[1]
            nextCost = curCost - heuristic(curState, problem) + successor[2] + heuristic(nextState, problem)
            nextNode = (nextState, nextAction)
            
            #Prioirty of the node is the cumulative cost of the path
            memory.push(nextNode, nextCost)
            nodeDict[nextState] = (curState, nextAction)
            visited.append(nextState)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
