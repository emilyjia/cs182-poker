# card object
# hand object
# river object

import random
import collections

class Deck:
# deck class: ranks are 2-14 (14 = ace)
  def __init__(self, remove_lst):
    cards = []
    ranks = range(2, 15)
    suits = ["heart", "spade", "club", "diamond"]
    for rank in ranks:
      for suit in suits:
        if (rank, suit) not in remove_lst:
          cards.append((rank, suit))
    cards.shuffle()

  def deal_cards(self, number):
    lst = []
    for i in range(number):
      lst.append(cards.pop)
    return lst

  def deal_hand(self):
    self.deal_cards(2)

  def deal_river(self):
    self.deal_cards(5)


# royal flush = 1
# straight flush = 2
# four of a kind = 3
# full house = 4
# flush = 5
# straight = 6
# three of a kind = 7
# two pair = 8
# pair = 9
# high card = 10
# returns (# of hand, determining card(s))
  def best_hand(self, you, shared):
    straight = false
    flush = false
    repeated = 0
    cards = you.extend(shared)
    # repeated cards
    c = Counter(cards)
    top = c.most_common(5)
    first_value == top[0][0]
    first_freq == top[0][1]
    sec_value == top[1][0]
    sec_freq == top[1][1]
    # check repeated
    if first_freq == 1:
      repeated = 10
    elif first_freq == 2 and not flush:
      # two pair or pair
      if second_freq == 2:
        lst = [first_value, sec_value]
        lst.sort()
        return (8, lst)
      if second_freq == 1:
        # need kicker

    # straight

    # is it a flush
    # repeated cards







