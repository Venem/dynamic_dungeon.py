#!/usr/bin/env python3

# we need random numbers for the boss fights
from random import randint
# we need to wait for a couple of seconds for the dragon fight at the end
from time import sleep
# this is for clearing the screen
from os import system, name

# the positioning system is a bit weird because of the 2d array thing, keep that in mind when changing the code
position = []
layout = []
discoveredRooms = [[]]
defeatedBosses = []
treasuresStolen = []

# \/ this is self-explanatory
gold = 0
health = 100

# initialise and get layout from file
def initLevel():
    tmpLayout = []
    # open file - when just using the filename, you have to run the game from the same folder as the layout and score. On linux and mac, if the game is in your $PATH, you need to use the full path of the layout file. This applies for the scores file.
    dungeon = open("layout.txt", "r")
    # separate lines into array and remove commented out lines
    for line in dungeon:
        if "#" in line:
            continue
        # █ character on windows messes up formatting, so we leave it as +
        if name != "nt":
            tmpLayout.append(line.replace("\n", "").replace("+", "█"))
        else:
            tmpLayout.append(line.replace("\n", ""))
    # put dungeon layout in 2d array
    for i in range(len(tmpLayout)):
        layout.append([])
        for char in tmpLayout[i]:
            layout[i].append(char)

# scans the whole map to find the start point
def findStart():
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            if layout[i][j] == "S":
                position.append(i)
                position.append(j)
                discoveredRooms[0].append(position[0])
                discoveredRooms[0].append(position[1])
                return

# checks to see if there is a room at the coordinates passed in
def isRoom(y, x):
    if y < 0:
        return False
    if x < 0:
        return False
    elif len(layout) <= y:
        return False
    elif len(layout[y]) <= x:
        return False
    elif str(layout[y][x]) == " ":
        return False
    else:
        return True

# same thing as printMyRoom() but useful in different situations
def roomType(y, x):
    roomType = layout[y][x]

    if roomType == "S":
        return("the start")
    elif roomType == "█":
        return("a room")
    elif roomType == "B":
        return("a boss room")
    elif roomType == "T":
        return("a treasure room")
    elif roomType == "D":
        return("the dragon room")


# find the rooms around the current position which is passed in as a argument
def findRooms(y, x):
    rooms = []
    roomsCounter = 0

    # room on the left
    if isRoom(y, x - 1):
        rooms.append([])
        rooms[roomsCounter].append(y)
        rooms[roomsCounter].append(x - 1)
        roomsCounter = roomsCounter + 1
        print("\033[0;90m - \033[0;00mYou can go \033[0;36;4mleft\033[0;00m to", roomType(y, x - 1))
    # room on the right
    if isRoom(y, x + 1):
        rooms.append([])
        rooms[roomsCounter].append(y)
        rooms[roomsCounter].append(x + 1)
        roomsCounter = roomsCounter + 1
        print("\033[0;90m - \033[0;00mYou can go \033[0;36;4mright\033[0;00m to", roomType(y, x + 1))
    # room up
    if isRoom(y - 1, x):
        rooms.append([])
        rooms[roomsCounter].append(y - 1)
        rooms[roomsCounter].append(x)
        roomsCounter = roomsCounter + 1
        print("\033[0;90m - \033[0;00mYou can go \033[0;36;4mup\033[0;00m to", roomType(y - 1, x))
    # room down
    if isRoom(y + 1, x):
        rooms.append([])
        rooms[roomsCounter].append(y + 1)
        rooms[roomsCounter].append(x)
        roomsCounter = roomsCounter + 1
        print("\033[0;90m - \033[0;00mYou can go \033[0;36;4mdown\033[0;00m to", roomType(y + 1, x))

    # add discovered rooms into an array, useful later on for map display
    for i in rooms:
        if i not in discoveredRooms:
            discoveredRooms.append(i)

