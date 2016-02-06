# 12 man's morris
# First project and upload to github! by noobling
from graphics import *
from math import *
from random import *

wSize = 600
allLocs = []
mills = []  # contains all possible mills
text = Text(Point(wSize/2, 25), "")
text.setSize(15)


def main():
    # controls the flow of the program, allows the players to put their pieces and then move them,
    # alternately, if a mill is made, invites the player to remove opponents piece and decides which
    # player has won. Uses the random function for Player 2 (the computer)

    win = GraphWin('QAT', wSize, wSize)
    win.setBackground('pink')
    win.setCoords(0, 0, wSize, wSize)
    ptList = drawBoard(win)
    # initalise all the variables needed
    pOccup, comOccup, pLOccup, comLOccup = [], [], [], []
    Circles = createCirc(ptList)
    unOccup = list(range(24))
    createmills()
    pColor, comColor = "purple", "hotpink"
    # Display intro and determine who goes first
    displayText(win, "QAT by noobling", pColor)
    displayText(win, "Do you want to go first? Type yes or no into console", pColor)
    ans = getInput()
    # begin the game by placing pieces
    placePieces(win, ans, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, pColor, comColor)
    # start moving pieces
    movePhase(win, ans, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, pColor, comColor)
    # Display end text
    displayText(win, "Thank you for playing!", "purple")
    print("game ended")


def getInput():
    # gets input from user returning 'yes' or 'no'
    # keeps looping until user gives 'yes' or 'no'
    ans = input("Enter here: ")
    while ans != "yes" and ans != "no":
        ans = input("Try again: ")
    return ans


def displayText(win, txt, Color):
    # function to display text on the bottom of window
    time.sleep(1)
    text.undraw()
    text.setText(txt)
    text.setFill(Color)
    text.draw(win)


def locInptList(index, ptList):
    # finds the corresponding point in ptList from allLocs
    # returns an object of class Point
    x, y = allLocs[index]
    return ptList[x][y]


def createCirc(ptList):
    # returns a list of all possible circle objects on board
    Circles = []
    for index in range(24):  # appends 24 different circle objects that represent a piece on the board to circles
        point = locInptList(index, ptList)
        Circles.append(Circle(point, 15))
    return Circles


def createmills():
    # return a list of lists mills where each list in mills contains the allLocs indexes to form a mill
    for i in range(0, 24, 2):
        if i in [6, 14, 22]:
            mills.append([i, i + 1, i - 6])
        else:
            mills.append([i, i + 1, i + 2])
    for j in range(8):
        mills.append([j, j + 8, j + 16])


def placePieces(win, ans, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, pColor, comColor):
    # alternates between player and computer to place a piece on board
    pPieOnSide, comPieOnSide = displayPieOnSide(win,comColor,pColor)
    if ans == "yes":  # let the player go first since they selected yes
        for i in range(12):
            pPlacePiece(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, pColor,pPieOnSide[i])
            comPlacePiece(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, comColor,comPieOnSide[i])
    else:
        for i in range(12):  # let the player go second since they selected no
            comPlacePiece(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, comColor,comPieOnSide[i])
            pPlacePiece(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, pColor,pPieOnSide[i])

def displayPieOnSide(win,comColor,pColor):
    # draws 12 circles for player and computer on the side
    # returns 2 lists for with the circle objects for player and computer
    pPieOnSide,comPieOnSide = [],[]
    x,y,spacing = 20,200,20 # x,y points for the lower left circle's center object and spacing between circle's center
    for i in range(1,13):
        pPieOnSide.append(Circle(Point(x,y+(i*spacing)),15))
        pPieOnSide[-1].draw(win)
        pPieOnSide[-1].setFill(pColor)
        comPieOnSide.append(Circle(Point(x+560,y+(i*spacing)),15))
        comPieOnSide[-1].draw(win)
        comPieOnSide[-1].setFill(comColor)
    return pPieOnSide,comPieOnSide

def pAnimation(Circle1,Circle2):
    p1,p2 = Circle1.getCenter(),Circle2.getCenter()
    xD = p2.getX() - p1.getX()
    yD = p2.getY() - p1.getY()
    for i in range(10):
        time.sleep(0.1)
        Circle1.move(xD/10.0,yD/10.0)
    return Circle1

