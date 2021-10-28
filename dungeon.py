#!/usr/bin/env python3

# IMPORTANT MEGA TODO: make it so that you can do "10r" and still discover rooms around you

# we need random numbers for the boss fights
from random import randint
# we need to wait for a couple of seconds for the dragon fight at the end
from time import sleep
# this is for clearing the screen
from os import system, name

# colours
E           = "m"
S           = "\033[0"
RESET       = "\033[0;00m"
BOLD        = ";1"
UNDERLINE   = ";4"
RED         = ";31"
GREEN       = ";32"
YELLOW      = ";33"
BLUE        = ";34"
MAGENTA     = ";35"
CYAN        = ";36"
WHITE       = ";37"
GREY        = ";90"
LRED        = ";91"
LGREEN      = ";92"
LYELLOW     = ";93"
LBLUE       = ";94"
LMAGENTA    = ";94"
LCYAN       = ";94"
LWHITE      = ";94"

# the positioning system is a bit weird because of the 2d array thing, keep that in mind when changing the code
position = []
layout = []
discoveredRooms = [[]]
defeatedBosses = []
treasuresStolen = []

# declare gold and health variables
gold = 0
health = 100

# initialise, get layout from file and find start
def initLevel():
    global layout
    dungeon = open("layout.txt", "r")
    i = 0
    for line in dungeon:
        if "#" in line: continue
        layout.append([])

        if name != "nt":
            line = line.replace("\n", "").replace("+", "█")
        else:
            line = line.replace("\n", "")

        for j in range(len(line)):
            layout[i].append(line[j])
            if layout[i][j] == "S":
                position.append(i)
                position.append(j)
                discoveredRooms[0].append(position[0])
                discoveredRooms[0].append(position[1])
        i+=1

# checks to see if there is a room at the coordinates passed in
def isRoom(y, x):
    if y < 0 or x < 0 or len(layout) <= y or len(layout[y]) <= x or str(layout[y][x]) == " ":
        return False
    else:
        return True

# TODO: merge with printMyRoom()?
# same thing as printMyRoom() but useful in different situations
def roomType(y, x):
    roomType = layout[y][x]

    if roomType == "S":
        return("the start")
    elif roomType == "█" or roomType == "+":
        return("a room")
    elif roomType == "B":
        return("a boss room")
    elif roomType == "T":
        return("a treasure room")
    elif roomType == "D":
        return("the dragon room")

# TODO: if statements are painfully repetitive
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
        print(S+GREY+E + " - " + RESET + "You can go " + S+CYAN+UNDERLINE+E + "left" + RESET + " to", roomType(y, x - 1))
    # room on the right
    if isRoom(y, x + 1):
        rooms.append([])
        rooms[roomsCounter].append(y)
        rooms[roomsCounter].append(x + 1)
        roomsCounter = roomsCounter + 1
        print(S+GREY+E + " - " + RESET + "You can go " + S+CYAN+UNDERLINE+E + "right" + RESET + " to", roomType(y, x + 1))
    # room up
    if isRoom(y - 1, x):
        rooms.append([])
        rooms[roomsCounter].append(y - 1)
        rooms[roomsCounter].append(x)
        roomsCounter = roomsCounter + 1
        print(S+GREY+E + " - " + RESET + "You can go " + S+CYAN+UNDERLINE+E + "up" + RESET + " to", roomType(y - 1, x))
    # room down
    if isRoom(y + 1, x):
        rooms.append([])
        rooms[roomsCounter].append(y + 1)
        rooms[roomsCounter].append(x)
        roomsCounter = roomsCounter + 1
        print(S+GREY+E + " - " + RESET + "You can go " + S+CYAN+UNDERLINE+E + "down" + RESET + " to", roomType(y + 1, x))

    # TODO: clean up for loop
    # add discovered rooms into an array, useful later on for map display
    for i in rooms:
        if i not in discoveredRooms:
            discoveredRooms.append(i)

