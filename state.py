import random
import collections
import copy
from montecarlo import *

# a gamestate is a cardstate and betstate
class GameState:
  def __init__(self, cardstate, betstate):
    self.cardstate = cardstate
    self.betstate = betstate

  # deals card if betstate
  def get_successors(self, next_move = []):
    successors = []
    if next_move == []:
      bet_successors = self.betstate.get_successors()
    else:
      bet_successors = self.betstate.get_successors([next_move])
    for successor in bet_successors:
      cardstatecopy = copy.deepcopy(self.cardstate)
      if successor.deal_card():
        cardstatecopy.deal_card()
      successors.append(GameState(cardstatecopy, successor))
    return successors

  def get_value(self):
    if self.betstate.showdown() or not self.betstate.isterminal():
      return ((self.betstate.get_pot() + 10)*self.cardstate.get_probs()[0] + 0.5*(self.betstate.get_pot())*self.cardstate.get_probs()[1] - self.betstate.mybet)
    elif self.betstate.isterminal():
      if self.betstate.myturn:
        return self.betstate.get_pot() - self.betstate.mybet + 10
      else:
        return -self.betstate.mybet - 10

  def is_terminal(self):
    return self.betstate.isterminal()


# keeps track of what cards are dealt and when they should be dealt

class CardState:
  import montecarlo
  def __init__(self, deck, myhand = [], shared = []):
    self.deck = deck
    self.myhand = myhand
    self.shared = shared

  def deal_hand(self):
    self.myhand = self.deck.deal_hand()

  def deal_card(self):
    if len(self.shared) < 3:
      self.shared = self.deck.deal_cards(3)
    elif len(self.shared) < 5:
      self.shared += self.deck.deal_cards(1)

  def get_probs(self): # gives probability of win
    return winprob(self.myhand, self. shared)

# keeps track of bets

class BetState:
  def __init__(self, actions = [], betround = 0, myturn = True, mybet = 0):
    self.actions = actions # actions[i] = [(CHECK, 0), (CHECK, 0)]
    self.betround = betround # which round of betting. 0 =pre, 1 =post, 2 = turn, 3 = river
    self.myturn = myturn # is it my turn
    self.mybet = mybet # how much of the pot is mine

  def __repr__(self):
    return "<BetState actions:%s \n betround:%s \n myturn: %s \n mybet: %s>" % (self.actions, self.betround, str(self.myturn), self.mybet)

  def deal_card(self):
    if len(self.actions) > 0:
      if len(self.actions[-1]) >= 2:
        return self.actions[-1][-1][0] == "CALL" or (self.actions[-1][-1][0] == "CHECK" and self.actions[-1][-2][0] == "CHECK")


  def showdown(self):
    # if we are in last round
    if self.betround == 3:
      lastround = self.actions[3]
      if len(lastround) >= 2:
        # if we have a call and both people have bet
        if self.actions[3][-1][0] == "CALL":
          return True
        # if we have a check and both people have checked
        if len(lastround) == 2 and self.actions[3][-1][0] == "CHECK":
          return True
      else:
        return False

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

    legal_bets = []
    if not self.myturn: # opponent always bets the same amount
      legal_bets = [("BET", 10)]
    else:
      legal_bets = [("BET", 5*x + 5) for x in range(3)]
    check_bet = [("CHECK", 0)] + legal_bets

    # no reraising
    if len(self.actions) - 1 < self.betround:
      return check_bet
    else:
      bets = len(self.actions[self.betround])
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

  def get_successors(self, nextmove = []):
    if nextmove == []:
      nextmove = self.next_legal()
    successors = []
    # need to determine if a new round of betting has started
    # yes if last action was a call, or check/check

    if len(self.actions) == 0:

      for step in nextmove:
        successors.append(BetState([[step]], self.betround, not self.myturn, step[1]))
      return successors
    last_action = self.actions[self.betround][-1][0]
    sec_last_action = None
    if len(self.actions[self.betround]) >= 2:
      sec_last_action = self.actions[self.betround][-2][0]
    betround = None
    if last_action == "CALL" or (last_action == "CHECK" and sec_last_action == "CHECK"):
      for step in nextmove:
        actions = copy.deepcopy(self.actions)
        actions.append([step])
        newmybet = None
        if self.myturn:
          newmybet = self.mybet + step[1]
        else:
          newmybet = self.mybet
        successors.append(BetState(actions, self.betround + 1, not self.myturn, newmybet))
    else:
      for step in nextmove:
        actions = copy.deepcopy(self.actions)
        actions[-1].append(step)
        if self.myturn:
          newmybet = self.mybet + step[1]
        else:
          newmybet = self.mybet
        successors.append(BetState(actions, self.betround, not self.myturn, newmybet))
    return successors




