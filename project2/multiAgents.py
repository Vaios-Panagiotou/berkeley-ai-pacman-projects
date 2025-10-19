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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #get the current game score
        score = successorGameState.getScore()

        #calculate the distance to the nearest food 
        foodDistances = [util.manhattanDistance(newPos, food) for food in newFood.asList()]
        nearestFoodDistance = min(foodDistances) if foodDistances else 0

        #check if a ghost is too close to Pacman
        isGhostTooClose = any(util.manhattanDistance(newPos, ghost.getPosition()) < 2 for ghost in newGhostStates)

        #consider the scared timer of the ghosts
        scaredGhostTimers = [timer for timer in newScaredTimes if timer > 0]
        scaredGhostBonus = max(scaredGhostTimers) if scaredGhostTimers else 0

        #combine factors to create a evaluation function
        evaluation = score + (1 / (nearestFoodDistance + 1)) - (10 if isGhostTooClose else 0) + scaredGhostBonus

        return evaluation

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        """
        def maxvalue(state, depth):#maximizing player
            if state.isWin() or state.isLose() or depth == 0:#if the game is in a terminal state or reached the depth limit, return the evaluation
                return self.evaluationFunction(state)
            
            value = float("-inf")
            legalActions = state.getLegalActions(0)  #pacmans actions
            for action in legalActions:#loop through legal actions for the current maximizing player
                successor = state.generateSuccessor(0, action)
                value = max(value, minvalue(successor, depth, 1))#using minimization if the last agent  call minimum value for the next level
            return value

        def minvalue(state, depth, agentIndex):#minimizing player
            if state.isWin() or state.isLose() or depth == 0:#if the game is in a terminal state or reached the depth limit, return the evaluation
                return self.evaluationFunction(state)
            
            value = float("inf")
            legalActions = state.getLegalActions(agentIndex)
            for action in legalActions:#loop through legal actions for the current minimizing player
                successor = state.generateSuccessor(agentIndex, action)
                if agentIndex == state.getNumAgents() - 1:  #last ghost
                    value = min(value, maxvalue(successor, depth - 1))#using maximazation if the last agent  call maximum value for the next level
                else:
                    value = min(value, minvalue(successor, depth, agentIndex + 1))#call minimum value for the next minimizing player
            return value

        legalActions = gameState.getLegalActions(0)  #pacmans actions
        bestAction = None
        bestValue = float("-inf")

        for action in legalActions:#loop through legal actions for the current maximizing player
            successor = gameState.generateSuccessor(0, action)#generate the successor state after taking action 'a'
            value = minvalue(successor, self.depth, 1)
            if value > bestValue:#if the value is better than the current best update the best value and action
                bestValue = value
                bestAction = action

        return bestAction



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        
        """
        DISCLAIMER :
        In the functions, _ means the value is not used, but we need to return it
        """
        def maxvalue(state, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth == 0:
                #if the game is in a terminal state or reached the depth limit, return the evaluation
                return self.evaluationFunction(state), None

            v = float("-inf")
            action = None
            for a in state.getLegalActions(0):
                #generating the successor state after taking action 'a'
                successor = state.generateSuccessor(0, a)
                #using minimization recursively get the value from the next level 
                successor_value, _ = minvalue(successor, depth, 1, alpha, beta)
                if successor_value > v:
                    v = successor_value
                    action = a
                if v > beta:
                    return v, action
                alpha = max(alpha, v)
            return v, action

        def minvalue(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or depth == 0:
                #if the game is in a terminal state or reached the depth limit, return the evaluation
                return self.evaluationFunction(state), None

            v = float("inf")
            action = None
            #loop through legal actions for the current minimizing player
            for a in state.getLegalActions(agentIndex):
                #generate the successor state after taking action 'a'
                successor = state.generateSuccessor(agentIndex, a)
                if agentIndex == state.getNumAgents() - 1:
                    #using maximazation if the last agent, call maxValue for the next level 
                    successor_value, _ = maxvalue(successor, depth - 1, alpha, beta)
                else:
                    #calling minValue for the next minimizing player
                    successor_value, _ = minvalue(successor, depth, agentIndex + 1, alpha, beta)
                if successor_value < v:
                    v = successor_value
                    action = a
                if v < alpha:
                    return v, action
                beta = min(beta, v)
            return v, action

        #initialize the search from the top level (maximization)
        _, bestAction = maxvalue(gameState, self.depth, float("-inf"), float("inf"))
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """
    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        """
        def maxValue(state, depth):
            if state.isWin() or state.isLose() or depth == 0:#if the game is in a terminal state or reached the depth limit  return the evaluation
                return self.evaluationFunction(state)

            value = float("-inf")
            legalActions = state.getLegalActions(0)  #pacmans actions
            for action in legalActions:#loop through legal actions for the current maximizing player
                successor = state.generateSuccessor(0, action)
                value = max(value, expValue(successor, depth, 1))  #calling expvalue for the next minimizing player
            return value

        def expValue(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)

            value = 0
            legalActions = state.getLegalActions(agentIndex)#get legal actions for the current minimizing player
            numActions = len(legalActions)

            for action in legalActions:#loop through legal actions for the current minimizing player
                successor = state.generateSuccessor(agentIndex, action)

                if agentIndex == state.getNumAgents() - 1:
                    #last ghost, call maxvalue for the next level
                    value += maxValue(successor, depth - 1)
                else:
                    #call expvalue for the next minimizing player
                    value += expValue(successor, depth, agentIndex + 1)

            return value / numActions  #average over legal actions

       
        legalActions = gameState.getLegalActions(0)  #pacmans actions
        bestAction = None
        bestValue = float("-inf")

        for action in legalActions:#loop through legal actions for the current maximizing player
            successor = gameState.generateSuccessor(0, action)#generate the successor state after taking action 'a'
            value = expValue(successor, self.depth, 1)
            if value > bestValue:#if the value is better than the current best update the best value and action
                bestValue = value
                bestAction = action

        return bestAction

def better_evaluation_function(currentGameState):
    total_score = 0
    pacman_location = currentGameState.getPacmanPosition()
    food_locations = currentGameState.getFood().asList()
    
    # Increase score based on proximity to closest food
    if food_locations:
        total_score += 5 / min(manhattanDistance(pacman_location, food) for food in food_locations)
        # Increase score based on remaining food count
        total_score += 2 / len(food_locations)

    # Decrease score if a ghost is too close
    if any(manhattanDistance(pacman_location, ghost) < 2 for ghost in currentGameState.getGhostPositions()):
        total_score -= 500

    # Increase score based on scared ghost durations
    total_score += 5 * sum(ghost_state.scaredTimer for ghost_state in currentGameState.getGhostStates())

    # Return total score plus a portion of the current game score
    return total_score + 50 * currentGameState.getScore()



better = better_evaluation_function
