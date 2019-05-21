# Card mapping: Let c=0,...51 be the card number
# Then c mod 13 refers to the rank, and floor(c/13) is the suit
# Ranks: A -> 0, 2 -> 1,  ...  , J -> 10, Q -> 11, K -> 12, A -> 13
# Suits: D -> 0, C -> 1, H -> 2, S -> 3
# e.g. c = 17 => c = 4 mod 13, floor(c/13) = 1, so it's the 5 of clubs
# Hands will be enumerated from 0 to 8 as follows: junk, pair, two pairs,
# three of a kind, straight, flush, full house, four of a kind, straight
# flush

import numpy as np
import random
def rankMap(rank):
    rankNum = {
        0 : "Ace",
        1 : "Two",
        2 : "Three",
        3 : "Four",
        4 : "Five",
        5 : "Six",
        6 : "Seven",
        7 : "Eight",
        8 : "Nine",
        9 : "Ten",
        10 : "Jack",
        11 : "Queen",
        12 : "King",
        13 : "Ace",
    }
    return rankNum.get(rank,"invalid rank")

# Map Suits to Numbers for Calculations
def suitMap(suit):
    suitNum = {
        0 : "Diamonds",
        1 : "Clubs",
        2 : "Hearts",
        3 : "Spades"
    }
    return suitNum.get(suit,"invalid suit")