# very important function, this actually moves you to a direction. a later addition: it can run a couple of commands such as "gold" to show the player how much gold they have
def move(direction):
    global position
    global automap

    timesToMove = 1
    numberLen = 0
    clear()

    # allows to run e.g 4r to go 4 to the right
    for i in range(len(direction)):
        if direction[i].isnumeric():
            numberLen = i

    if direction[:numberLen+1].isnumeric():
        timesToMove = int(direction[:numberLen+1])
        direction = direction[numberLen+1:]

    # TODO: get a second opinion on this
    if direction.lower() == "left" or direction.lower() == "l" \
    and isRoom(position[0], position[1] - timesToMove):
        position = [position[0], position[1] - timesToMove]
        for i in range(timesToMove):
            incrementalPos = [position[0], position[1] + i]
            if incrementalPos not in discoveredRooms:
                discoveredRooms.append(incrementalPos)
    elif direction.lower() == "right" or direction.lower() == "r" \
    and isRoom(position[0], position[1] + timesToMove):
        position = [position[0], position[1] + timesToMove]
        for i in range(timesToMove):
            incrementalPos = [position[0], position[1] - i]
            if incrementalPos not in discoveredRooms:
                discoveredRooms.append(incrementalPos)
    elif direction.lower() == "up" or direction.lower() == "u" \
    and isRoom(position[0] - timesToMove, position[1]):
        position = [position[0] - timesToMove, position[1]]
        for i in range(timesToMove):
            incrementalPos = [position[0] - i, position[1]]
            if incrementalPos not in discoveredRooms:
                discoveredRooms.append(incrementalPos)
    elif direction.lower() == "down" or direction.lower() == "d" \
    and isRoom(position[0] + timesToMove, position[1]):
        position = [position[0] + timesToMove, position[1]]
        for i in range(timesToMove):
            incrementalPos = [position[0] + i, position[1]]
            if incrementalPos not in discoveredRooms:
                discoveredRooms.append(incrementalPos)
    else:
        if direction.lower() == "gold" or direction.lower() == "g":
            print(S+YELLOW+E + "You have", gold, "gold" + RESET)
        elif direction.lower() == "health" or direction.lower() == "hp":
            print(S+RED+E + "You have", health, "hp" + RESET)
        elif direction.lower() == "scores" or direction.lower() == "s":
            showScores()
        elif direction.lower() == "help" or direction == "?":
            showHelp()
        elif direction.lower() == "q":
            exit()
        else:
            print(S+LRED+E + "Command not executed: wrong syntax or direction out of range." + RESET)

# TODO: merge with roomType()?
# looks at your coordinates and tells you what room you're in
def printMyRoom():
    roomType = layout[position[0]][position[1]]

    print(S+MAGENTA+BOLD+E, end="")
    if roomType == "S":
        print("You are at the start")
    elif roomType == "█" or roomType == "+":
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
    print(RESET, end="")

# TODO: work out what on earth this does and simplify
# this is only used in the function below
def isMatch(i, j, sortedMap):
    for k in range(len(sortedMap)):
        if i == sortedMap[k][0] and j == sortedMap[k][1]:
            return True

# TODO: same applies here as above. I mean this is painful to read
# some wizardry I spent 3 hours on; shows a map of rooms the player has discovered
def showMap():
    sortedMap = sorted(discoveredRooms)
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            print(S+GREY+E, end="")
            if isMatch(i, j, sortedMap) and i == position[0] and j == position[1]:
                print(S+RED+BOLD+E, end="")
            if isMatch(i, j, sortedMap):
                print(layout[i][j], end="")
                print(RESET, end="")
            else:
                print(" ", end="")
        if i <= sortedMap[-1][0] and (i + 1) >= sortedMap[0][0]:
            print()
    print(RESET)

# help menu
def showHelp():
    print(
            S+GREY+BOLD+E + "How to play the game:" + RESET + "\n" +
            S+GREY+E + " - " + RESET + "You are in a dungeon, collect as much gold as possible" + "\n" +
            S+GREY+E + " - " + RESET + "Do this by fighting bosses and raiding treasure rooms" + "\n" +
            "---" + "\n" +
            S+GREY+BOLD+E + "COMMANDS:" + RESET + "\n" +
            S+GREY+E + " - " + RESET + "up, down, right, left to move to the respective direction" + "\n" +
            S+GREY+E + " - " + RESET + "You can also type the first letter to move (u,d,r,l)" + "\n" +
            S+GREY+E + " - " + RESET + "You can move in the same direction multiple times (e.g: 4left)\nbut there are some drawbacks such as not discovering rooms around you" + "\n" +
            S+GREY+E + " - " + RESET + "g or gold to show the amount of gold you have" + "\n" +
            S+GREY+E + " - " + RESET + "hp or health to show the amount of health you have" + "\n" +
            S+GREY+E + " - " + RESET + "s or scores to show previous scores" + "\n" +
            S+GREY+E + " - " + RESET + "? or help for this menu" + "\n" +
            S+GREY+E + " - " + RESET + "q to quit"
        )

def giveTreasure():
    global gold
    # if treasure is already stolen, return
    if position in treasuresStolen:
        print(S+CYAN+E + "You have already stolen this treasure" + RESET)
        return
    goldToGive = randint(10, randint(20, 500))
    print(S+YELLOW+E + "You gained", goldToGive, "gold!" + RESET)
    gold = gold + goldToGive
    treasuresStolen.append(position)

