#
# RandNumGame.py
# Random Number Game
# This file implements a (maybe not so exciting) random number game.
#
# Created by Eugene Krug in January 2019.
#


import random
import LeaderboardEntry


# Variables/constants for the game
curPlayerName = ""
numRounds = 5
minRandNum = 1
maxRandNum = 10
curRoundIndex = 0
score = 0
maxNumGuesses = 3
leaderboardFilePath = 'leaderboard.txt'
numPlayersOnLeaderboard = 0
maxNumPlayersOnLeaderboard = 3
leaderboardEntries = []
qualifiedForLeaderboard = True


# Displays a welcome messge and the rules
def dispWelcomeAndRules():
    print("Welcome to a (maybe not so exciting) random number game!")
    print("* You will be guessing a random number between " + str(minRandNum) + " and " + str(maxRandNum) + ".")
    print("* The game consists of " + str(numRounds) + " rounds.")
    print("* For each round, you will have at most " + str(maxNumGuesses) + " guesses.")
    print("* If you guess correctly, the number of points you earn is equal to the number.")
    print("* If the guess is NOT your last guess, you will receive bonus points!")
    print("  Bonus points are calculated as the number of guesses remaining as you made your guess")
    print("  times the number. For example, you would earn " + str(maxNumGuesses) + "x the number of points")
    print("  if you guessed correctly on the first guess.")
    print()
    print()


# Prompts the user for their name and returns it
def getUserName():
    print("Enter your name: ")
    curPlayerName = input()

    while(curPlayerName == ""):
        print("Invalid input. Please enter your name.")
        curPlayerName = input()

    return curPlayerName


# Read in leaderboard from file
def readInLeaderboard():
    try:
        leaderboardFile = open(leaderboardFilePath, 'r')

        lineName = leaderboardFile.readline().rstrip("\n")
        lineScore = leaderboardFile.readline().rstrip("\n")

        while lineName:
            newLeaderboardEntry = LeaderboardEntry.LeaderboardEntry(lineName, int(lineScore))
            leaderboardEntries.append(newLeaderboardEntry)

            lineName = leaderboardFile.readline().rstrip("\n")
            lineScore = leaderboardFile.readline().rstrip("\n")   
        
        leaderboardFile.close()

        global numPlayersOnLeaderboard 
        numPlayersOnLeaderboard = len(leaderboardEntries)

    except IOError:
        print("Leaderboard file not found. If this is your first time playing, ")
        print("this is normal. A leaderboard file will be created when you finish.")
        print()
        print()


# Display the leaderboard
def dispLeaderboard():
    print("** Leaderboard **") 
    if(numPlayersOnLeaderboard == 0):
        print("Empty! You're guarenteed to be #1!")
    else:
        i = 0

        while(i < numPlayersOnLeaderboard):
            print("#{0:2} {1:16} {2:3}".format(str(i+1), leaderboardEntries[i].name, str(leaderboardEntries[i].score)))
            i += 1

    print()
    print()


# Write the leaderboard to file
def writeOutLeaderboard():
    if leaderboardFilePath != "":
        leaderboardFile = open(leaderboardFilePath, 'w')

        i = 0

        while(i < numPlayersOnLeaderboard):
            leaderboardFile.write(leaderboardEntries[i].name + '\n')
            leaderboardFile.write(str(leaderboardEntries[i].score) + '\n')
            i += 1

        leaderboardFile.close()
    else:
        print("A leaderboard file path was not specified, so changes to the leaderboard will not persist between game sessions.")


# Add's the most recent play (user's name and score) to the leaderboard
# Called if leaderboard updates are necessary
def leaderboardUpdates():
    # Create a new leaderboard entry and append to the leaderboard entries array
    newLeaderboardEntry = LeaderboardEntry.LeaderboardEntry(curPlayerName, score)
    leaderboardEntries.append(newLeaderboardEntry)

    # Sort the leaderboard entries array by descending score
    leaderboardEntries.sort(key=lambda x: x.score, reverse=True)

    global numPlayersOnLeaderboard
    numPlayersOnLeaderboard = len(leaderboardEntries)

    # If the the number of leaderboard entries is greater than the maximum 
    # number allowed, remove the last entry
    while(numPlayersOnLeaderboard > maxNumPlayersOnLeaderboard): 
        del leaderboardEntries[numPlayersOnLeaderboard - 1]
        numPlayersOnLeaderboard = len(leaderboardEntries)

    # Write the leaderboard to file
    writeOutLeaderboard()


# Returns a random number in the range defined
def getRandNumInRange():
    return random.randint(minRandNum, maxRandNum)


# Prompts the user for their guess and returns it
def getUserGuess():
    badInput = True
    
    print("Enter your guess: ")

    while badInput:
        try:
            userGuess = int(input())
            badInput = False
        except ValueError:
            print("Invalid input. Please enter an integer value.")

    return userGuess


# Display feedback based on the user's incorrect guess
def dispIncGuessFeedback(guess, number, curGuessesRemaining):
    if curGuessesRemaining != 1: # not the user's last guess
        if guess > number:
            print("Incorrect...too high!")
        else:
            print("Incorrect...too low!")
    else: # the user's last guess
        print("Incorrect...the correct number was ", number)



# Welcome the user
dispWelcomeAndRules()


# Read in and display the leaderboard
readInLeaderboard()
dispLeaderboard()


# Get the user's name
curPlayerName = getUserName()
print()


# Game drive logic/loop for each round
while(curRoundIndex < numRounds):
    # Print current score
    print("Round: " + str(curRoundIndex + 1) + " (of " + str(numRounds) + ")")
    print("Score: " + str(score))
    print()

    # Get a random number in the range defined
    randNumInRange = getRandNumInRange()

    curGuessesRemaining = maxNumGuesses
    while(curGuessesRemaining > 0):
        # Get the user's guess
        userGuess = getUserGuess()

        if userGuess == randNumInRange: # user makes the correct guess
            pointsEarned = userGuess * curGuessesRemaining

            if curGuessesRemaining != 1: # not the user's last guess, so earning a point bonus
                print("Correct guess! You have the " + str(curGuessesRemaining) + "x point bonus and earned ", pointsEarned, " points!")
            else: # the user's last guess
                print("Correct guess! You earned " + str(pointsEarned) + " points!")

            score += pointsEarned
            break
        else: # user makes an incorrect guess
            dispIncGuessFeedback(userGuess, randNumInRange, curGuessesRemaining)
        
        curGuessesRemaining -= 1
    
    print()
    print()

    curRoundIndex = curRoundIndex + 1


print("Thanks for playing! Your final score is " + str(score) + " points!")
print()
print()


# Update boolean flag if the user did NOT qualify for the leaderboard
if(len(leaderboardEntries) == maxNumPlayersOnLeaderboard):
    if(score <= leaderboardEntries[maxNumPlayersOnLeaderboard - 1].score):
        qualifiedForLeaderboard = False


if(qualifiedForLeaderboard):
    leaderboardUpdates()
    print("Your score qualified you for the leaderboard!")
    print()
    dispLeaderboard()

  
print("Goodbye.")