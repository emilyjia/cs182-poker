from expectimax import GameState


actions = [[("CHECK", 0)]]
betround = 0
myturn = False

# first action check
gs = GameState(actions, betround, myturn)
assert(gs.next_legal() == [("CHECK", 0), ("BET", 10)])
# print gs.get_successors()

myturn = True
gs = GameState(actions, betround, myturn)
assert(gs.next_legal() == [("CHECK", 0)] + [("BET", 5*x + 5) for x in range(20)])

# first action bet
myturn = False
actions = [[("BET", 5)]]
gs = GameState(actions, betround, myturn)
assert(gs.next_legal() == [("CALL", 5), ("FOLD", 0), ("RAISE", 15)])

actions = [[("CHECK", 0), ("BET", 5)]]
gs = GameState(actions, betround, myturn)
# print gs.get_successors()

# does betround work correctly
actions = [[("CHECK", 0), ("CHECK", 0)]]
gs = GameState(actions, betround, myturn)
# print gs.get_successors()

actions = [[("BET", 10), ("RAISE", 20)]]
gs = GameState(actions, betround, myturn)
# print gs.get_successors()

actions = [[("CHECK", 0), ("BET", 10), ("RAISE", 20)]]
gs = GameState(actions, betround, myturn)
# print gs.get_successors()

