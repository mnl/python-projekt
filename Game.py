#!/usr/bin/env python3

import random

class Dice:
    """ Class for holding dice """

    def __init__(self):
        self.frozen = False
        self.roll()

    def __str__(self):
        return str(self.value)

    def roll(self):
        if (not self.frozen):
            self.val = random.randint(1,6)

    def fakeroll(self,fake):
        self.val = fake

    @property
    def value(self): 
        return self.val

    @property
    def iced(self): 
        return self.frozen

    def freeze(self):
        self.frozen = True
        
    def thaw(self):
        self.frozen = False

    def toggle(self):
        self.frozen = not self.frozen

class Score:
    """ Score keeping functions live here """
    
#    def count(c,dice):
#        """ Return number of occurances for c """
#        return len([i for i, d in enumerate(dice) if d.value == c])

    def count(dice):
        """ Helper function to count occurances of each value"""
#        counts = { nr.value: Score.count(nr.value, dice) for nr in dice}
        counts = { nr.value: Score.upper(nr.value, dice)//nr.value for nr in dice }
        return counts
    
    def upper(num,dice):
        """ Returns sum of all values num """
        return sum( die.value for die in dice if die.value == num )

    def ones(dice):
        return Score.upper(1,dice)
    def twos(dice):
        return Score.upper(2,dice)
    def threes(dice):
        return Score.upper(3,dice)
    def fours(dice):
        return Score.upper(4,dice)
    def fives(dice):
        return Score.upper(5,dice)
    def sixes(dice):
        return Score.upper(6,dice)

    def onePair(dice):
        """ Returns sum of pair or zero """
        score = 0
        throw = Score.count(dice)
        for k,v in throw.items():
            if v >= 2:
                score = max(score, k*2)
        return score
    
    def twoPairs(dice):
        """ Returns sum of two pairs or zero """
        score = 0
        throw = Score.count(dice)
        for k,v in throw.items():
            if v >= 2:
                score += k*2
        if score <= Score.onePair(dice):
            return 0
        return score
    
    def kinds(n,dice):
        """ Returns the sum of n dice with the same value"""
        throw = Score.count(dice)
        for k,v in throw.items():
            if v >= n:
                return k*n
        return 0
    
    def threeKind(dice): return Score.kinds(3,dice)
    def fourKind(dice): return Score.kinds(4,dice)
    
    def straight(dice,large=False):
        """ Returns 15, 20 or 0 for small, large or no straight"""
        values = sorted([ die.value for die in dice ])
        a_straight = [2,3,4,5,6] if large else [1,2,3,4,5]
        if values == a_straight:
            return sum(values)
        return 0
    def smStraight(dice):
        return Score.straight(dice)
    def lgStraight(dice):
        return Score.straight(dice,large=True)

    def fullHouse(dice):
        pair = Score.twoPairs(dice)
        thrice = Score.threeKind(dice)
        if (pair and thrice):
            return pair+thrice
        return 0

    def chance(dice):
        """ Return sum of all dice values """
        return sum([ die.value for die in dice ])

    def yatzy(dice): 
        if Score.kinds(5,dice): 
            return 50
        return 0

class CommandLine:

    def __init__():
        pass

    def play():

        # Make five new dice
        dice = [ Dice() for n in range(5) ]
    
        for time in range(1,3):
        
            print(f"Throw numer {time}")
        
            # Roll and thaw all dice
            for die in dice:
                die.roll()
                die.thaw()
                
            # Sort current throw
            throw = [ die.value for die in dice ]
               
            # Print result
            print("-<1>-<2>-<3>-<4>-<5>-\n  ",end="")
            for d in range(5):
                print(throw[d],end="   ")
            print("\n")
                
            # Select dice to hold
            hold = input("Select dice to hold: ").split(',')
            for die in hold:
                dice[int(die)-1].freeze()
            print()
            
        for die in dice:
            die.roll()
        # Print result
        print("-<1>-<2>-<3>-<4>-<5>-\n  ",end="")
        throw = [ die.value for die in dice ]
        for d in range(5):
            print(throw[d],end="   ")
        print()
    
        print(" 0: Exit game")
        print(" 1: Ones:\t\t",Score.upper(1,dice))
        print(" 2: Twos:\t\t",Score.upper(2,dice))
        print(" 3: Threes:\t\t",Score.upper(3,dice))
        print(" 4: Fours:\t\t",Score.upper(4,dice))
        print(" 5: Fives:\t\t",Score.upper(5,dice))
        print(" 6: Sixes:\t\t",Score.upper(6,dice))
        print(" 7: One pair:\t\t",Score.onePair(dice))
        print(" 8: Two pair:\t\t",Score.twoPairs(dice))
        print(" 9: Three of a kind:\t",Score.threeKind(dice))
        print("10: Four of a kind:\t",Score.fourKind(dice))
        print("11: Small straight:\t",Score.straight(dice))
        print("12: Large straight:\t",Score.straight(dice,large=True))
        print("13: Full house:\t\t",Score.fullHouse(dice))
        print("14: Chance:\t\t",Score.chance(dice))
        print("15: Yatzy:\t\t",Score.yatzy(dice))
        while True:
                selection = int(input("Select field to score in: "))
                if selection in range(16):
                    break
                print("Invalid choice")
        