def pPlacePiece(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, pColor,pPieOnSide):
    # place a piece for the player
    # if a mill is formed allow the player to remove a computer piece unless computer have all mills
    displayText(win, "Your turn to place a piece", pColor)
    nn, d = findNN(pMouseClick(win), ptList)  # get users mouseclick postion on board and store it in nn
    while (d > 15 or nn not in unOccup):  # keep looping until user gives a valid click
        nn, d = findNN(pMouseClick(win), ptList)
    place(win, nn, pOccup, unOccup, Circles, pColor,pPieOnSide)  # place piece on board updating the required variables

    # if a line/mill is formed from the last placed piece allow the player to remove one of comp's pieces
    if isLine(pOccup, pLOccup):
        if allmills(comOccup, comLOccup):
            displayText(win, "Computers has all mills program will skip piece remove", pColor)
            print("com has all mills")
        else:
            displayText(win, "You created a mill, now select a valid to piece to remove!", pColor)
            removePiece(win, ptList, "Player 1", comOccup, unOccup, comLOccup, Circles)


def comPlacePiece(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, comColor,comPieOnSide):
    # place a piece for the computer
    # if a milled is formed allow computer to remove player piece unless player has all mills
    displayText(win, "Computer's turn to place a piece", comColor)
    index = AIplace(comOccup, pOccup, unOccup)
    place(win, index, comOccup, unOccup, Circles, comColor,comPieOnSide)

    # remove a player piece if last move generated a mill/line
    if isLine(comOccup, comLOccup):
        if allmills(pOccup, pLOccup):
            displayText(win, "Player has all mills program will skip piece remove", comColor)
            print("player has all mills")
        else:
            displayText(win, "Computer created a mill removing a piece....", comColor)
            removePiece(win, ptList, "Player 2", pOccup, unOccup, pLOccup, Circles)


def allmills(Occup, linesOccup):
    # given the list of occup places returns true if all pieces form mills
    for nn in Occup:
        if not inLinesOccup(nn, linesOccup): return False
    return True


def pMouseClick(win):
    # return the point which the user clicked
    return win.getMouse()


def place(win, index, Occup, unOccup, Circles, cColor,piece):
    # updates the required lists and displays the circle
    Occup.append(index)
    unOccup.remove(index)
    Circles[index] = pAnimation(piece,Circles[index])


def legalmoves(nn, Occup, unOccup):
    # return a list of legal points in allLocs to move to for nn 
    moves = []  # store all possible moves
    legalmoves = []  # store only legal moves according to game rules
    if nn in [0, 8, 16]:
        moves.append(nn + 7)
        moves.append(nn + 1)
    elif nn in [7, 15, 23]:
        moves.append(nn - 7)
        moves.append(nn - 1)
    else:
        moves.append(nn - 1)
        moves.append(nn + 1)
    moves.append(nn + 8)
    moves.append(nn - 8)
    for move in moves:
        if 0 <= move <= 23 and (move not in Occup) and (move in unOccup):
            legalmoves.append(move)
    return legalmoves


def blocked(Occup, unOccup):
    # Occup is a list of occupied points/locations by a Player and unOccup are free locations
    # returns True if all pieces of the Player are blocked otherwise False

    for nn in Occup:
        if len(legalmoves(nn, Occup, unOccup)) > 0:  # if a legal move is still possible return false
            return False
    return True


