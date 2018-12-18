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

def gametest():
  deck = Deck()
  cardstate = CardState(deck)
  cardstate.deal_hand()
  betstate = BetState()
  gamestate = GameState(cardstate, betstate)
  new_state = gamestate.get_successors(("CHECK", 0))
  print new_state[0].betstate
  next_state = new_state[0].get_successors(("CHECK", 0))
  print next_state[0].betstate
  then_state = next_state[0].get_successors(("CHECK", 0))
  print then_state[0].betstate

def bettest():

  actions = [[("CHECK", 0)]]
  betround = 0
  myturn = False
  mybet = 0

  # first action check
  gs = BetState(actions, betround, myturn, 0)
  print gs
  print gs.get_successors(("CHECK", 0))
  for successor in gs.get_successors():
    print successor.get_successors()


  myturn = True
  gs = BetState(actions, betround, myturn, 0)
  # print gs.next_legal()

  # first action bet
  myturn = False
  actions = [[("BET", 5)]]
  gs = BetState(actions, betround, myturn, 0)
  # print gs.next_legal()

  actions = [[("CHECK", 0), ("BET", 5)]]
  gs = BetState(actions, betround, myturn, 0)
  # print gs.get_successors()

  # does betround work correctly
  actions = [[("CHECK", 0), ("CHECK", 0)]]
  gs = BetState(actions, betround, myturn, 0)
  # print gs.get_successors()

  actions = [[("BET", 10), ("RAISE", 20)]]
  gs = BetState(actions, betround, myturn, 0)
  # print gs.get_successors()

  actions = [[("CHECK", 0), ("BET", 10), ("RAISE", 20)]]
  gs = BetState(actions, betround, myturn, 0)
  # print gs.get_successors()

def runsimul(agent_type):
  a = Agent(agent_type)
  simul(a, Agent("aggressive"), 20)
  simul(a, Agent("passive"), 20) # [all 10's]
  simul(a, Agent("random"), 20)

runsimul("minimax")
