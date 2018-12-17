import state

def getExpectiAction(startState):
  # pick the successor tha has the highest exp_value
  def max_value(gameState, get_action):
    if gameState.is_terminal():
      print gameState.betstate
      print gameState.get_value()
      return gameState.get_value()
    else:
      v = -10000
      best = None
      for successor in gameState.get_successors():
        action = successor.betstate.actions[-1][-1]
        val_succ = exp_value(successor)
        if val_succ > v:
          v = val_succ
          best = action
    if get_action:
      return best
    else:
      return v

  def exp_value(gameState):
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
          v += 0.1*max_value(successor, False)
        else:
          v += prob*max_value(successor, False)
      return v

  return max_value(startState, True)



      # finish exp value part


