from expectimax import *
from minimax import *
from montecarlo import *
from state import *
from simul import *

def expectitest():
  deck = Deck()
  cardstate = CardState(deck)
  cardstate.deal_hand()
  print cardstate.myhand
  betstate = BetState()
  gamestate = GameState(cardstate, betstate)
  depth = 2
  print getExpectiAction(gamestate, depth)

def minimaxtest():
  deck = Deck()
  cardstate = CardState(deck)
  cardstate.deal_hand()
  print cardstate.myhand
  betstate = BetState()
  gamestate = GameState(cardstate, betstate)
  depth = 2
  print getMinimaxAction(gamestate, depth)

def bettest():

  actions = [[("CHECK", 0)]]
  betround = 0
  myturn = False
  mybet = 0

  # first action check
  gs = BetState(actions, betround, myturn, 0)
  print gs
  print gs.get_successors()
  for successor in gs.get_successors():
    print successor.get_successors()


  myturn = True
  gs = BetState(actions, betround, myturn, 0)
  print gs.next_legal()

  # first action bet
  myturn = False
  actions = [[("BET", 5)]]
  gs = BetState(actions, betround, myturn, 0)
  print gs.next_legal()

  actions = [[("CHECK", 0), ("BET", 5)]]
  gs = BetState(actions, betround, myturn, 0)
  print gs.get_successors()

  # does betround work correctly
  actions = [[("CHECK", 0), ("CHECK", 0)]]
  gs = BetState(actions, betround, myturn, 0)
  print gs.get_successors()

  actions = [[("BET", 10), ("RAISE", 20)]]
  gs = BetState(actions, betround, myturn, 0)
  print gs.get_successors()

  actions = [[("CHECK", 0), ("BET", 10), ("RAISE", 20)]]
  gs = BetState(actions, betround, myturn, 0)
  print gs.get_successors()


# simul(Agent("expectimax"), Agent("aggressive"), 1)
simul(Agent("expectimax"), Agent("passive"), 20)
simul(Agent("expectimax"), Agent("random"), 20)
simul(Agent("expectimax"), Agent("aggressive"), 20)
simul(Agent("expectimax"), Agent("expectimax"), 20)