# very important function, this actually moves you to a direction. a later addition: it can run a couple of commands such as "gold" to show the player how much gold they have
def move(direction):
    global position
    global automap

    clear()

    if direction.lower() == "left" or direction.lower() == "l" and isRoom(position[0], position[1] - 1):
        position = [position[0], position[1] - 1]
    elif direction.lower() == "right" or direction.lower() == "r" and isRoom(position[0], position[1] + 1):
        position = [position[0], position[1] + 1]
    elif direction.lower() == "up" or direction.lower() == "u" and isRoom(position[0] - 1, position[1]):
        position = [position[0] - 1, position[1]]
    elif direction.lower() == "down" or direction.lower() == "d" and isRoom(position[0] + 1, position[1]):
        position = [position[0] + 1, position[1]]
    elif direction.lower() == "gold" or direction.lower() == "g":
        print("\033[0;33mYou have", gold, "gold\033[0;00m")
    elif direction.lower() == "health" or direction.lower() == "hp":
        print("\033[0;31mYou have", health, "hp\033[0;00m")
    elif direction.lower() == "scores" or direction.lower() == "s":
        showScores()
    elif direction.lower() == "help" or direction == "?":
        showHelp()
    elif direction.lower() == "q":
        exit()
    else:
        print("\033[0;91mThere is no such room\033[0;00m")

# looks at your coordinates and tells you what room you're in
def printMyRoom():
    roomType = layout[position[0]][position[1]]

    print("\033[0;35;1m", end="")
    if roomType == "S":
        print("You are at the start")
    elif roomType == "█":
        print("You are in a room")
    elif roomType == "B":
        print("You are in a boss room")
        bossFight()
    elif roomType == "T":
        print("You are in a treasure room")
        giveTreasure()
    elif roomType == "D":
        print("You are in the dragon room")
        dragonFight()
    print("\033[0;00m", end="")

# this is only used in the function below
def isMatch(i, j, sortedMap):
    for k in range(len(sortedMap)):
        if i == sortedMap[k][0] and j == sortedMap[k][1]:
            return True

# some wizardry I spent 3 hours on; shows a map of rooms the player has discovered
def showMap():
    sortedMap = sorted(discoveredRooms)
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            print("\033[0;90m", end="")
            if isMatch(i, j, sortedMap) and i == position[0] and j == position[1]:
                print("\033[0;31;1m", end="")
            if isMatch(i, j, sortedMap):
                print(layout[i][j], end="")
                print("\033[0;00m", end="")
            else:
                print(" ", end="")
        if i <= sortedMap[-1][0] and (i + 1) >= sortedMap[0][0]:
            print()
    print("\033[0;00m")

# help menu
def showHelp():
    print("\033[0;90;1mHow to play the game:\033[0;00m")
    print("\033[0;90m - \033[0;00mYou are in a dungeon, collect as much gold as possible")
    print("\033[0;90m - \033[0;00mDo this by fighting bosses and raiding treasure rooms")
    print("---")
    print("\033[0;90;1mCOMMANDS:\033[0;00m")
    print("\033[0;90m - \033[0;00mup, down, right, left to move to the respective direction")
    print("\033[0;90m - \033[0;00mg or gold to show the amount of gold you have")
    print("\033[0;90m - \033[0;00mhp or health to show the amount of health you have")
    print("\033[0;90m - \033[0;00ms or scores to show previous scores")
    print("\033[0;90m - \033[0;00m? or help for this menu")
    print("\033[0;90m - \033[0;00mq to quit")

def giveTreasure():
    global gold

    if position in treasuresStolen:
        print("\033[0;36mYou have already stolen this treasure\033[0;00m")
        return

    goldToGive = randint(10, randint(20, 500))
    print("\033[0;33mYou gained", goldToGive, "gold!\033[0;00m")
    gold = gold + goldToGive
    treasuresStolen.append(position)

