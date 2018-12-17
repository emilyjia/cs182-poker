import state
import random

class Agent:
  def __init__(self, agent_type):
    self.agent_type = agent_type

  def get_action(self, gamestate, depth):
    if self.agent_type == "expectimax":
      return getExpectiAction(gamestate, depth)
    if self.agent_type == "minimax":
      return getMinimaxAction(gamestate, depth)
    if self.agent_type == "random":
      return getRandomAction(gamestate)
    if self.agent_type == "aggressive":
      return getAggressiveAction(gamestate)
    if self.agent_type == "passive":
      return getPassiveAction(gamestate, 0.1)

def getRandomAction(startState):
  next_moves = startState.betstate.next_legal()
  random.shuffle(next_moves)
  return next_moves[0]

def getPassiveAction(startState, fold):
  # returns check or fold (probability of fold is fold)
  if random.uniform(0,1) < fold:
    return ("FOLD", 0)
  else:
    for action in startState.betstate.next_legal():
      if action == ("CHECK", 0):
        return action
  return ("FOLD", 0)

def getAggressiveAction(startState):
  # returns raise or call
  next_moves = startState.betstate.next_legal()
  random.shuffle(next_moves)
  for action in next_moves:
    if action[0] == "RAISE" or action[0] == "BET":
      return action
  for action in next_moves:
    if action[0] == "CALL":
      return action
  return ("FOLD", 0)

def getExpectiAction(startState, maxdepth):
  # pick the successor tha has the highest exp_value
  def max_value(gameState, depth):
    if gameState.is_terminal() or depth == 0:
      # print gameState.betstate
      # print gameState.get_value()
      return gameState.get_value()
    else:
      v = -10000
      best = None
      for successor in gameState.get_successors():
        action = successor.betstate.actions[-1][-1]
        val_succ = exp_value(successor, depth - 1)
        if val_succ > v:
          v = val_succ
          best = action
    return best if depth == maxdepth else v

  def exp_value(gameState, depth):
    if gameState.is_terminal():
      return gameState.get_value()
    else:
      v = 0
      next_legal = gameState.betstate.next_legal()
      prob = 0
      if ("FOLD", 0) in next_legal:
        prob = 0.9/(len(next_legal) - 1)
      else:
        probs = 1.0/(len(next_legal))
      for successor in gameState.get_successors():
        action = successor.betstate.actions[-1][-1]
        if action == "FOLD":
          v += 0.1*max_value(successor, depth)
        else:
          v += prob*max_value(successor, depth)
      return v

  return max_value(startState, maxdepth)


def getMinimaxAction(startState, maxdepth):
  # pick the successor that has the highest exp_value
  def max_value(gameState, depth):
    if gameState.is_terminal() or depth == 0:
      # print gameState.betstate
      # print gameState.get_value()
      return gameState.get_value()
    else:
      v = -10000
      best = None
      for successor in gameState.get_successors():
        action = successor.betstate.actions[-1][-1]
        val_succ = mini_value(successor, depth-1)
        if val_succ > v:
          v = val_succ
          best = action
    return best if depth == maxdepth else v

  def mini_value(gameState, depth):

    if gameState.is_terminal():
        return gameState.get_value()
    else:
        v = 10000
        # don't need to iterate thru actions because don't need to know what
        # the opponent does, just need to know the node value?
        for successor in gameState.get_successors():
          # action = successor.betstate.actions[-1][-1]
          v = min(v,max_value(successor, depth))
        return v

  return max_value(startState, maxdepth)


