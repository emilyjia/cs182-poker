# card object
# hand object
# river object

import random
from collections import Counter
import copy
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
        if hand[2:] == [10,11,12,13,14]:
            return True, 14, 13, 12, 11, 10
        return False, 0, 0, 0, 0, 0

    def is_straightflush(self,top):
        return ((self.is_straight(top)[0] and self.is_flush(top)[0]), self.is_straight(top)[1], self.is_straight(top)[2], self.is_straight(top)[3], self.is_straight(top)[4], self.is_straight(top)[5])

    def is_fourkind(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        h = Counter(hand)
        h = h.most_common(len(hand))
        if h[0][1] == 4:
            return True, h[0][0], h[-1][0], h[-2][0], 0, 0
        return False, 0, 0, 0, 0, 0

    def is_fullhouse(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        h = Counter(hand)
        h = h.most_common(len(hand))
        if h[0][1] == 3 and h[1][1] == 2:
            return True, h[0][0], h[1][0], h[-1][0], h[-2][0], h[-3][0]
        return False, 0, 0, 0, 0, 0

    def is_flush(self,top):
        hand_suits = [top[i][1] for i in range(len(top))]
        h = Counter(hand_suits)
        h = h.most_common(1)

        if h[0][1] == 5:
            hand = []
            for i in range(len(top)):
                if top[i][1] == h[0][0]:
                    hand += [top[i][0]]
            hand.sort()
            return True, hand[-1], hand[-2], hand[-3], hand[-4], hand[-5]
        return False, 0, 0, 0, 0, 0

    def is_straight(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        for j in range(3):
            temp = True
            i = 0
            for i in range(4):
                if hand[j+i+1] != (hand[j+i] + 1): temp = False
            if temp == True: return True, hand[j+4], hand[j+3], hand[j+2], hand[j+1], hand[j]
        return False, 0, 0, 0, 0, 0

    # error when i try h[-4][0] as last element, not sure if that's a problem...
    def is_threekind(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        h = Counter(hand)
        h = h.most_common(len(top))
        if h[0][1] == 3: return True, h[0][0], h[-1][0], h[-2][0], h[-3][0], 0
        return False, 0, 0, 0, 0, 0

    def is_twopair(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        h = Counter(hand)
        h = h.most_common(7)
        if h[0][1] == 2 and h[1][1] == 2:
            return True, max(h[0][0],h[1][0]), min(h[0][0],h[1][0]), h[-1][0], h[-2][0], h[-3][0]
        else:
            return False, 0, 0, 0, 0, 0

    def is_pair(self,top):
        hand = [top[i][0] for i in range(len(top))]
        hand.sort()
        h = Counter(hand)
        h = h.most_common(7)
        if h[0][1] == 2:
            return True, h[0][0], h[-1][0], h[-2][0], h[-3][0], h[-4][0]
        else:
            return False, 0, 0, 0, 0, 0

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

        a,b,c,d,e,f = self.is_royalflush(cards)
        if a: return 10, b, c, d, e, f

        a,b,c,d,e,f = self.is_straightflush(cards)
        if a: return 9, b, c, d, e, f

        a,b,c,d,e,f = self.is_fourkind(cards)
        if a: return 8, b, c, d, e, f

        a,b,c,d,e,f = self.is_fullhouse(cards)
        if a: return 7, b, c, d, e, f

        a,b,c,d,e,f = self.is_flush(cards)
        if a: return 6, b, c, d, e, f

        a,b,c,d,e,f = self.is_straight(cards)
        if a: return 5, b, c, d, e, f

        a,b,c,d,e,f = self.is_threekind(cards)
        if a: return 4, b, c, d, e, f

        a,b,c,d,e,f = self.is_twopair(cards)
        if a: return 3, b, c, d, e, f

        a,b,c,d,e,f = self.is_pair(cards)
        if a: return 2, b, c, d, e, f

        hand = [cards[i][0] for i in range(len(cards))]
        hand.sort()
        return 1, hand[-1], hand[-2], hand[-3], hand[-4], hand[-5]

    def you_better(self, you, them, shared):
        # print self.best_hand(you, shared)
        # print self.best_hand(them, shared)
        (you_a, you_b, you_c, you_d, you_e, you_f) = self.best_hand(you, shared)
        (them_a, them_b, them_c, them_d, them_e, them_f) = self.best_hand(them, shared)
        return (you_a, you_b, you_c, you_d, you_e, you_f) > (them_a, them_b, them_c, them_d, them_e, them_f)

    def you_worse(self, you, them, shared):
        (you_a, you_b, you_c, you_d, you_e, you_f) = self.best_hand(you, shared)
        (them_a, them_b, them_c, them_d, them_e, them_f) = self.best_hand(them, shared)
        return (you_a, you_b, you_c, you_d, you_e, you_f) < (them_a, them_b, them_c, them_d, them_e, them_f)

me = [(10, 'club'), (8, 'diamond')]

# determines probability of winning

def winprob(me, shared):
    win = 0
    lose = 0
    tie = 0
    for i in range(1000):
        deck = Deck(me + shared)
        you = deck.deal_hand()
        shared_copy = copy.deepcopy(shared)
        while len(shared_copy) < 5:
            shared_copy += deck.deal_cards(1)
        if deck.you_better(me, you, shared_copy):
            win += 1
        elif deck.you_worse(me, you, shared_copy):
            lose += 1
        else:
            tie += 1
    return (win/1000.0, tie/1000.0, lose/1000.0)
