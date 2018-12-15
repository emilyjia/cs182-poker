# card object
# hand object
# river object

import random
import collections
import copy

# state should be hand, pot,
def value(state):
  if state.isterminal():
    return montecarlo(state)
  elif state.myturn():
    return maxvalue(state)
  else:
    return expvalue(state)

def maxvalue(state):
  v = -10000
  for successor in state.successors():
    v = max(v, expvalue(successor))
  return v

def expvalue(state):
  v = 0
  for successor in state.successors():
    p = state.probabilities(successor)
    v += p*maxvalue(successor)
  return v


class CardState:
  import montecarlo
  def __init__(self, deck, myhand = [], shared = []):
    self.deck = deck
    self.myhand = myhand
    self.shared = shared

  def deal_hand(self):
    self.myhand = deck.deal_hand()

  def deal_card(self):
    if len(shared) < 3:
      shared = deck.deal_cards(3)
    else:
      shared.append(deck.deal_cards(1))

  def get_probs(self):
    return winprob(myhand, shared)

class BetState:
  def __init__(self, actions, betround, myturn):
    self.actions = actions # actions[i] = [(CHECK, 0), (CHECK, 0)]
    self.betround = betround # which round of betting. 0 =pre, 1 =post, 2 = turn, 3 = river
    self.myturn = myturn # is it my turn
    self.deck = deck
    self.myhand = myhand
    self.shared = shared

  def __repr__(self):
    return "<BetState actions:%s \n betround:%s \n myturn: %s>" % (self.actions, self.betround, str(self.myturn))

  def deal_card(self):
    return (not len(self.actions) == self.betround + 1)

  def isterminal(self):
    # if last action was a fold
    if self.actions[-1] == ("FOLD", 0):
      return True
    lastround = self.actions[3]

    # if we are in last round
    if betround == 3 and len(lastround) >= 2:
      # if we have a call and both people have bet
      if self.actions[3][-1][0] == "CALL":
        return True
      # if we have a check and both people have checked
      if len(lastround) == 2 and self.actions[3][-1][0] == "CHECK":
        return True
    else:
      return False

  def get_pot(self):
    pot = 0
    for x in range(self.betround + 1):
      pot += sum(pair[1] for pair in self.actions[x])
    return pot

  # at most: check, bet, raise, call ==> 4 bets
  def next_legal(self):
    bets = len(self.actions[self.betround])
    legal_bets = []
    if not self.myturn: # opponent always bets the same amount
      legal_bets = [("BET", 10)]
    else:
      legal_bets = [("BET", 5*x + 5) for x in range(20)]
    check_bet = [("CHECK", 0)] + legal_bets

    # no reraising
    if bets == 0:
      return check_bet
    else:
      last_action = self.actions[self.betround][-1]
      if last_action[0] == "CALL" or last_action[0] == "CHECK": # start a new round of betting
        return check_bet
      if last_action[0] == "FOLD":
        return []
      call_fold = [("CALL", last_action[1]), ("FOLD", 0)]
      call_fold_raise = [("CALL", last_action[1]), ("FOLD", 0), ("RAISE", max(self.get_pot()*0.5, 10 + last_action[1]))]
      if bets == 1:
          return call_fold_raise
      if bets == 2:
        if last_action[0] == "BET": # if check/bet, call/fold/raise
          return call_fold_raise
        if last_action[0] == "RAISE": # if bet/raise, call/fold
          return call_fold
      if bets == 3: # check / bet / raise
        if last_action[0] == "RAISE":
          return call_fold

  def get_successors(self):
    successors = []
    # need to determine if a new round of betting has started
    # yes if last action was a call, or check/check
    last_action = self.actions[self.betround][-1][0]
    sec_last_action = None
    if len(self.actions[self.betround]) >= 2:
      sec_last_action = self.actions[self.betround][-2][0]
    betround = None
    if last_action == "CALL" or (last_action == "CHECK" and sec_last_action == "CHECK"):
      for step in self.next_legal():
        actions = copy.deepcopy(self.actions)
        actions.append([step])
        successors.append(BetState(actions, self.betround + 1, not self.myturn))
    else:
      for step in self.next_legal():
        actions = copy.deepcopy(self.actions)
        actions[-1].append(step)
        successors.append(BetState(actions, self.betround, not self.myturn))
    return successors