# boss fight: boss picks a random number, player tries to guess number. depending on how close guess is we determine how much damage the player takes.
def bossFight():
    global health
    if position in defeatedBosses:
        print(S+CYAN+E + "You have already killed this boss" + RESET)
        return

    bossNum = randint(1, 100)
    validValue = False
    while not validValue:
        print(RESET, end="")
        myGuess = input(S+CYAN+E + "The boss offers to let you go past if you guess its secret number (1-100): " + RESET)

        if not myGuess.isnumeric():
            print(S+RED+E + "The boss wants a valid number" + RESET)
            continue
        # try:
        #     myGuess = int(myGuess)
        # except ValueError :
        #     print(S+RED+E + "The boss wants a valid number" + RESET)
        #     continue

        if myGuess <= 100 and myGuess >= 1:
            validValue = True
        else:
            print(S+RED+E + "The boss wants a valid number" + RESET)
            continue

    if bossNum < myGuess:
        difference = myGuess - bossNum
    elif bossNum > myGuess:
        difference = bossNum - myGuess
    elif bossNum == myGuess:
        difference = 0
        print(S+CYAN+E + "You guessed its number, you can go past" + RESET)

    damage = round((100 - difference) * (difference / 32)/2, 0)
    print(S+RED+E + "You lost", damage, "health!" + RESET)
    health = health - int(damage)
    if health < 0:
        print(S+RED+BOLD+E + "You died" + RESET)
        exit()
    defeatedBosses.append(position)

# TODO: geez this was rushed... Throw it all out and redo fight
# the final boss fight, you can either get more gold for defeating it but have a lower chance to kill it or get less gold but have a higher chance to kill it
def dragonFight():
    global health
    global gold

    while True:
        print(RESET, end="")
        choice = input(S+CYAN+E + "The Dragon gives you two choices:\n(1) Get paid 8 gold per health (33% chance of winning fight)\n(2) Get paid 2 gold per health (66% chance of winning fight): " + RESET)

        try:
            choice = int(choice)
        except ValueError :
            print(S+RED+E + "The dragon wants a valid choice" + RESET)
            continue

        if choice == 1:
            goldToGive = health * 8
            print(S+YELLOW+E + "You gained", goldToGive, "gold!" + RESET, end="")
            gold = gold + goldToGive
            health = 1

            sleep(0.5)

            print()

            print(S+MAGENTA+E + "Fighting Dragon" + RESET, end="")

            sleep(1)

            print()

            # approx 33% chance to win
            if randint(0, health) < health / 3:
                print(S+BLUE+E + "You killed the dragon!" + RESET)
                print(S+YELLOW+E + "You got a total of", gold, "gold!" + RESET)
                initials = input("Saving score. Please enter your initials: ")
                writeScore(gold, initials)
                exit()
            else:
                print(S+RED+E + "You were killed by the dragon" + RESET)
                exit()

        elif choice == 2:

            print(S+MAGENTA+E + "Fighting Dragon" + RESET, end="")

            sleep(1)

            print()

            # approx 66% chance to win
            if randint(0, health) > health / 3:
                print(S+BLUE+E + "You killed the dragon!" + RESET)

                sleep(0.5)

                print("Converting " + S+RED+E + "hearts" + RESET + " into " + S+YELLOW+E + "gold" + RESET)

                sleep(0.5)

                gold = gold + (health * 2)

                print(S+YELLOW+E + "You got a total of", gold, "gold!" + RESET)
                initials = input("Saving score. Please enter your initials: ")
                writeScore(gold, initials)
                exit()
            else:
                print(S+RED+E + "You were killed by the dragon" + RESET)
                exit()
        else:
            print(S+RED+E + "The dragon wants a valid choice" + RESET)
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
        # TODO: this will look messed up if name is too long
        scoresStore.append(line.split("\t\t"))
        # TODO: wow this is janky af
        scoresStore[-1][0] = int(scoresStore[-1][0])

    sortedScores = sorted(scoresStore, reverse=True)

    for i in range(len(sortedScores)):
        print(S+LYELLOW+BOLD+E + str(i + 1) + ". " + RESET + S+LBLUE+E + str(sortedScores[i][0]) + "\t\t" + sortedScores[i][1] + RESET, end="")

# to clear screen
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# start the game
clear()
initLevel()
while True:
    print("---")
    printMyRoom()
    findRooms(position[0], position[1])
    print("---")
    showMap()
    print("~~~")
    print("(? for help): " + S+GREEN+E, end="")
    move(input())
    print(RESET, end="")
input()
