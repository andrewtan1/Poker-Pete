# Card mapping: Let c=0,...51 be the card number
# Then c mod 13 refers to the rank, and floor(c/13) is the suit
# Ranks: A -> 0, 2 -> 1,  ...  , J -> 10, Q -> 11, K -> 12
# Suits: D -> 0, C -> 1, H -> 2, S -> 3
# e.g. c = 17 => c = 4 mod 13, floor(c/13) = 1, so it's the 5 of clubs
# Hands will be enumerated from 0 to 8 as follows: junk, pair, two pairs,
# three of a kind, straight, flush, full house, four of a kind, straight
# flush

import numpy as np
import random

# generate a card hand of size n (WILL NOT BE USED IN ACTUAL GAME)
def generate_hand(n):
    my_sample = random.sample(range(52), n)
    return np.asarray(my_sample)

# given a hand, give a list of ranks and suits (as numbers)
def get_ranks(hand):
    n = len(hand)
    ranks = np.zeros((n,), dtype=int)
    for i in range(n):
        ranks[i] = hand[i] % 13
        ranks[ranks == 0] = 13    
    return ranks
def get_suits(hand):
    n = len(hand)
    suits = np.zeros((n,),dtype=int)
    for i in range(n):
        suits[i] = hand[i] / 13
    return suits

# Print out the cards
def read_hand(hand):
    ranks = get_ranks(hand)
    suits = get_suits(hand)
    n = len(hand)
    for i in range(n):
        r = ranks[i]
        s = suits[i]
        str1 = " "
        str2 = " "
        #between 1-9 means the card's rank is from 2 to 10
        if 0 < r and r < 10:
            str1 = str(r+1)
        elif r == 10:
            str1 = "Jack"
        elif r == 11:
            str1 = "Queen"
        elif r == 12:
            str1 = "King"
        elif r == 13:
            str1 = "Ace"
        
        if s == 0:
            str2 = "Diamonds"
        elif s == 1:
            str2 = "Clubs"
        elif s == 2:
            str2 = "Hearts"
        elif s == 3:
            str2 = "Spades"
        print(str1, end =" ") 
        print("of", end = " ")
        print(str2)
    return

# return the hand's highest card
def get_highest_card(hand):
    ranks = get_ranks(hand)
    suits = get_suits(hand)
    max_rank = max(ranks)
    i = np.where(ranks == max_rank)[0]
    subset = suits[i]
    max_suit = max(subset)
    j = np.where(subset == max_suit)[0]
    high_card = hand[i[j]]
    return high_card
    
# check if the hand is a straight-flush (note: we cannot just use has_straight() and has_flush(), in the case that the hand has more than 5 cards)    
def has_straight_flush(hand):   
    for i in range(4):
        # royal = royal flush 10, J, Q, K, A
        royal = np.array([9,10,11,12,0]) + 13*i*np.ones((5,),dtype=int)
        if (all (x in hand for x in royal)):
            return True
        for j in range(9):
            straight_flush = range(j+13*i,j+13*i+5)
            if (all (x in hand for x in straight_flush)):
                return True

    return False


# check for a straight
def has_straight(hand): 
    ranks = get_ranks(hand)
    #wheel = straight of A 2 3 4 5 (the five-high straight)
    wheel = np.array([13,1,2,3,4])
    if (all (x in ranks for x in wheel)):
        return True
    
    for i in range(1,10):
        straight = range(i,i+5)
        if(all(x in ranks for x in straight)):
            return True
    return False

# check for a flush
def has_flush(hand):
    suits = get_suits(hand)
    suits = suits.tolist()
    for i in range(4):
        num = suits.count(i)
        if num >= 5:
            return True
    return False

#
def count_multiples(hand):
    pairs = 0
    triples = 0
    quadruples = 0
    counts = np.zeros((13,),dtype=int)
    ranks = get_ranks(hand)
    ranks[ranks == 13] = 0
    for i in range(len(hand)):
        counts[ranks[i]] = counts[ranks[i]] + 1
    for i in range(13):
        num = counts[i]
        if num == 2:
            pairs = pairs + 1
        elif num == 3:
            triples = triples + 1
        elif num == 4:
            quadruples = quadruples + 1

    return np.array([pairs,triples,quadruples])