# boss fight: boss picks a random number, player tries to guess number. depending on how close guess is we determine how much damage the player takes.
def bossFight():
    global health

    if position in defeatedBosses:
        print("\033[0;36mYou have already killed this boss\033[0;00m")
        return

    bossNum = randint(1, 100)

    while True:
        print("\033[0;00m", end="")
        myGuess = input("\033[0;36mThe boss offers to let you go past if you guess its secret number (1-100): \033[0;00m")

        try:
            myGuess = int(myGuess)
        except ValueError :
            print("\033[0;31mThe boss wants a valid number\033[0;00m")
            continue

        if myGuess <= 100 and myGuess >= 1:
            break
        else:
            print("\033[0;31mThe boss wants a valid number\033[0;00m")
            continue

    if bossNum < myGuess:
        difference = myGuess - bossNum
    elif bossNum > myGuess:
        difference = bossNum - myGuess
    elif bossNum == myGuess:
        difference = 0
        print("\033[0;36mYou guessed its number, you can go past\033[0;00m")

    damage = round((100 - difference) * (difference / 32), 0)
    print("\033[0;31mYou lost", damage, "health!\033[0;00m")
    health = health - int(damage)
    if health < 0:
        print("\033[0;31;1mYou died\033[0;00m")
        exit()
    defeatedBosses.append(position)

# the final boss fight, you can either get more gold for defeating it but have a lower chance to kill it or get less gold but have a higher chance to kill it
def dragonFight():
    global health
    global gold

    while True:
        print("\033[0;00m", end="")
        choice = input("\033[0;36mThe Dragon gives you two choices:\n(1) Get paid 8 gold per health (33% chance of winning fight)\n(2) Get paid 2 gold per health (66% chance of winning fight): \033[0;00m")

        try:
            choice = int(choice)
        except ValueError :
            print("\033[0;31mThe dragon wants a valid choice\033[0;00m")
            continue

        if choice == 1:
            goldToGive = health * 8
            print("\033[0;33mYou gained", goldToGive, "gold!\033[0;00m", end="")
            gold = gold + goldToGive
            health = 1

            sleep(0.5)

            print()

            print("\033[0;35mFighting Dragon\033[0;00m", end="")

            sleep(1)

            print()

            # approx 33% chance to win
            if randint(0, health) < health / 3:
                print("\033[0;34mYou killed the dragon!\033[0;00m")
                print("\033[0;33mYou got a total of", gold, "gold!\033[0;00m")
                initials = input("Saving score. Please enter your initials: ")
                writeScore(gold, initials)
                exit()
            else:
                print("\033[0;31mYou were killed by the dragon\033[0;00m")
                exit()

        elif choice == 2:

            print("\033[0;35mFighting Dragon\033[0;00m", end="")

            sleep(1)

            print()

            # approx 66% chance to win
            if randint(0, health) > health / 3:
                print("\033[0;34mYou killed the dragon!\033[0;00m")

                sleep(0.5)

                print("Converting \033[0;31mhearts\033[0;00m into \033[0;33mgold\033[0;00m")

                sleep(0.5)

                gold = gold + (health * 2)

                print("\033[0;33mYou got a total of", gold, "gold!\033[0;00m")
                initials = input("Saving score. Please enter your initials: ")
                writeScore(gold, initials)
                exit()
            else:
                print("\033[0;31mYou were killed by the dragon\033[0;00m")
                exit()
        else:
            print("\033[0;31mThe dragon wants a valid choice\033[0;00m")
            continue

# save the player's score
def writeScore(gold, initials):
    with open("scores.txt", "a") as scores:
        scores.write(str(gold) + "\t\t" + initials + "\n")

def showScores():
    scoresStore = []
    sortedScores = []
    scores = open("scores.txt", "r")

    # some wizardry to sort the scores
    for line in scores:
        scoresStore.append(line.split("\t\t"))
        scoresStore[-1][0] = int(scoresStore[-1][0])

    sortedScores = sorted(scoresStore, reverse=True)

    for i in range(len(sortedScores)):
        print("\033[0;93;1m" + str(i + 1) + ". " + "\033[0;00m\033[0;94m" + str(sortedScores[i][0]) + "\t\t" + sortedScores[i][1] + "\033[0;00m", end="")

# to clear screen
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# start the game
clear()
initLevel()
findStart()
while True:
    print("---")
    printMyRoom()
    findRooms(position[0], position[1])
    print("---")
    showMap()
    print("~~~")
    print("(? for help): \033[0;32m", end="")
    move(input())
    print("\033[0;00m", end="")
input()
