import os
import sys
import copy

verbose = 0
BOARD_SIZE = 10

def clear_board():
    if verbose > 0: print "clear_board()"
    b = []
    if verbose > 0: print "b:"
    if verbose > 0: print b
    for i in range(0, BOARD_SIZE):
        if verbose > 0: print "i:", i
        b.append(["O"] * BOARD_SIZE)
        if verbose > 0: print "b[i]:", b[i]
    return b

def print_board(b):
    if verbose > 0: print "print_board(b)"
    if verbose > 0: print "B:"
    if verbose > 0: print b
    for row in range(0, BOARD_SIZE + 1):
        if verbose > 0: print "Row:", row
        r = []
        if(row == 0):
            if verbose > 0: print "First Row, Header"
            r = [" "]
            for i in range(0, BOARD_SIZE):
                r.append(i)
        else:
            if verbose > 0: print "Row Index", row-1
            if verbose > 0: print "Row",b[row-1]
            r = [row-1]
            r += b[row-1]
        print " | ".join(str(n) for n in r)

def place_ship(ship, board):
    if(ship["placed"] == True):
        print("Ship",ship["name"],"has already been placed")
        print(ship["bow"],"->",ship["stern"])
    startX = -1
    startY = -1
    print_board(board)
    while (startX < 0 or startY < 0):
        try:
            startX = int(raw_input("Start Column: "))
            startY = int(raw_input("Start Row: "))
        except:
            print("Invalid Input")
            startX = -1
            startY = -1
            continue
        if(startX < 0 or startX >= BOARD_SIZE or startY < 0 or startY >= BOARD_SIZE):
            print "Ship off the board"
            startX = -1
            startY = -1
        elif(board[startY][startX] != "O"):
            print startX,",",startY,"is occupied!",board[startY][startX]
            startX = -1
            startY = -1
    d = ""
    while(len(d) == 0):
        try:
            d = str(raw_input("Direction? (N, E, S, W): "))[0].upper()
        except:
            print("Invalid Input")
            d = ""
            continue
        if verbose > 0: print "D:", d
        if(d != "N" and d != "E" and d != "S" and d != "W"):
            d = ""
        else:
            x = 0
            y = 0
            if d == "N":
                y -= ship["size"]-1
            elif d == "E":
                x += ship["size"]-1
            elif d == "S":
                y += ship["size"]-1
            elif d == "W":
                x -= ship["size"]-1
            else:
                d = ""
                continue
            endX = startX + x
            endY = startY + y
            if(endX < 0 or endX >= BOARD_SIZE or endY < 0 or endY >= BOARD_SIZE):
                print "Ship off the board"
                d = ""
                continue
            else:
                if verbose > 0: print "START:",startX,",",startY
                if verbose > 0: print "END:",endX,",",endY
                ship["bow"] = [startX, startY]
                ship["stern"] = [endX, endY]
                if(not deploy_ship(ship, board)): d = ""

def remove_ship(ship, board):
    if(verbose > 0): print "remove_ship(",ship["name"],")"
    startX = ship["bow"][0]
    endX = ship["stern"][0]
    startY = ship["bow"][1]
    endY = ship["stern"][1]
    rX = []
    rY = []
    if(startX == endX): rX.append(startX)
    elif(startX < endX): rX = range(startX, endX+1)
    else: rX = range(endX, startX+1)
    if(startY == endY): rY.append(startY)
    elif(startY < endY): rY = range(startY, endY+1)
    else: rY = range(endY, startY+1)

    for i in rX:
        for j in rY:
            board[j][i] = "O"
    ship["bow"] = [-1, -1]
    ship["stern"] = [-1, -1]
    ship["placed"] = False

def deploy_ship(ship, board):
    startX = ship["bow"][0]
    endX = ship["stern"][0]
    startY = ship["bow"][1]
    endY = ship["stern"][1]
    rX = []
    rY = []
    if(startX == endX): rX.append(startX)
    elif(startX < endX): rX = range(startX, endX+1)
    else: rX = range(endX, startX+1)
    if verbose > 0: print "rX:",rX

    if(startY == endY): rY.append(startY)
    elif(startY < endY): rY = range(startY, endY+1)
    else: rY = range(endY, startY+1)
    if verbose > 0: print "rY:",rY

    for i in rX:
        for j in rY:
            if verbose > 0: print j,",",i,":",board[j][i]
            if board[j][i] != "O":
                print "Fleet",j,",",i,"occupied!",board[j][i]
                remove_ship(ship)
                return False
            else:
                board[j][i] = ship["name"][0]
                if verbose > 0: print board[j][i]
    ship["placed"] = True
    return True