def movePiece(win, ptList, cColor, Player, Occup, linesOccup, Circles, unOccup):
    # this function performs a valid move for a Player (1 or 2) and updates the relevant lists
    # it uses the random function to make a valid move for Player 2 (the computer)
    # win is the GraphWin object, ptList is defined in drawBoard(), cColor is the color of pieces,
    # Occup is a list of occupied locations by the Player, linesOccup is a list of lines (mills)
    # of the Player, Circles is a list of the circles (pieces) and unOccup is a list of unOccup locations
    # does not return anything

    # player move
    if Player == "Player 1":
        # select the required piece
        displayText(win, "Your turn to move a piece", cColor)
        nn1, d1 = findNN(pMouseClick(win), ptList)  # get user click location on board and store in nn
        nummoves = len(legalmoves(nn1, Occup, unOccup))  # store the number of possible moves in nummoves
        while d1 > 15 or (nn1 not in Occup) or (nummoves == 0):  # keep looping until user gives a valid click
            nn1, d1 = findNN(pMouseClick(win), ptList)
            nummoves = len(legalmoves(nn1, Occup, unOccup))
        print("player occup", Occup)
        print("unoccup", unOccup)
        print("legal player moves", legalmoves(nn1, Occup, unOccup))
        Circles[nn1].setFill('black')  # change circle color to show its selected
        # move to clicked location
        nn2, d2 = findNN(pMouseClick(win), ptList)
        while d2 > 15 or (nn2 not in legalmoves(nn1, Occup, unOccup)):  # keep looping when an invalid click is made
            if (nn1 == nn2): break  # if the same spot is clicked break loop because it is a valid click
            nn2, d2 = findNN(pMouseClick(win), ptList)
        if (nn1 == nn2):  # Deselect when player clicks on the same circle
            print("deselection executes")
            Circles[nn1].setFill(cColor)
            movePiece(win, ptList, cColor, Player, Occup, linesOccup, Circles, unOccup)
        else:
            move(win, nn1, nn2,ptList, Occup, unOccup, Circles, cColor, linesOccup)

    # computer move
    else:
        displayText(win, "Computer's turn to move a piece", cColor)
        print("comp turn")
        nn1, nn2 = AImove(Occup, unOccup)
        Circles[nn1].setFill('white')  # change color to show selected circle
        time.sleep(1)
        move(win, nn1, nn2,ptList, Occup, unOccup, Circles, cColor, linesOccup)


def move(win, nn1, nn2, ptList,Occup, unOccup, Circles, cColor, linesOccup):
    # remove the required lines if they are broken in linesOccup
    # update the appropriate items
    # undraw previous piece(nn1) and draw new piece(nn2)
    for line in linesOccup:
        for nn in line:
            if nn1 == nn:
                linesOccup.remove(line)
    Occup.remove(nn1)
    Occup.append(nn2)
    unOccup.remove(nn2)
    unOccup.append(nn1)
    mAnimation(win,nn1,nn2,ptList,Circles) # graphically move the circle from nn1 to nn2
    Circles[nn2].setFill(cColor)

def mAnimation(win,nn1,nn2,ptList,Circles):
    # selected piece will move in a straight line to selected location
    p1 = locInptList(nn1,ptList)
    p2 = locInptList(nn2,ptList)
    xD = p2.getX() - p1.getX() # x distance between two points of nn1 and nn2
    yD = p2.getY() - p1.getY() # y distance between two points
    tempCircle = Circles[nn1]
    tempCircle.undraw()
    Circles[nn1].draw(win)
    for i in range(10): # slowly move the circle at nn1 to nn2 so we can graphically see the move
        time.sleep(0.1)
        Circles[nn1].move(xD/10.0,yD/10.0)
    Circles[nn2],Circles[nn1] = Circles[nn1],tempCircle

def movePhase(win, ans, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, pColor, comColor):
    # computer and player take turns moving implementing the proper checks to see if game ended
    if ans == "yes":  # player wanted to go first execute this order of turns
        while True:  # keep looping until a losing condition is met
            if gameEnd(pOccup, unOccup):
                displayText(win, "Computer wins!", comColor)
                print("all players pieces are blocked comp wins")
                break
            pTurn(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, pColor)
            if gameEnd(comOccup, unOccup):
                displayText(win, "Player wins!", pColor)
                print("all computer pieces are blocked player wins")
                break
            comTurn(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, comColor)
    else:  # player did not want to go first so execute this order of turns
        while True:
            if gameEnd(comOccup, unOccup):
                displayText(win, "Player wins!", pColor)
                print("all computer pieces are blocked player wins")
                break
            comTurn(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, comColor)
            if gameEnd(pOccup, unOccup):
                displayText(win, "Computer wins!", comColor)
                print("all players pieces are blocked comp wins")
                break
            pTurn(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, pColor)


def gameEnd(Occup, unOccup):
    # returns true if one of the winning conditions is met
    if blocked(Occup, unOccup) or len(Occup) < 3:
        return True
    else:
        return False


