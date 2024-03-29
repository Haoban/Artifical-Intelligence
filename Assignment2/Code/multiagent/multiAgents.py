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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        from util import manhattanDistance

        """
        food = newFood.asList()
        foodDistances = []
        ghostDistances = []
        count = 0 # Tell as how is it worthing to pick this state

        # Calculate distance from every food 
        for item in food:
            foodDistances.append(manhattanDistance(newPos,item))

        for i in foodDistances:
            if i <= 4:
                count += 1
            elif i > 4 and i <= 15:
                count += 0.20
            else:
                count += 0.15
        
        # Calculate distance from every ghost 
        for ghost in successorGameState.getGhostPositions():
            ghostDistances.append(manhattanDistance(ghost,newPos))
        
        for ghost in successorGameState.getGhostPositions():
            
            if manhattanDistance(ghost,newPos) == 0:
                count = 2 - count

            elif manhattanDistance(ghost,newPos) <= 3.5:
                count = 1 - count

        return successorGameState.getScore() + count
        """

        closestghost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])

        if closestghost:
            # The more closestghost is, the more ghost_dist is.
            ghost_dist = -10/closestghost
        else:
            # When the ghost has reached pacman.
            return
        
        ScaredTimes = 0
        for st in newScaredTimes:
            ScaredTimes += st
        
        foodList = newFood.asList()
        if foodList:
            closestfood = min([manhattanDistance(newPos, food) for food in foodList])
        else:
            closestfood = 0

        # consider the number of remained food and large weight to number of food left
        return (-1 * closestfood) + ghost_dist - (100*len(foodList)) + ScaredTimes
        
        #"""
        
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
        """
        "*** YOUR CODE HERE ***"

        def miniMax(gameState,agent,depth):
            result = []

            # Calculate nextAgent
            # final state or reached max depth
            if depth == self.depth or not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState),0

            # all ghosts have finised one round: increase depth
            # Calculate nextAgent
            # Last ghost: nextAgent = pacman. This round has ended.
            if agent == gameState.getNumAgents() - 1:
                depth += 1
                nextAgent = self.index            
                
            # Availiable ghosts. Pick next ghost
            else:
                nextAgent = agent + 1

            # For every successor find minimax value
            for action in gameState.getLegalActions(agent):

                if not result: # If it is the first round
                    nextValue = miniMax(gameState.generateSuccessor(agent,action),nextAgent,depth)

                    # add result with minimax value and action
                    result.append(nextValue[0])
                    result.append(action)
                else:

                    # check if miniMax value is better than the previous one
                    # record previous value. Minimax
                    previousValue = result[0] 
                    nextValue = miniMax(gameState.generateSuccessor(agent,action),nextAgent,depth)

                    # Max agent: Pacman 
                    if agent == self.index:
                        if nextValue[0] > previousValue:
                            result[0] = nextValue[0]
                            result[1] = action

                    # Min agent: Ghost 
                    else:
                        if nextValue[0] < previousValue:
                            result[0] = nextValue[0]
                            result[1] = action
            return result
            
        return miniMax(gameState, self.index,0)[1]
        
            
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def ABPruning(gameState,agent,depth,a,b):
            result = []

            # Calculate nextAgent

            # final state or reached max depth
            if depth == self.depth or not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState),0

            # all ghosts have finised one round: increase depth
            # Calculate nextAgent
            # Last ghost: nextAgent = pacman. This round has ended.
            if agent == gameState.getNumAgents() - 1:
                depth += 1
                nextAgent = self.index 

            # Availiable ghosts. Pick next ghost
            else:
                nextAgent = agent + 1

            # For every successor find minmax value
            for action in gameState.getLegalActions(agent):
                if not result: # If it is the first round
                    nextValue = ABPruning(gameState.generateSuccessor(agent,action),nextAgent,depth,a,b)

                    # add result with minimax value and action
                    result.append(nextValue[0])
                    result.append(action)

                    # initialize a,b (for the first node)
                    if agent == self.index:
                        a = max(result[0],a)
                    else:
                        b = min(result[0],b)
                else:
                    # Check if minMax value is better than the previous one
                    # Chech if we can overpass some nodes                   
                    # It is true               
                    if result[0] > b and agent == self.index:
                        return result

                    if result[0] < a and agent != self.index:
                        return result

                    previousValue = result[0] # record previous value
                    nextValue = ABPruning(gameState.generateSuccessor(agent,action),nextAgent,depth,a,b)

                    # Max agent: Pacman 
                    if agent == self.index:
                        if nextValue[0] > previousValue:
                            result[0] = nextValue[0]
                            result[1] = action
                            # update a 
                            a = max(result[0],a)

                    # Min agent: Ghost 
                    else:
                        if nextValue[0] < previousValue:
                            result[0] = nextValue[0]
                            result[1] = action
                            # update b
                            b = min(result[0],b)
            return result

        # Call ABPruning with initial depth = 0 and -inf and inf(a,b) values
        return ABPruning(gameState,self.index,0,-float("inf"),float("inf"))[1]
        
        util.raiseNotDefined()

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
        def expectiMax(gameState,agent,depth):
            result = []

            # Calculate nextAgent

            # final state or reached max depth
            if depth == self.depth or not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState),0

            # all ghosts have finised one round: increase depth
            # Calculate nextAgent
            # Last ghost: nextAgent = pacman. This round has ended.
            if agent == gameState.getNumAgents() - 1:
                depth += 1
                nextAgent = self.index 

            # Availiable ghosts. Pick next ghost
            else:
                nextAgent = agent + 1

            # For every successor find minimax value
            for action in gameState.getLegalActions(agent):
                if not result: # If it is the first round
                    nextValue = expectiMax(gameState.generateSuccessor(agent,action),nextAgent,depth)
                         
                    # Probability: 1 /(total legal actions) 
                    # all actions have the same probability
                    if(agent != self.index):
                        result.append((1.0 / len(gameState.getLegalActions(agent))) * nextValue[0])
                        result.append(action)                    
                    else:
                        
                        result.append(nextValue[0])
                        result.append(action)
                    
                else:

                    # Check if miniMax value is better than the previous one 
                    previousValue = result[0] # record previous value. 
                    nextValue = expectiMax(gameState.generateSuccessor(agent,action),nextAgent,depth)

                    # Max agent: Pacman
                    if agent == self.index:
                        if nextValue[0] > previousValue:
                            result[0] = nextValue[0]
                            result[1] = action

                    # Min agent: Ghost
                    # find the average value of chance nodes
                    else:
                        result[0] = result[0] + (1.0 / len(gameState.getLegalActions(agent))) * (nextValue[0])
                        result[1] = action
            return result

        # Call expectiMax with initial depth = 0 and get an action
        # Pacman plays first -> agent == 0 or self.index
        
        return expectiMax(gameState,self.index,0)[1]
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