def bin(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke.
    See http://stackoverflow.com/questions/3025162/statistics-combinations-in-python
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

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
        # Change ace to have rank 13
        ranks[ranks == 0] = 13    
    return ranks
def get_suits(hand):
    n = len(hand)
    suits = np.zeros((n,),dtype=int)
    for i in range(n):
        suits[i] = hand[i] / 13
    return suits

def compute_blackjack_sum(hand):
    sum = 0
    ranks = get_ranks(hand)
    n = len(hand)
    for i in range(n):
        if ranks[i] == 13:
            sum = sum + 11
        if ranks[i] >= 9:
            sum = sum + 10
        else:
            sum = sum + (ranks[i]+1)
    if sum > 21:
        for i in range(n):
            # Should still check if sum > 21 in case there are multiple aces
            if ranks[i] == 13 and sum > 21:
                sum = sum - 10
    return sum

# Print out the cards
def read_hand(hand):
    ranks = get_ranks(hand)
    suits = get_suits(hand)
    n = len(hand)
    for i in range(n):
        r = ranks[i]
        s = suits[i]
        str1 = rankMap(r)
        str2 = suitMap(s)
        print(str1, end =" ") 
        print("of", end = " ")
        if i == n - 1:
            print(str2)
        else:
            print(str2, end = ", ")
    return

# compare two cards

def compare_cards(c1, c2):
    winner = 0
    r1 = get_ranks(c1)
    r2 = get_ranks(c2)
    s1 = get_suits(c1)
    s2 = get_suits(c2)

    if r1 > r2:
        winner = 1
    elif r1 < r2:
        winner = 2
    else:
        if s1 > s2:
            winner = 1
        elif s1 < s2:
            winner = 2

    return winner

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
    high = get_highest_card(hand)
    ranks = get_ranks(hand)
    suits = get_suits(hand)
    high_rank = get_ranks(high)[0]

    if straight_flush:
        # A 2 3 4 5 straight flush
        if 13 in ranks and 4 in ranks:
            s = 4
        else:
            s = high_rank
        return s+ 800

    if quadruples >= 1:
        unique, counts = np.unique(ranks, return_counts = True)
        for i in range(unique.size):
            if counts[i] == 4:
                s = unique[i]           
        return s + 700

    if triples >= 1 and pairs >= 1:
        unique, counts = np.unique(ranks, return_counts = True)
        for i in range(unique.size):
            if counts[i] == 3:
                s = unique[i]
        return s + 600
    if flush:
        return suits[0] + 500
    if straight:
        if 13 in ranks and 4 in ranks:
            s = 4
        else:
            s = high_rank
        return s + 400
    if triples >= 1:
        unique, counts = np.unique(ranks, return_counts = True)
        for i in range(unique.size):
            if counts[i] == 3:
                s = unique[i]
        return s + 300

    if pairs >= 2:
        unique, counts = np.unique(ranks, return_counts = True)
        s = 0
        for i in range(unique.size):
            if counts[i] == 2 and unique[i] > s:
                s = unique[i]
        return s + 200

    if pairs == 1:
        unique, counts = np.unique(ranks, return_counts = True)
        for i in range(unique.size):
            if counts[i] == 2:
                s = unique[i]
        return s + 100

    else:
        return high_rank

def read_strength(hand):
    s = measure_strength(hand)
    t = s % 100
    rank = rankMap(t)
    high_card = get_highest_card(hand)
    high_rank = rankMap(get_ranks(high_card)[0])
    high_suit = suitMap(get_suits(high_card)[0])
    
    output = ""
    if s == 813:
        output = "Royal Flush of " + high_suit
    elif s > 800:
        output = "Straight Flush with leading card" + high_rank + " of " + high_suit
    elif s > 700:
        output = "Four of a Kind of " + rank
    elif s > 600:
        output = "Full House of " + rank
    elif s > 500:
        output = "Flush of " + high_suit + ". Highest card is " + high_rank + " of " + high_suit
    elif s > 400:
        output = "Straight with leading card " + high_rank + " of " + high_suit
    elif s > 300:
        output = "Three of a Kind of " + rank
    elif s > 200:
        ranks = get_ranks(hand)
        p1 = rank
        p2 = " "
        unique, counts = np.unique(ranks, return_counts = True)
        for i in range(unique.size):
            if counts[i] == 2 and unique[i] != t:
                p2 = rankMap(unique[i])
        output = "Two Pairs of " + p1 + " and " + p2
    elif s > 100:
        output = "One Pair of " + rank
    else:
        output = "Nothing. Highest card is " + high_rank + " of " + high_suit

    print(output)
    return output

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
    if s >= 400:
        print("Keep all cards")
        return []
    
    # If 3 of a kind, throw away the other two cards
    elif s >= 300:
        for i in range(5):
            if rank_count[ranks[i]] == 3:
                #find index in discard_list
                ind = discard_list.index(i+1)
                discard_list.pop(ind)
        

    # If 1 or 2 pairs, throw away nonpaired cards
    elif s >= 100:
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

        # If not close to flush or straight, keep all high cards according to rank threshold
        if close_to_flush == False and close_to_straight == False:
            rank_threshold = 10
            ranks[ranks == 0] = 13
            for i in range(5): 
                if ranks[i] >= rank_threshold:
                    ind = discard_list.index(i+1)
                    discard_list.pop(ind) 
               
    return discard_list

# estimate the probability of getting a LOWER hand
def estimate_probability(hand):
    s = measure_strength(hand)
    t = s % 100

    if s > 800:
        return 1 - 0.000015
    elif s > 700:
        return 1 - 0.000256
    elif s > 600:
        return 1 - 0.0017
    elif s > 500:
        return 1 - 0.00367
    elif s > 400:
        return 1 - 0.0076
    elif s > 300:
        return 1- 0.0287
    elif s > 200: 
        return 1 - 0.0762
    elif s > 100:
        #TODO: compute probability
        p = 1 - 0.499
        i = t
        while i > 1:
            p = p + bin(4,2)*bin(12,3)*pow(4,3)/bin(52,5)
            i = i - 1
        return p
    else:
        #TODO: compute probability 
        p = 0
        for i in range(6,13):
            if i == t:
                return p
            p = p + (4*(bin(i-1,4)*pow(4,4) - pow(4,4) - bin(i-1,4) + 1))/(bin(52,5))
        return p

# Simulate a game of poker (start with Borel model where P1 can fold first)

def play_game():
    play = True
    p1_pool = 10
    p2_pool = 10
    num_rounds = 3
    ante = 1
    
    while play == True and p1_pool > 0 and p2_pool > 0:
        winner = 0
        p = input("Play? [y/n]: ")
        if p == 'y' or p == 'Y' or p1_pool <= 0 or p2_pool <= 0:
            p1_pool = p1_pool - ante
            p2_pool = p2_pool - ante
            pool = 2

            start = generate_hand(10)
            used = start
            p1_hand = start[0:5]
            p2_hand = start[5:10]

            for i in range(num_rounds):
                print("Your current hand is: ")
                print(p1_hand)
                read_hand(p1_hand)
                invalid = True
                action = input("What would you like to do? [bet/check]:")
                while invalid == True:
                    if action == "bet" or action == "check":
                        invalid = False
                    else:
                        action = input("Invalid action, try again. [bet/check]:")
                if action == "bet":
                    p1_pool = p1_pool - 1
                    pool = pool + 1
                    # p2 calls
                    print("The opponent calls!")
                    p2_pool = p2_pool - 1
                    pool = pool + 1

                #elif action == "check":

                print("List the cards you want to discard (no commas!):")
                discard = list(map(int,input().split()))
                for x in discard:
                    redundant = True
                    while redundant == True:
                        new_card = random.randint(0,51)
                        if np.any(used[:] == new_card) == False:
                            redundant = False
                            used = np.append(used, new_card)
                            p1_hand[x-1] = new_card
                            print("Used cards p1: ", used)
                
                p2_discard  = recommend_move(p2_hand)
                for x in p2_discard:
                    redundant = True
                    while redundant == True:
                        new_card = random.randint(0,51)
                        if np.any(used[:] == new_card) == False:
                            redundant = False
                            used = np.append(used, new_card)
                            p2_hand[x-1] = new_card
                            print("Used cards p2: ", used)
                            
            print("Your final hand is: ")
            read_hand(p1_hand)
            read_strength(p1_hand)
            print("The opponent's final hand is: ")
            read_hand(p2_hand)
            read_strength(p2_hand)
            s1 = measure_strength(p1_hand)    
            s2 = measure_strength(p2_hand)

            
            if s1 > s2:
                winner = 1
            elif s1 < s2:
                winner = 2
            else:
                winner = compare_cards(get_highest_card(p1_hand), get_highest_card(p2_hand))

            if winner == 1:
                p1_pool = p1_pool + pool
                print("You won! You currently have", end = " ") 
                print(p1_pool, end = " ")
                print("points")  

            elif winner == 2:
                p2_pool = p2_pool + pool
                print("You lost! You currently have", end = " ")
                print(p1_pool, end = " ")
                print("points")

        else:
            play = False
    print("Game over! Your final score is", end = " ")
    print(p1_pool, end = " ")
    print("points")


    return

def main():
    """
    hand = np.array([12,25, 2, 29, 50])
    hand = generate_hand(5)
    print(hand)
    read_hand(hand)
    #print("Strength is", end = " ")
    #print(measure_strength(hand))
    print("You have", end = " ")
    read_strength(hand) 
    recommend_move(hand)
    print("The probability of a lower hand is", end = " ")
    print(estimate_probability(hand))
    print("Discard card(s)", end = " ")
    discard_list = recommend_move(hand)
    print(discard_list)
    """
    play_game()
       
main()
    
#%%