def measure_strength(hand):
    straight = has_straight(hand)
    flush = has_flush(hand)
    straight_flush = has_straight_flush(hand)
    multiples = count_multiples(hand)
    pairs = multiples[0]
    triples = multiples[1]
    quadruples = multiples[2]

    if straight_flush:
        return 8
    if quadruples >= 1:
        return 7
    if triples >= 1 and pairs >= 1:
        return 6
    if flush:
        return 5
    if straight:
        return 4
    if triples >= 1:
        return 3
    if pairs >= 2:
        return 2
    if pairs == 1:
        return 1
    return 0

def read_strength(hand):
    s = measure_strength(hand)
    if s == 8:
        print("Straight Flush")
    elif s == 7:
        print("Four of a Kind")
    elif s == 6:
        print("Full House")
    elif s == 5:
        print("Flush")
    elif s == 4:
        print("Straight")
    elif s == 3:
        print("Three of a Kind")
    elif s == 2:
        print("Two Pairs")
    elif s == 1:
        print("One Pair")
    else:
        print("Nothing")
    return

def recommend_move(hand):
    discard_list = [1,2,3,4,5]
    ranks = get_ranks(hand)
    suits = get_suits(hand)

    rank_count = np.zeros((13,),dtype=int)
    suit_count = np.zeros((4,), dtype = int)

    ranks[ranks == 13] = 0
    for x in ranks:
        rank_count[x] = rank_count[x] + 1
    for x in suits:
        suit_count[x] = suit_count[x] + 1


    s = measure_strength(hand)
    # If straight or higher, keep the cards
    if s >= 4:
        print("Keep all cards")
        return
    # If 3 of a kind, throw away the other two cards
    elif s == 3:
        for i in range(5):
            if rank_count[ranks[i]] == 3:
                #find index in discard_list
                ind = discard_list.index(i+1)
                discard_list.pop(ind)
        

    # If 1 or 2 pairs, throw away nonpaired cards
    elif s == 2 or s == 1:
        for i in range(5):
            if rank_count[ranks[i]] == 2:
                #find index in discard_list
                ind = discard_list.index(i+1)
                discard_list.pop(ind)
    

    #If junk, keep cards that MIGHT get you good hands (e.g. flush, straight). Otherwise, discard all low cards in hopes for a decent pair
    else:
        # Attempt to go for a flush if possible
        close_to_flush = False
        close_to_straight = False
        closeness_requirement = 4


        if max(suit_count) == closeness_requirement:
            close_to_flush = True
            for i in range(len(hand)):
                if suit_count[suits[i]] == closeness_requirement:
                    ind = discard_list.index(i+1)
                    discard_list.pop(ind)   
        # Attempt to go for a straight if possible
        
        if close_to_flush == False:
            temp = [1, 2, 3, 4, 5]
            # note: royal as in UNSUITED 10, J, Q, K, A
            royal = [9, 10, 11, 12, 0] 
            close_to_royal = False
            for j in range(5):
                if ranks[j] in royal:
                    ind = temp.index(j+1)
                    temp.pop(ind)
            if len(temp) == 5 - closeness_requirement:
                close_to_royal = True
                close_to_straight = True
                discard_list = temp

            if close_to_royal == False:
                for i in range(9):
                    temp = [1, 2, 3, 4, 5]
                    straight = [8-i, 9-i, 10-i, 11-i, 12-i]
                    for j in range(5):
                        if ranks[j] in straight:
                            ind = temp.index(j+1)
                            temp.pop(ind)
                    if len(temp) == 5 - closeness_requirement:
                        close_to_straight = True
                        discard_list = temp


        if close_to_flush == False and close_to_straight == False:
            ranks[ranks == 0] = 13
            for i in range(5): 
                if ranks[i] >= 10:
                    ind = discard_list.index(i+1)
                    discard_list.pop(ind) 
               
    print("Discard card(s)", end = " ")
    for x in discard_list:

        print(x, end = " ")
    print(" ")
    return


def main():
    #hand = np.array([0,2,4, 5,38])
    hand = generate_hand(5)
    ranks = get_ranks(hand)
    suits = get_suits(hand)
    print(hand)
    print(ranks)
    print(suits)
    read_hand(hand)
    high_card = get_highest_card(hand)
    print("The highest card is", end = " ")
    read_hand(high_card)
    print("You have", end = " ")
    read_strength(hand) 
    recommend_move(hand)

    
    
       
if __name__ == "__main__" :
    main()
  