def attack(atk, pos, enm):
    aX = -1
    aY = -1
    retVal = 0
    while(aX < 0 or aY < 0):
        print_board(atk)
        try:
            aX = int(raw_input("Attack Col? "))
            aY = int(raw_input("Attack Row? "))
        except:
            print("Invalid Input")
            aX = -1
            aY = -1
            continue

        if(aX < 0 or aX >= BOARD_SIZE or aY < 0 or aY >= BOARD_SIZE):
            print("Attack is off the board")
            aX = -1
            aY = -1
            continue
        else:
            p = pos[aY][aX]

        if(p != "O" and p != "H" and p != "m"):
            print "HIT"
            atk[aY][aX] = "H"
            ship = {}
            if(p == "B"):
                ship = enm["battleship"]
            elif(p == "A"):
                ship = enm["carrier"]
            elif(p == "D"):
                ship = enm["destroyer"]
            elif(p == "F"):
                ship = enm["frigate"]
            ship["hits"] += 1
            if(ship["hits"] >= ship["size"]):
                print "You sunk the enemy",ship["name"]
                ship["sunk"] = True
            pos[aY][aX] = "H"
            retVal = 1
        elif(p == "H" or p == "m"):
            print "You Already Attacked There"
            aX = -1
            aY = -1
        else:
            print "MISS"
            atk[aY][aX] = "m"
            pos[aY][aX] = "m"
            retVal = 0

    print_board(atk)
    return retVal
def endGame(fleet):
    if verbose > 0: print "endGame(fleet)"
    shipsRemaining = len(fleet)
    if verbose > 0: print "R:",shipsRemaining
    for s in fleet:
        if verbose > 0: print s,fleet[s],fleet[s]["sunk"]
        if(fleet[s]["sunk"]):
            shipsRemaining -= 1
            if verbose > 0: print shipsRemaining
    if verbose > 0: print shipsRemaining
    return shipsRemaining <= 0

ships = {
    "battleship": {
        "name": "Battleship",
        "size": 5,
        "bow": [-1,-1],
        "stern": [-1,-1],
        "hits": 0,
        "placed": False,
        "sunk": False
    },
    "carrier": {
        "name": "Aircraft Carrier",
        "size": 4,
        "bow": [-1,-1],
        "stern": [-1,-1],
        "hits": 0,
        "placed": False,
        "sunk": False
    },
    "destroyer": {
        "name": "Destroyer",
        "size": 3,
        "bow": [-1,-1],
        "stern": [-1,-1],
        "hits": 0,
        "placed": False,
        "sunk": False
    },
    "frigate": {
        "name": "Frigate",
        "size": 2,
        "bow": [-1,-1],
        "stern": [-1,-1],
        "hits": 0,
        "placed": False,
        "sunk": False
    }
}

p1Fleet = copy.deepcopy(ships)
p2Fleet = copy.deepcopy(ships)
p1Deploy = clear_board()
p1Attack = clear_board()
p2Deploy = clear_board()
p2Attack = clear_board()
if verbose > 0:
    print p1Fleet
    print p2Fleet
    print p1Deploy
    print p1Attack
    print p2Deploy
    print p2Attack

os.system('clear')
print "P1: Place Your Ships"
for s in p1Fleet.keys():
    place_ship(p1Fleet[s], p1Deploy)
print_board(p1Deploy)
raw_input("Press RETURN to continue...")

os.system('clear')
print "P2: Place Your Ships"
for s in p2Fleet.keys():
    place_ship(p2Fleet[s], p2Deploy)
print_board(p2Deploy)
raw_input("Press RETURN to continue...")

def play():
    while True:
        os.system('clear')
        print("P1 Attack")
        if(attack(p1Attack, p2Deploy, p2Fleet) > 0):
            if(endGame(p2Fleet)):
                print "P1 Wins"
                print_board(p1Attack)
                print_board(p1Deploy)
                print "GAME OVER"
                break
        raw_input("Press RETURN to continue...")

        os.system('clear')
        print("P2 Attack")
        if(attack(p2Attack, p1Deploy, p1Fleet)):
            if(endGame(p1Fleet)):
                print "P2 Wins"
                print_board(p2Attack)
                print_board(p2Deploy)
                print "GAME OVER"
                break
        raw_input("Press RETURN to continue...")

play()
