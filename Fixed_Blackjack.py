import random
# import time

deckOfCards = []
dealerHand = []
playerHand = []
Score = 0
playerScore = 0
dealerScore = 0
bet = 0

# makes a deck of (52 * a determinable number) cards
def newDeck(sets):
    for i in range(0, sets):
        for x in ('Hearts', 'Diamonds', 'Clubs', 'Spades'):
            deckOfCards.append(f'Ace of {x}')
            for y in range(2, 11):
                deckOfCards.append(f'{y} of {x}')
            for y in ('Jack', 'Queen', 'King'):
                deckOfCards.append(f'{y} of {x}')

# yes or no question command
def makingDecision(answer):
    while True:
        if answer == "y" or answer == "Y":
            return True
        elif answer == "n" or answer == "N":
            return False
        else:
            answer = input('''You can only answer with "y" or "n"
y/n?
> ''')

# allows the user pick how much money to bet
def makingBet(possession):
    amount = input('''Please enter the amount you want to bet
> ''')
    while True:
        if amount.isnumeric():
            amount = int(amount)
            if amount > possession:
                amount = input(f'''You only have ${possession} to bet with
> ''')
            else:
                return amount
        else:
            amount = input('''You can only answer with a number
> ''')

# returns value of a determined hand
def valueOf(hand):
    Sum = 0
    hasAce = 0
    for x in range(0, len(hand)):
        if hand[x][1:2].endswith(' '):
            Sum = Sum + int(hand[x][0:1])
            continue
        elif (hand[x][0:2]).isnumeric():
            Sum = Sum + 10
            continue
        elif (hand[x][0:1]) == 'J':
            Sum = Sum + 10
            continue
        elif (hand[x][0:1]) == 'Q':
            Sum = Sum + 10
            continue
        elif (hand[x][0:1]) == 'K':
            Sum = Sum + 10
            continue
        elif (hand[x][0:1]) == 'A':
            Sum = Sum + 11
            hasAce = hasAce + 1
            continue
    for x in range(0, hasAce):
        if Sum > 21:
            Sum = Sum - 10
    return Sum

# draws card(s) for a determined hand
def draw(hand, amount):
    hand.extend(deckOfCards[0:amount])
    del deckOfCards[0:amount]

# BLACKJACK
def gamestart(money):
    # RESTARTS STATS
    global deckOfCards
    deckOfCards = []
    global dealerHand
    dealerHand = []
    global playerHand
    playerHand = []
    global Score
    global playerScore
    playerScore = 0
    global dealerScore
    dealerScore = 0

    # creates a shuffled deck(s) and deals the hands
    newDeck(1)
    random.shuffle(deckOfCards)
    draw(dealerHand, 2)
    draw(playerHand, 2)

    print('Game starts')
    print(f'You have ${money}')
    bet = makingBet(money)

    while valueOf(dealerHand) < 17:
        draw(dealerHand, 1)
    if valueOf(dealerHand) > 21:
        playerScore = playerScore + 1
        money = money + bet
        Answer = makingDecision(input(f'''The dealer has {dealerHand}, for a total sum of {valueOf(dealerHand)}.
Dealer busts!
You have ${money}.
Try again?
y/n?
> '''))
        if Answer:
            gamestart(money)
            return
        elif Answer == False:
            Score = money
            return
    else:
        print(f'''The dealer has a {dealerHand[0:1]}, and {len(dealerHand) - 1} other card(s).
You the player have {playerHand }, for a total sum of {valueOf(playerHand)}.
What do you do? (Type "help" for commands)''')
    while True:
        if valueOf(playerHand) > 21:
            dealerScore = dealerScore + 1
            money = money - bet
            print(f'''You busted!
You have ${money}.''')
            if money == 0:
                Score = money
                return
            Answer = makingDecision(input('''Try again?
y/n?
> '''))
            if Answer:
                gamestart(money)
                return
            elif Answer == False:
                Score = money
                return
        command = input('> ')
        if command.title() == 'Help':
            print('''commands:
help
check
hit
stand''')
        if command.title() == 'Score':
            print(f'Score is {playerScore}:{dealerScore}')
        if command.title() == 'Check':
            print(f'''The dealer has a {dealerHand[0:1]}, and {len(dealerHand) - 1} other card(s).
You the player have {playerHand[0:len(playerHand)]}, for a total sum of {valueOf(playerHand)}.
You have ${money}.''')
        if command.title() == 'Hit':
            draw(playerHand, 1)
            print(f'You the player have {playerHand[0:len(playerHand)]}, for a total sum of {valueOf(playerHand)}.')
        if command.title() == 'Stand':
            if valueOf(playerHand) == 21 and valueOf(dealerHand) == 21:
                Answer = makingDecision(input(f'''A tie!
The dealer has {dealerHand}, for a total sum of {valueOf(dealerHand)}.
You the player have {playerHand[0:len(playerHand)]}, for a total sum of {valueOf(playerHand)}.
Try again?
y/n?
> '''))
                if Answer:
                    gamestart(money)
                    return
                elif Answer == False:
                    Score = money
                    return
            elif valueOf(playerHand) > valueOf(dealerHand):
                playerScore = playerScore + 1
                money = money + bet
                Answer = makingDecision(input(f'''You win!
The dealer has {dealerHand}, for a total sum of {valueOf(dealerHand)}.
You the player have {playerHand[0:len(playerHand)]}, for a total sum of {valueOf(playerHand)}.
You have ${money}.
Try again?
y/n?
> '''))
                if Answer:
                    gamestart(money)
                    return
                elif Answer == False:
                    Score = money
                    return
            else:
                dealerScore = dealerScore + 1
                money = money - bet
                print(f'''You lost!
The dealer has {dealerHand}, for a total sum of {valueOf(dealerHand)}.
You the player have {playerHand[0:len(playerHand)]}, for a total sum of {valueOf(playerHand)}.
You have ${money}.''')
                if money == 0:
                    Score = money
                    return
                Answer = makingDecision(input('''Try again?
y/n?
> '''))
                if Answer:
                    gamestart(money)
                    return
                elif Answer == False:
                    Score = money
                    return

# initiates the start of the game and repeats anytime the game ends
while True:
    input('''Press "enter" to play
''')
    gamestart(500)
    print(f'Your score: {Score}')