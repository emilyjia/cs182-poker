# card object
# hand object
# river object

import random
from collections import Counter

class Deck:
# deck class: ranks are 2-14 (14 = ace)
    def __init__(self, remove_lst = []):
        self.cards = []
        self.ranks = range(2, 15)
        self.suits = ["heart", "spade", "club", "diamond"]
        for rank in self.ranks:
            for suit in self.suits:
                if (rank, suit) not in remove_lst:
                    self.cards.append((rank, suit))
        random.shuffle(self.cards)

    def deal_cards(self, number):
        lst = []
        for i in range(number):
            lst.append(self.cards.pop())
        return lst

    def deal_hand(self):
        return self.deal_cards(2)

    def deal_river(self):
        return self.deal_cards(5)

    # determine what kind of hand

    def is_royalflush(self, top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        if hand == [10,11,12,13,14]:
            return True, 14, 13
        return False, 0, 0

    def is_straightflush(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        return ((self.is_straight(top)[0] and self.is_flush(top)[0]), hand[-1], hand[-2])

    def is_fourkind(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        if hand.count(hand[0]) == 4:
            return True, hand[0], hand[-1]
        elif hand.count(hand[-1]) == 4:
            return True, hand[-1], hand[0]
        return False, 0, 0

    def is_fullhouse(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        if (hand.count(hand[0]) == 2) and (hand.count(hand[-1]) == 3):
            return True, hand[-1], hand[0]
        elif (hand.count(hand[0]) == 3) and (hand.count(hand[-1]) == 2):
            return True, hand[0], hand[-1]
        return False, 0, 0

    def is_flush(self,top):
        hand_suits = [top[i][1] for i in range(len(top))]
        h = Counter(hand_suits)
        h = h.most_common(1)

        if h[0][1] == 5:
            hand = [top[i][0] for i in range(len(top))]
            hand.sort()
            return True, hand[-1], hand[-2]
        return False, 0, 0

    def is_straight(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        for i in range(len(hand)-1):
            if hand[i+1] != (hand[i] + 1): return False, 0, 0
        return True, max(hand), 0

    def is_threekind(self,top):
        hand = [top[i][0] for i in range(len(top))]
        h = Counter(hand)
        h = h.most_common(5)
        if h[0][1] == 3: return True, h[0][0], h[1][0]
        return False, 0, 0

    def is_twopair(self,top):
        hand = [top[i][0] for i in range(len(top))]
        h = Counter(hand)
        h = h.most_common(2)
        if h[0][1] == 2 and h[1][1] == 2:
            return True, max(h[0][0],h[1][0]), min(h[0][0],h[1][0])
        else:
            return False, 0, 0

    def is_pair(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        h = Counter(hand)
        h = h.most_common(5)
        if h[0][1] > 1:
            return True, h[0][0],h[-1][0]
        else:
            return False, 0, 0

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

    # returns (# of hand, determining card)
    def best_hand(self, you, shared):

        cards = you + shared

        a,b,c = self.is_royalflush(cards)
        if a: return 10, b, c

        a,b,c = self.is_straightflush(cards)
        if a: return 9, b, c

        a,b,c = self.is_fourkind(cards)
        if a: return 8, b, c

        a,b,c = self.is_fullhouse(cards)
        if a: return 7, b, c

        a,b,c = self.is_flush(cards)
        if a: return 6, b, c

        a,b,c = self.is_straight(cards)
        if a: return 5, b, c

        a,b,c = self.is_threekind(cards)
        if a: return 4, b, c

        a,b,c = self.is_twopair(cards)
        if a: return 3, b, c

        a,b,c = self.is_pair(cards)
        if a: return 2, b, c

        hand = [cards[i][0] for i in range(len(cards))]
        hand.sort()
        return 1, hand[-1], hand[-2]

    def you_better(self, you, them, shared):
        # print self.best_hand(you, shared)
        # print self.best_hand(them, shared)
        (you_a, you_b, you_c) = self.best_hand(you, shared)
        (them_a, them_b, them_c) = self.best_hand(them, shared)
        return (you_a > them_a) or (you_a == them_a and you_b > them_b) or (you_a == them_a and you_b == them_b and you_c > them_c)

    def you_worse(self, you, them, shared):
        (you_a, you_b, you_c) = self.best_hand(you, shared)
        (them_a, them_b, them_c) = self.best_hand(them, shared)
        return (you_a < them_a) or (you_a == them_a and you_b < them_b) or (you_a == them_a and you_b == them_b and you_c < them_c)


test_deck = Deck()
# me = test_deck.deal_hand()
me = [(10, 'club'), (8, 'diamond')]
win = 0
lose = 0
tie = 0
for i in range(1000):
    deck = Deck(me)
    you = deck.deal_hand()
    # print you
    river = deck.deal_river()
    # print river
    if deck.you_better(me, you, river):
        win += 1
        # print "better"
    elif deck.you_worse(me, you, river):
        lose += 1
        # print "worse"
    else:
        tie += 1
        # print "tie"

print win, lose, tie
print 1.0*win/(win+lose+tie)
