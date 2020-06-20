# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import numpy as np

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newCapsules = successorGameState.getCapsules()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        gameScore = successorGameState.getScore()
        
        #Sum of the whole distances with the ghost
        for newGhostState in newGhostStates:
            ghostPosition = newGhostState.getPosition()
            ghost_distance = abs(newPos[0] - ghostPosition[0]) + abs(newPos[1] - ghostPosition[1])

        #Sum of the whole distances with the food
        food_distance = 0
        gamma = .9
        for i in range(newFood.width):
            for j in range(newFood.height):
                if newFood[i][j] == True:
                    food_distance += gamma * (abs(newPos[0] - i) + abs(newPos[1] - j))
                    gamma *= 0.9
                    
        capsule_distance = 0
        for capsule in newCapsules:
            capsule_distance += (abs(newPos[0] - capsule[0]) + abs(newPos[1] - capsule[1]))
        
        score = 0.8* gameScore + np.log(ghost_distance + 0.001) - 0.15 * food_distance - 0.5 * capsule_distance

        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        numAgents = gameState.getNumAgents()
        
        maxValue, action = self.getMaxValue(0, numAgents, gameState, depth = 1, max_depth = self.depth)

        return action
    
    def getMaxValue(self, agentIndex, numAgents, gameState, depth, max_depth):
        values = {}
        max_value = -99999
        max_action = 'Stop'
        
        legalActions = gameState.getLegalActions(agentIndex)
        
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            
            #Terminal State
            if (successorState.isWin() == True) | (successorState.isLose() == True):
                values[action] = self.evaluationFunction(successorState)
                
            else:
                values[action] = self.getMinValue(agentIndex + 1, numAgents, successorState, depth, max_depth)[0]

        for action in values:
            value = values[action]
            if value > max_value:
                max_value = value
                max_action = action
            
        return max_value, max_action
    
    def getMinValue(self, agentIndex, numAgents, gameState, depth, max_depth):
        values = {}
        min_value  = 99999
        min_action = 'Stop'
        
        legalActions = gameState.getLegalActions(agentIndex)
        
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            
            #Terminal State
            if (successorState.isWin() == True) | (successorState.isLose() == True):
                values[action] = self.evaluationFunction(successorState)
                
            else:
                # Next node is Max node
                if (agentIndex + 1 >= numAgents) & (depth < max_depth):
                    values[action] = self.getMaxValue(0, numAgents, successorState, depth + 1, max_depth)[0]
                
                # Max Depth, Terminate
                elif (agentIndex + 1 == numAgents) & (depth == max_depth):
                    values[action] = self.evaluationFunction(successorState)
                
                # Next node is Min node
                else:
                    values[action] = self.getMinValue(agentIndex + 1, numAgents, successorState, depth, max_depth)[0]    
        
        for action in values:
            value = values[action]
            if value < min_value:
                min_value = value
                min_action = action
            
        return min_value, min_action
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #Alpha: Max's best option on path to root
        #Beta : Min's best option on path to root
        
        numAgents = gameState.getNumAgents()
        
        maxValue, action = self.getMaxValue(0, numAgents, gameState, depth = 1, max_depth = self.depth, alpha = -99999, beta = 99999)

        return action
    
    def getMaxValue(self, agentIndex, numAgents, gameState, depth, max_depth, alpha, beta):
        values = {}
        max_value = -99999
        max_action = 'Stop'
        
        legalActions = gameState.getLegalActions(agentIndex)
        
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            
            #Terminal State
            if (successorState.isWin() == True) | (successorState.isLose() == True):
                values[action] = self.evaluationFunction(successorState)
                
            else:
                values[action] = self.getMinValue(agentIndex + 1, numAgents, successorState, depth, max_depth, alpha, beta)[0]
            
            # Pruning, if the value is larger than beta Min node will not choose this node eventually
            if values[action] > beta:
                return values[action], action
            
            # Update the Max node's best possible value
            if values[action] > alpha:
                alpha = values[action]

        for action in values:
            value = values[action]
            if value > max_value:
                max_value = value
                max_action = action
            
        return max_value, max_action
    
    def getMinValue(self, agentIndex, numAgents, gameState, depth, max_depth, alpha, beta):
        values = {}
        min_value  = 99999
        min_action = 'Stop'
        
        legalActions = gameState.getLegalActions(agentIndex)
        
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            
            #Terminal State
            if (successorState.isWin() == True) | (successorState.isLose() == True):
                values[action] = self.evaluationFunction(successorState)
                
            else:
                # Next node is Max node
                if (agentIndex + 1 >= numAgents) & (depth < max_depth):
                    values[action] = self.getMaxValue(0, numAgents, successorState, depth + 1, max_depth, alpha, beta)[0]
                
                # Max Depth, Terminate
                elif (agentIndex + 1 == numAgents) & (depth == max_depth):
                    values[action] = self.evaluationFunction(successorState)
                
                # Next node is Min node
                else:
                    values[action] = self.getMinValue(agentIndex + 1, numAgents, successorState, depth, max_depth, alpha, beta)[0]    
            
            # Pruning, if the value is smaller than beta Max node will not choose this node eventually
            if values[action] < alpha:
                return values[action], action
            
            # Update the Min node's best possible value
            if values[action] < beta:
                beta = values[action]
        
        for action in values:
            value = values[action]
            if value < min_value:
                min_value = value
                min_action = action
            
        return min_value, min_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        
        maxValue, action = self.getMaxValue(0, numAgents, gameState, depth = 1, max_depth = self.depth)

        return action
    
    def getMaxValue(self, agentIndex, numAgents, gameState, depth, max_depth):
        values = {}
        max_value = -99999
        max_action = 'Stop'
        
        legalActions = gameState.getLegalActions(agentIndex)
        
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            
            #Terminal State
            if (successorState.isWin() == True) | (successorState.isLose() == True):
                values[action] = self.evaluationFunction(successorState)
                
            else:
                values[action] = self.getExpValue(agentIndex + 1, numAgents, successorState, depth, max_depth)

        for action in values:
            value = values[action]
            if value > max_value:
                max_value = value
                max_action = action
            
        return max_value, max_action
    
    def getExpValue(self, agentIndex, numAgents, gameState, depth, max_depth):
        values = {}
        exp_value  = 0
        prob = 1
        
        legalActions = gameState.getLegalActions(agentIndex)
        
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            
            #Terminal State
            if (successorState.isWin() == True) | (successorState.isLose() == True):
                values[action] = self.evaluationFunction(successorState)
                
            else:
                # Next node is Max node
                if (agentIndex + 1 >= numAgents) & (depth < max_depth):
                    values[action] = self.getMaxValue(0, numAgents, successorState, depth + 1, max_depth)[0]
                
                # Max Depth, Terminate
                elif (agentIndex + 1 == numAgents) & (depth == max_depth):
                    values[action] = self.evaluationFunction(successorState)
                
                # Next node is Min node
                else:
                    values[action] = self.getExpValue(agentIndex + 1, numAgents, successorState, depth, max_depth)
        
        for action in values:
            # prob = probability of the action, it's all equal in the pacman
            exp_value += prob * values[action]
            
        return exp_value

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    Pos  = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    Capsules = currentGameState.getCapsules()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

    gameScore = currentGameState.getScore()
        
    #Sum of the whole distances with the ghost
    ghost_distance = 0
    for g in range(len(GhostStates)):
        GhostState = GhostStates[g]
        ghostPosition = GhostState.getPosition()
        ghost_distance = abs(Pos[0] - ghostPosition[0]) + abs(Pos[1] - ghostPosition[1])
        scaredTime = ScaredTimes[g]
        
        if ghost_distance > 3:
            ghost_distance = 4
        
    #Sum of the whole distances with the food
    food_distance = 0
    gamma = .9
    for i in range(Food.width):
        for j in range(Food.height):
            if Food[i][j] == True:
                food_distance += gamma * (abs(Pos[0] - i) + abs(Pos[1] - j))
                gamma *= 0.9
                
    capsule_distance = 0
    for capsule in Capsules:
        capsule_distance += (abs(Pos[0] - capsule[0]) + abs(Pos[1] - capsule[1]))
        
    score = 0.4* gameScore + 0.2 * ghost_distance - 0.2 * food_distance - 0.3 * capsule_distance

    return score

# Abbreviation
better = betterEvaluationFunction
