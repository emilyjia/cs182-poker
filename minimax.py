import state

def getMinimaxAction(startState, maxdepth):
  # pick the successor that has the highest exp_value
  def max_value(gameState, depth):
    if gameState.is_terminal() or depth == 0:
      print gameState.betstate
      print gameState.get_value()
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
