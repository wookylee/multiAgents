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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        currentPos = currentGameState.getPacmanPosition()
        currentFood = currentGameState.getFood();
        "currentGhostPos = currentGameState.getGhostPosition()"
        "futureGhostPos = successorGameState.getGhostPosition()"
        foodArray = newFood.asList()
        foodscore = 0;
        for foodPos in foodArray:
            if len(foodArray) == 0:
                foodscore = 1
            else:
                foodscore = (1.0 / (util.manhattanDistance(newPos,foodPos)))

        ghostscore  = 0
        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            if (util.manhattanDistance(newPos, ghostPos)) < 2:
                ghostscore = -100


        return (successorGameState.getScore() - currentGameState.getScore()) + foodscore + ghostscore

        "return successorGameState.getScore()"

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
        """
        
        return self.getnextaction       
        """
        return self.MinimaxSearch(gameState, 1, 0)

        util.raiseNotDefined()

    def MinimaxSearch(self, gameState, curDepth, agentIndex):
        if gameState.isWin() or gameState.isLose() or curDepth > self.depth:
            return self.evaluationFunction(gameState)

            "minimax algorithm"

        legalMoves = [action for action in gameState.getLegalActions(agentIndex)]

        nextAgent = agentIndex + 1
        nextDepth = curDepth
        if nextAgent >= gameState.getNumAgents():
            nextAgent = 0
            nextDepth = nextDepth + 1

        results = [self.MinimaxSearch(gameState.generateSuccessor(agentIndex, action), nextDepth, nextAgent) for action in legalMoves]

        if agentIndex == 0 and curDepth == 1:
            return legalMoves[random.choice([index for index in range(len(results)) if results[index] == max(results) ])]
        if agentIndex == 0:
            return max(results)
        else:
            return min(results)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"


        return self.AlphaBeta(gameState, 0, 0, float('-inf'), float('inf'))


        util.raiseNotDefined()

    def AlphaBeta(self, gameState, curDepth, agentIndex, alpha, beta):

        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            curDepth = curDepth + 1

        if curDepth == self.depth:
            return self.evaluationFunction(gameState)

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)



        if agentIndex == 0:
            v = float('-inf')
            for legalMoves in gameState.getLegalActions(agentIndex):

                temp = self.AlphaBeta(gameState.generateSuccessor(agentIndex, legalMoves), curDepth, agentIndex + 1, alpha, beta)
                if temp > v:
                    v = temp
                    actVal = legalMoves
                if v > beta:
                    return v

                alpha = max(alpha, v)

            if curDepth == 0:
                return actVal
            else:
                return v
        else:
            v = float('inf')
            for legalMoves in gameState.getLegalActions(agentIndex):

                temp = self.AlphaBeta(gameState.generateSuccessor(agentIndex, legalMoves), curDepth, agentIndex + 1, alpha, beta)
                if temp < v:
                    v = temp
                    actVal = legalMoves
                if v < alpha:
                    return v
                beta = min(beta, v)

            return v


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
