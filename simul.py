from minimax import *
from expectimax import *
from state import *

# define two bots, number of rounds, tally PNL


def simul(mybot, opponent, games):
  mybot_pnl = []
  print "==============="
  for game in range(games):
    deck = Deck()
    cardstate = CardState(deck)
    cardstate.deal_hand()
    print "my cards"
    print cardstate.myhand
    betstate = BetState()
    gamestate = GameState(cardstate, betstate)
    depth = 2
    while not gamestate.is_terminal():
      action = None
      print "shared"
      print gamestate.cardstate.shared
      if gamestate.betstate.myturn:
        action = mybot.get_action(gamestate, depth)
        print "my action " + str(action)
        gamestate = gamestate.get_successors(action)[0]
        print gamestate.betstate
      else:
        action = opponent.get_action(gamestate, depth)
        print "opponent action " + str(action)
        gamestate = gamestate.get_successors(action)[0]
        print gamestate.betstate
    print gamestate.get_value()
    mybot_pnl.append(gamestate.get_value())
    print mybot_pnl
    print "==============="