def pTurn(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, pColor):
    # player's turn to move a piece

    # move a player piece
    movePiece(win, ptList, pColor, "Player 1", pOccup, pLOccup, Circles, unOccup)
    if isLine(pOccup, pLOccup):  # if a mill was created allow player to remove piece
        print("linecreated  by player")
        if allmills(comOccup, comLOccup):
            displayText(win, "skipping remove piece because all mills", pColor)
            print("comp has all mills")
        else:
            displayText(win, "You created a mill, now select a valid to piece to remove!", pColor)
            removePiece(win, ptList, "Player 1", comOccup, unOccup, comLOccup, Circles)


def comTurn(win, ptList, unOccup, pOccup, comOccup, pLOccup, comLOccup, Circles, comColor):
    # computer's turn move piece
    # move a computer piece
    movePiece(win, ptList, comColor, "Player 2", comOccup, comLOccup, Circles, unOccup)
    if isLine(comOccup, comLOccup):  # if computer created a mill allow computer to remove piece
        print("line created by computer")
        if allmills(pOccup, pLOccup):
            displayText(win, "skipping remove piece because all mills", comColor)
            print("player has all mills")
        else:
            displayText(win, "Computer created a mill removing a piece....", comColor)
            removePiece(win, ptList, "Player 2", pOccup, unOccup, pLOccup, Circles)


def drawBoard(win):
    # draws the board and populates the gobal list allLocs[] which contains all valid locations in ptList
    # returns ptList which is a 3x8 list of lists containing Point objects. At the top level it contains
    # the 3 squares (biggest first). At the second level, it contains the 8 Points that define
    # each square e.g. ptList[2][1] is the inner most square's 2nd Point. For each square, the bottom
    # left is the first Point
    bk = wSize / 8
    ptList = []
    for i in range(1, 4):
        ptList.append(
            [Point(bk * i, bk * i), Point(bk * i, 4 * bk), Point(bk * i, bk * (8 - i)), Point(4 * bk, bk * (8 - i)),
             Point(bk * (8 - i), bk * (8 - i)), Point(bk * (8 - i), 4 * bk), Point(bk * (8 - i), bk * i),
             Point(4 * bk, bk * i)])
        pp = Polygon(ptList[-1])  # takes the lastest points to create a square
        pp.setWidth(5)  # set the thickness of the lines of polygon
        pp.setOutline(color_rgb(255, 20, 147))
        pp.draw(win)
        for j in range(8):
            allLocs.append([i - 1, j])
    for i in range(8):
        ll = Line(ptList[0][i],
                  ptList[2][i])  # connects the corresponding points of the inner polygon with the outer most polygon
        ll.setWidth(5)
        ll.setFill(color_rgb(255, 20, 147))
        ll.draw(win)
    return ptList  # return a list of all the possible points on board
    # pstList[0][i] refers to the outter most polygon values


def findNN(pt, ptList):
    # finds the nearest location to a point pt in ptList so that the user is only required
    # to click near the location to place/select/move a piece and not exactly on top of it
    # returns the distance d and index location nn in ptList of the nearest point
    d = pointDst(ptList[0][0], pt)  # initalise d the distance from point clicked and a point on board
    nn = 0
    index = -1  # start from 0 so it can be incremented correctly
    for square in ptList:
        for p in square:
            index += 1
            if pointDst(p, pt) < d:  # When d is smallest that will be the cloest point in ptList to pt
                d = pointDst(p, pt)
                nn = index
    return nn, d


def pointDst(p1, p2):
    # find the distance of two points
    return sqrt((p1.getX() - p2.getX()) ** 2 + (p1.getY() - p2.getY()) ** 2)


def isLine(Occup, linesOccup):
    # Occup is a list of occupied locations by a Player and linesOccup are the Player's mills
    # returns True if a line (mill) has been made with the last move and updates linesOccup (mills)
    # otherwise returns False

    tocheck = []  # A list of all the potential mills that could form from the last move
    millcreated = 0  # number of mills created
    # fill tocheck
    for mill in mills:
        for i in mill:
            if i == Occup[-1]:
                tocheck.append(mill)
                break
    for mill in tocheck:
        for j in range(len(mill)):  # check if all the required points to form mill are stored in Occup
            if mill[j] not in Occup:
                break
            elif j == 2:  # once the final element in mill passed the mill must exist in Occup
                linesOccup.append(mill)
                millcreated += 1
    if millcreated > 0: return True
    return False


