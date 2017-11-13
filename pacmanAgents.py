# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from pacman import Directions
from game import Agent
from heuristics import scoreEvaluation
import random

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        fringe = [] # This contains nodes to be expanded
        leaf_node = [] # This list contains all the leaf nodes
        directions_from_start_state = state.getLegalPacmanActions() #initial directions 
        initial_successors = [(state.generatePacmanSuccessor(direction), direction)for direction in directions_from_start_state] # list of initial successors
        for node in initial_successors: # iterating over initial successors
            fringe.append(node) # append to fringe to be explored further

        while fringe: # loop till fringe is not empty
                current_node = fringe.pop(0)
                if current_node[0]==None:
                    continue
                legal = current_node[0].getLegalPacmanActions()
                successors = []
                if legal: # if only action is legal
                    for action in legal:
                        current_state = current_node[0].generatePacmanSuccessor(action)
                        if current_state!=None and action is not None: # sometimes action is equating to None
                            successors.append((current_state, current_node[1])) # appending the successor and the action taken to get to the suv

                if len(successors) == 0 or current_node[0].isWin() or current_node[0].isLose():
                    leaf_node.append(current_node)

                    
                else:
                    for succ_node in successors:
                        fringe.append(succ_node)
                        
       
        
        # get best choice
        max_score = -10000000
        if leaf_node:
            for node in leaf_node:
                if node[0]!=None and node[1]!=None and scoreEvaluation(node[0])>max_score:
                    max_score  = scoreEvaluation(node[0])  
                    result = node[1]
            return result
            
            



        


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        fringe = [] # This contains nodes to be expanded
        leaf_node = [] # This list contains all the leaf nodes
        explored=[]
        directions_from_start_state = state.getLegalPacmanActions() #initial directions 
        initial_successors = [(state.generatePacmanSuccessor(direction), direction)for direction in directions_from_start_state] # list of initial successors
        for node in initial_successors: # iterating over initial successors
            fringe.append(node) # append to fringe to be explored further

        while fringe: # loop till fringe is not empty
                current_node = fringe.pop()
                explored.append(current_node[0])
                if current_node[0]==None:
                    continue
                legal = current_node[0].getLegalPacmanActions()
                successors = []
                if legal: # if only action is legal
                    for action in legal:
                        current_state = current_node[0].generatePacmanSuccessor(action)
                        explored.append(current_state)
                        if current_state!=None and action is not None: # sometimes action is equating to None
                            successors.append((current_state, current_node[1])) # appending the successor and the action taken to get to the suv

                if len(successors) == 0 or current_node[0].isWin() or current_node[0].isLose():
                    leaf_node.append(current_node)

                    
                else:
                    for succ_node in successors :
                        fringe.append(succ_node)

                        
       
        
        # get best choice
        max_score = -10000000
        if leaf_node:
            for node in leaf_node:
                if node[0]!=None and node[1]!=None and scoreEvaluation(node[0])>max_score:
                    max_score  = scoreEvaluation(node[0])  
                    result = node[1]
            return result

       

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        none_flag = 0  # handles None type
        node_depth = 1# used to find the depth of each node
        legal = state.getLegalPacmanActions()# gets all legal actions
        root_score_eval = scoreEvaluation(state)
        fringe = []#list of successors
        for action in legal:
            current_state = state.generatePacmanSuccessor(action)
            cost = node_depth - (scoreEvaluation(current_state) - root_score_eval) # A-star hueristic
            fringe.append((cost, current_state, action, node_depth)) # append into successor list
        while (fringe):#iterate over successor
            if (none_flag == 1):
                break
            fringe.sort()
            cost, cur_state, action, node_depth = fringe.pop(0)
            if (cur_state.isWin()):
                return action
            legal = cur_state.getLegalPacmanActions()
            if legal:
                for next_action in legal:
                    child_node = cur_state.generatePacmanSuccessor(next_action)
                    if (child_node == None):
                        none_flag = 1
                        break
                    cost = (node_depth + 1) - (scoreEvaluation(child_node) - root_score_eval)
                    fringe.append((cost, child_node, action, node_depth + 1))

        bestAction_pseudo = Directions.STOP
        scored = [(scoreEvaluation(state), n_depth, action) for cost, state, action, n_depth in fringe]
        bestScore = max(scored)[0]
        new_scored = [(score, n_depth, action) for score, n_depth, action in scored if score == bestScore]
        if(new_scored!=None):
            bestAction_pseudo = min(new_scored, key=lambda item: item[1])[2]  

        return bestAction_pseudo

