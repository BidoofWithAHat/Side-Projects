print(f'i choose a random number between 1 to 10, you have 3 guesses.')
import random

stringList = ("what is your first guess? ", "what is your second guess? ", "what is your third guess? ")

while(True):
    failedGuesses = 0
    num = random.randint(1, 10)
    print(f"(the answer is: {num})")
    
    while(failedGuesses < 3):
        guess = input(stringList[failedGuesses])
        if guess.isnumeric():
            if (f"{guess}" == f"{num}"): #why does this not work without the f"{var}"?
                print('congrats that is my number!')
                break
            else:
                print('sorry, that is not my number')
                failedGuesses += 1
        else:
            print("that is not a number, please pick a number.")
   
    while(True):
        answer = input("do you want to play again? (y/n) ")
        if(answer == "y" or answer == "n"):
            break
        else:
            print("please answer with 'y' or 'n'")
    
    if(answer == "n"):
        break