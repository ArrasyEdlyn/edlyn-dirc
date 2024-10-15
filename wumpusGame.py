import random

# Initialize the map array.
world = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

# Hide the wumpus (w).
row = random.randint(1, 4)
col = random.randint(1, 4)
world[row][col] = 'w'


def existance(uRow, uCol):
    if uRow >= 0 and uCol >= 0 and uRow <= 4 and uCol <= 4:
        return True
    else:
        return False


# Hide the pit (1).
needit = True
while needit:
    row = random.randint(1, 3)
    col = random.randint(1, 3)
    if world[row][col] == 0:
        world[row][col] = 'p1'
        needit = False

# Hide the pit (2)
needit1 = True
while needit1:
    row = random.randint(1, 4)
    col = random.randint(1, 4)
    if world[row][col] == 0:
        world[row][col] = 'p0'
        needit1 = False

# Hide the Gold
needit2 = True
while needit2:
    row = random.randint(1, 4)
    col = random.randint(1, 4)
    if world[row][col] == 0:
        world[row][col] = 'G'
        needit2 = False

# Initialize variables
arrows = 1
alive = True
userCol = 0
userRow = 0
usermoves = 0
Gold = False

# print(world)
while alive:

    # Tell user where he is.
    print('You are at row ' + str(userRow) + ' and col ' + str(userCol) + '.')

    # Tells user if he is near the wumpus
    if (existance(userRow - 1, userCol) == True and world[userRow - 1][userCol] == 'w') or (
            existance(userRow + 1, userCol) == True and world[userRow + 1][userCol] == 'w') or (
            existance(userRow, userCol - 1) == True and world[userRow][userCol - 1] == 'w') or (
            existance(userRow, userCol + 1) and world[userRow][userCol + 1] == 'w'):
        print('I smell a Wumpus...  ')

    # Tells user if he is near a pit
    if (existance(userRow - 1, userCol) == True and (
            world[userRow - 1][userCol] == 'p1' or world[userRow - 1][userCol] == 'p0')) or (
            existance(userRow + 1, userCol) == True and (
            world[userRow + 1][userCol] == 'p1' or world[userRow + 1][userCol] == 'p0')) or (
            existance(userRow, userCol - 1) == True and (
            world[userRow][userCol - 1] == 'p1' or world[userRow][userCol - 1] == 'p0')) or (
            existance(userRow, userCol + 1) and (
            world[userRow][userCol + 1] == 'p1' or world[userRow][userCol + 1] == 'p0')):
        print('I feel a breeze...  ')

    # Ask user what to do next (n/s/e/w/f).
    print('What do you want to do next?')
    print('You can type "north", "south", "east", or "west" to move, or "fire" to fire an arrow.')
    action = input()

    # If direction, move
    if action == 'north':
        if userRow != 4:
            userRow = userRow + 1
            usermoves += 1
            if userRow == 0 and userCol == 0 and Gold == True:
                print("You win in " + str(usermoves) + " moves.")
                alive = False
        else:
            print("Oops!You walk off the face of the Earth.Try again...")
    if action == 'south':
        if userRow != 0:
            userRow = userRow - 1
            usermoves += 1
            if userRow == 0 and userCol == 0 and Gold == True:
                print("You win in " + str(usermoves) + " moves.")
                alive = False
        else:
            print("Oops!You walk off the face of the Earth.Try again...")
    if action == 'east':
        if userCol != 0:
            userCol = userCol - 1
            usermoves += 1
            if userRow == 0 and userCol == 0 and Gold == True:
                print("You win in " + str(usermoves) + " moves.")
                alive = False
        else:
            print("Oops!You walk off the face of the Earth.Try again...")
    if action == 'west':
        if userCol != 4:
            userCol = userCol + 1
            usermoves += 1
            if userRow == 0 and userCol == 0 and Gold == True:
                print("You win in " + str(usermoves) + " moves.")
                alive = False
        else:
            print("Oops!You walk off the face of the Earth.Try again...")

    # If wumpus then user dies.
    if world[userRow][userCol] == 'w':
        print('Chomp, chomp, chomp, you are dinner...')
        alive = 0

    # If pit then user dies.
    if world[userRow][userCol] == 'p1' or world[userRow][userCol] == 'p0':
        print('"Aaaaaaaaaah," you scream as you fall to your death.')
        alive = 0

    # If user find the gold.
    if world[userRow][userCol] == 'G':
        print('Wow you find the gold you can came back home')
        Gold = True

    # Arrow/Shooting Stuff

    if action == 'fire' and arrows != 0:
        print(
            'Which direction do you want to fire?\nyou can type "fire north","fire south","fire east",or "fire west" to choose a direction.')
        flight = input()
        # Check if the arrow hit the wumpus.
        if flight == 'fire north':
            arrows = 0
            wumpusdie = False
            arrowRow = userRow + 1
            arrowCol = userCol
            for i in range(userRow, 4):
                if world[i][arrowCol] == "w":
                    print("Congradulation!you killed the Wumpus")
                    world[i][arrowCol] = 0
                    wumpusdie = True

            if wumpusdie == False:
                print("Oops!you lost your chance:(")
        if flight == 'fire east':
            arrows = 0
            wumpusdie = False
            arrowRow = userRow
            arrowCol = userCol - 1
            for i in range(0, userCol):
                if world[arrowRow][i] == "w":
                    print("Congradulation!you killed the Wumpus")
                    world[arrowRow][i] = 0
                    wumpusdie = True

            if wumpusdie == False:
                print("Oops!you lost your chance:(")

        if flight == 'fire south':
            arrows = 0
            wumpusdie = False
            arrowRow = userRow - 1
            arrowCol = userCol
            for i in range(0, userRow):
                if world[i][arrowCol] == "w":
                    print("Congradulation!you killed the Wumpus")
                    world[i][arrowCol] = 0
                    wumpusdie = True

            if wumpusdie == False:
                print("Oops!you lost your chance:(")
        if flight == 'fire west':
            arrows = 0
            wumpusdie = False
            arrowRow = userRow
            arrowCol = userCol + 1
            for i in range(userCol, 4):
                if world[arrowRow][i] == "w":
                    print("Congradulation!you killed the Wumpus")
                    world[arrowRow][i] = 0
                    wumpusdie = True

            if wumpusdie == False:
                print("Oops!you lost your chance:(")

    elif action == "fire" and arrows == 0:
        print("Oh!You don't have any arrow!")
