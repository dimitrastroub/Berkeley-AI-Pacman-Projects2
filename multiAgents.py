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
        FoodDistance = []
        GhostDistance = []
        current_score = successorGameState.getScore()

        #count the distances betwwen Ghosts - pacman
        foodList = newFood.asList()
        for eachFood in foodList: 
            count = util.manhattanDistance(eachFood,newPos)
            FoodDistance.append(count)

        #count the distances betwwen Ghosts - pacman
        GhostList = successorGameState.getGhostPositions()
        for eachGhost in GhostList:
            count = util.manhattanDistance(eachGhost,newPos)
            GhostDistance.append(count)

        def reciprocal( alist ,value):
            item = 0
            for each in alist:
                if each > value:
                    item = item + 1.0/each
            return item
        #find the reciprocal value from the arrays GhostsDistances and FoodFistances
        ImportantFoodValue = reciprocal(FoodDistance,0)
        ImportantGhostValue = reciprocal(GhostDistance,1)
        final_score = 3*ImportantFoodValue + 2*ImportantGhostValue + current_score 
        return final_score
        #return successorGameState.getScore()

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
        def decision(gameState, agentId, gameDeep):
        
            def maxValue(array , gameState, agentId, gameDeep):
                movement = None
                v = -float("inf")
                array.append(movement)
                array.append(v)
                listOfActions = gameState.getLegalActions(agentId)
                if listOfActions:
                    for action in listOfActions:
                        nextState = gameState.generateSuccessor(agentId, action)
                        nextAgent = agentId + 1
                        nextValue = decision(nextState, nextAgent ,gameDeep)
                        testing = nextValue[1]
                        if testing > array[1]:
                            array[1] = nextValue[1]
                            array[0] = action
                return array
                
            def minValue(array ,gameState, agentId, gameDeep):
                movement = None
                v = float("inf")
                array.append(movement)
                array.append(v)
                listOfActions = gameState.getLegalActions(agentId)
                if listOfActions:
                    for action in listOfActions:
                        nextState = gameState.generateSuccessor(agentId, action)
                        nextAgent = agentId + 1
                        nextValue = decision(nextState, nextAgent ,gameDeep)
                        testing = nextValue[1]
                        if testing < array[1]:
                            array[1] = nextValue[1]
                            array[0] = action
                return array

            numberAgents = gameState.getNumAgents()
            maxArray = [] 
            minArray = []
            prevDeep = gameDeep
            if agentId == numberAgents:  #if all ghost have played
                gameDeep += 1 # increase the deep by one
            if prevDeep!= gameDeep: # if the deep has been increases, pacman plays! 
                agentId = self.index
            if  gameState.isWin() or gameState.isLose():
                value = self.evaluationFunction(gameState)
                return [None,value]
            if gameDeep==self.depth:
                value = self.evaluationFunction(gameState)
                return [None,value]
            if agentId == 0:
                return maxValue( maxArray,gameState, agentId ,gameDeep)
            else:
                if agentId >=1:
                    return minValue(minArray,gameState, agentId ,gameDeep)
        
        startState = gameState
        pacman = self.index
        startDeep = 0
        return decision(startState, pacman, startDeep)[0]
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
        def decision(gameState, agentId, gameDeep ,alpha ,beta):
        
            def maxValue(array , gameState,alpha ,beta):
                movement = None
                v = -float("inf")
                array.append(movement)
                array.append(v)
                listOfActions = gameState.getLegalActions(agentId)
                if listOfActions:
                    for action in listOfActions:
                        nextState = gameState.generateSuccessor(agentId, action)
                        nextAgent = agentId + 1
                        nextValue = decision(nextState, nextAgent ,gameDeep,alpha, beta)
                        testing = nextValue[1]
                        if testing > array[1]:
                            array[1] = nextValue[1]
                            array[0] = action
                        if array[1] > beta:
                            return array
                        alpha = max(alpha , array[1])
                return array
                
            def minValue(array ,gameState ,alpha , beta):
                movement = None
                v = float("inf")
                array.append(movement)
                array.append(v)
                listOfActions = gameState.getLegalActions(agentId)
                if listOfActions:
                    for action in listOfActions:
                        nextState = gameState.generateSuccessor(agentId, action)
                        nextAgent = agentId + 1
                        nextValue = decision(nextState,nextAgent , gameDeep ,alpha ,beta)
                        testing = nextValue[1]
                        if testing < array[1]:
                            array[1] = nextValue[1]
                            array[0] = action
                        if array[1] < alpha:
                            return array
                        beta = min(beta , array[1])
                return array

            numberAgents = gameState.getNumAgents()
            maxArray = [] 
            minArray = []
            prevDeep = gameDeep
            if agentId == numberAgents:  #if all ghost have played
                gameDeep += 1 # increase the deep by one
            if prevDeep!= gameDeep: # if the deep has been increases, pacman plays! 
                agentId = self.index
            if  gameState.isWin() or gameState.isLose():
                value = self.evaluationFunction(gameState)
                return [None,value]
            if gameDeep==self.depth:
                value = self.evaluationFunction(gameState)
                return [None,value]
            if agentId == 0:
                return maxValue( maxArray,gameState,alpha ,beta)
            else:
                if agentId >=1:
                    return minValue(minArray,gameState,alpha , beta)
        
        startState = gameState
        pacman = self.index
        startDeep = 0
        alpha = -float("inf")
        beta= float("inf")
        return decision(startState, pacman, startDeep, alpha ,beta)[0]
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
        def decision(gameState, agentId, gameDeep):
        
            def maxValue(array , gameState, agentId, gameDeep):
                movement = None
                v = -float("inf")
                array.append(movement)
                array.append(v)
                listOfActions = gameState.getLegalActions(agentId)
                if listOfActions:
                    for action in listOfActions:
                        nextState = gameState.generateSuccessor(agentId, action)
                        nextAgent = agentId + 1
                        nextValue = decision(nextState, nextAgent ,gameDeep)
                        testing = nextValue[1]
                        if testing > array[1]:
                            array[1] = nextValue[1]
                            array[0] = action
                return array
                
            def expValue(array ,gameState, agentId, gameDeep):
                movement = None
                v = 0
                array.append(movement)
                array.append(v)
                listOfActions = gameState.getLegalActions(agentId)
                length = len(listOfActions)
                if listOfActions:
                    for action in listOfActions:
                        if length != 0:
                            probability = 1.0/length
                        else:
                            probability = float("inf")
                        nextState = gameState.generateSuccessor(agentId, action)
                        nextAgent = agentId + 1
                        nextValue = decision(nextState, nextAgent ,gameDeep)
                        testing = nextValue[1]
                        v= v + (testing* probability)
                        array[0] = action
                        array[1] = v
                return array

            numberAgents = gameState.getNumAgents()
            maxArray = [] 
            minArray = []
            prevDeep = gameDeep
            if agentId == numberAgents:  #if all ghost have played
                gameDeep += 1 # increase the deep by one
            if prevDeep!= gameDeep: # if the deep has been increases, pacman plays! 
                agentId = self.index
            if  gameState.isWin() or gameState.isLose():
                value = self.evaluationFunction(gameState)
                return [None,value]
            if gameDeep==self.depth:
                value = self.evaluationFunction(gameState)
                return [None,value]
            if agentId == 0:
                return maxValue( maxArray,gameState, agentId ,gameDeep)
            else:
                if agentId >=1:
                    return expValue(minArray,gameState, agentId ,gameDeep)
        
        startState = gameState
        pacman = self.index
        startDeep = 0
        return decision(startState, pacman, startDeep)[0]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    FoodDistance = []
    GhostDistance = []
    current_score = currentGameState.getScore()

    #count the distances betwwen Ghosts - pacman
    foodList = newFood.asList()
    for eachFood in foodList: 
        count = util.manhattanDistance(eachFood,newPos)
        FoodDistance.append(count)

    #count the distances betwwen Ghosts - pacman
    GhostList = currentGameState.getGhostPositions()
    for eachGhost in GhostList:
        count = util.manhattanDistance(eachGhost,newPos)
        GhostDistance.append(count)

    def reciprocal( alist ,value):
        item = 0
        for each in alist:
            if each > value:
                item = item + 1.0/each
        return item
    #find the reciprocal value from the arrays GhostsDistances and FoodFistances
    ImportantFoodValue = reciprocal(FoodDistance,0)
    ImportantGhostValue = reciprocal(GhostDistance,1)
    final_score = ImportantFoodValue + ImportantGhostValue + current_score 
    return final_score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

