from expectimax import BetState


from montecarlo import winprob



def bettest():

  actions = [[("CHECK", 0)]]
  betround = 0
  myturn = False
  mybet = 0

  # first action check
  gs = BetState(actions, betround, myturn, 0)
  assert(gs.next_legal() == [("CHECK", 0), ("BET", 10)])
  print gs.get_successors()

  myturn = True
  gs = BetState(actions, betround, myturn, 0)
  assert(gs.next_legal() == [("CHECK", 0)] + [("BET", 5*x + 5) for x in range(20)])

  # first action bet
  myturn = False
  actions = [[("BET", 5)]]
  gs = BetState(actions, betround, myturn, 0)
  assert(gs.next_legal() == [("CALL", 5), ("FOLD", 0), ("RAISE", 15)])

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


bettest()
