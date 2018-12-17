import random
import collections
import copy

# a gamestate is a cardstate and betstate
class GameState:
  def __init__(self, cardstate, betstate):
    self.cardstate = cardstate
    self.betstate = betstate

  # deals card if betstate
  def get_successors():
    successors = []
    for successor in self.betstate.get_successors():
      cardstatecopy = copy.deepcopy(cardstate)
      if successor.deal_card():
        cardstatecopy.deal_card()
      successors.append(GameState(cardstate, gamestate))
    return successors

# this is wrong
  def get_value():
    if betstate.showdown():
      return (betstate.get_pot()*cardstate.get_probs()[0] + 0.5*betstate.get_pot()*cardstate.get_probs()[0] - betstate.mybet)
    elif betstate.isterminal():
      if betstate.myturn:
        return betstate.get_pot() - betstate.mybet
      else:
        return -betstate.mybet

  def is_terminal():
    return betstate.isterminal()


# keeps track of what cards are dealt and when they should be dealt

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

  def get_probs(self): # gives probability of win
    return winprob(myhand, shared)

# keeps track of bets

class BetState:
  def __init__(self, actions, betround, myturn, mybet):
    self.actions = actions # actions[i] = [(CHECK, 0), (CHECK, 0)]
    self.betround = betround # which round of betting. 0 =pre, 1 =post, 2 = turn, 3 = river
    self.myturn = myturn # is it my turn
    self.mybet = mybet # how much of the pot is mine

  def __repr__(self):
    return "<BetState actions:%s \n betround:%s \n myturn: %s \n mybet: %s>" % (self.actions, self.betround, str(self.myturn), self.mybet)

  def deal_card(self):
    return (not len(self.actions) == self.betround + 1)

  def showdown(self):
  # if we are in last round
  lastround = self.actions[3]
  if betround == 3 and len(lastround) >= 2:
    # if we have a call and both people have bet
    if self.actions[3][-1][0] == "CALL":
      return True
    # if we have a check and both people have checked
    if len(lastround) == 2 and self.actions[3][-1][0] == "CHECK":
      return True

  def isterminal(self):
    if self.showdown():
      return True
    # if last action was a fold
    if len(self.actions) > 0 and self.actions[-1][-1] == ("FOLD", 0):
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
        newmybet = None
        if self.myturn:
          newmybet = self.mybet + step[1]
        else:
          newmybet = step[1]
        successors.append(BetState(actions, self.betround + 1, not self.myturn, newmybet))
    else:
      for step in self.next_legal():
        actions = copy.deepcopy(self.actions)
        actions[-1].append(step)
        if self.myturn:
          newmybet = self.mybet + step[1]
        else:
          newmybet = step[1]
        successors.append(BetState(actions, self.betround, not self.myturn, newmybet))
    return successors