def removePiece(win, ptList, Player, Occup, unOccup, linesOccup, Circles):
    # performs the removal of a piece as per the game rules
    # and updates Occup, unOccup and Circles lists
    # does not return anything

    if Player == "Player 1":  # player remove piece
        nn, d = findNN(pMouseClick(win), ptList)
        # keep looping until a valid piece to remove is clicked according to the game rules
        while d > 15 or inLinesOccup(nn, linesOccup) or (nn not in Occup):
            nn, d = findNN(pMouseClick(win), ptList)
        updateRmvPiece(nn, Occup, unOccup, Circles)  # remove piece graphically and from Occup
    else:  # computer remove piece
        nn = randrange(0, 24)
        print("player lines occup", linesOccup)
        while (inLinesOccup(nn, linesOccup)) or (nn not in Occup):
            nn = randrange(0, 24)
        updateRmvPiece(nn, Occup, unOccup, Circles)


def inLinesOccup(nn, linesOccup):
    # check if nn is in a mill currently occupied by a player or computer
    for lines in linesOccup:
        for p in lines:
            if nn == p: return True
    return False


def updateRmvPiece(nn, Occup, unOccup, Circles):
    # undraws the circle and updates the required lists 
    Occup.remove(nn)
    unOccup.append(nn)
    flash(nn, Circles)
    Circles[nn].undraw()


def flash(nn, Circles):
    # flash 5 times
    for i in range(5):
        Circles[nn].setFill("white")
        time.sleep(0.1)
        Circles[nn].setFill("black")
        time.sleep(0.1)


def findpOccup(comOccup, unOccup):
    # finds the player occupied points to use in AImove and AIplace
    pOccup = list(range(24))
    notpOccup = comOccup + unOccup
    for x in notpOccup:
        pOccup.remove(x)
    return pOccup


def AIplace(comOccup, pOccup, unOccup):
    # replace the random function by this so that the computer (Player 2) performs an intelligent move
    # if the player is about to create mill place piece in that spot
    # unOccup represents all the possible moves in the place phase of the game
    for nn in unOccup:
        if willMakeLine(nn, pOccup, comOccup, unOccup):
            print("willmakeline passed")
            return nn  # if a line is formed/broken by placing piece at nn return this nn
    # if no lines could be broken or formed check for places that will create a situation where it is one off creating a mill
    if len(comOccup) == 0 or blocked(comOccup,
                                     unOccup):  # if one of the conditions is true it will not be possible to find the afforementioned situation
        print("random piece execueted")
        return choice(unOccup)  # return a randomly chosen point in unOccup list using choice function from random
    for nn in comOccup:
        moves = legalmoves(nn, comOccup, unOccup)
        if len(moves) > 0:
            print("placed next to a piece")
            return moves[0]  # return a position that is next to an already placed piece
    print("Something went wrong")  # error checking (at least on return statement should have been executed)


def willMakeLine(nn, pOccup, comOccup, unOccup):
    # finds the occupied lists from unoccupied list
    # determines if nn will make a line from occupied list
    # if returned true nn will break player's line or form a line
    occuplst = list(range(24))
    for x in unOccup:  # finds the occupied list which includes both player and computer points

        occuplst.remove(x)

    for mill in mills:  # iterating over the global variable mills that stores all possible mills
        for i in occuplst:
            for j in occuplst:
                if allConditions(i, j, nn, pOccup, comOccup, mill):
                    print("mill about to be formed", mill)
                    return True
    return False  # return false when we cannot find a mill with nn and 2 points from occuplst


def allConditions(i, j, nn, pOccup, comOccup, mill):
    # tests if all conditions are met to form/break mill
    if i in mill and j in mill and nn in mill and i != j:
        if ((i in pOccup and j in pOccup) or (i in comOccup and j in comOccup)):
            return True
    return False


def AImove(comOccup, unOccup):
    # looks at all legal moves and returns the first move that will break/form a mill
    # otherwise return the first legal move
    # A move will always be returned because blocked function is checked before this function is executed
    for nn in comOccup:
        moves = legalmoves(nn, comOccup, unOccup)
        for move in moves:
            if willMakeLine(move, findpOccup(comOccup, unOccup), comOccup, unOccup):
                return nn, move
    for nn in comOccup:
        moves = legalmoves(nn, comOccup, unOccup)
        if len(moves) > 0:
            return nn, moves[0]
    print("Something went wrong")  # error checking


main()
