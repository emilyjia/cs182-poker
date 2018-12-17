import state

def getExpectiAction(self, gameState):
  # pick the successor tha has the highest exp_value
  def max_value(gameState):
    if gameState.is_terminal():
      return gameState.get_value()
    else:
      v = -10000
      for successor in gameState.get_successors():
        action = successor.betstate.actions[-1][-1]
        val_succ = exp_value(successor)
        if val_succ > v:
          v = val_succ
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
          v += 0.1*max_value(successor)
        else:
          v += prob*max_value(successor)
      return v


      # finish exp value part


