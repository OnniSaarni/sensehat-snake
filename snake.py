import os
from sense_hat import SenseHat
import random
import time
import math
import threading
import pyfiglet
import dotenv
import requests
import uuid

dotenv.load_dotenv()

def save_highscore(name,score):
    print(name, score)
    requests.post("http://10.255.0.31:5000/save", json={"id": str(uuid.uuid4()),"name": name, "score": score, "deviceid": os.environ.get('SNAKE_DEVICEID')}, headers={"Authorization": os.environ.get('AUTH_KEY'), "Content-Type": "application/json"})

def set_char(chosenChar,selectedColor):
    global matrix

    startPos = [4,6]

    getChar = pyfiglet.figlet_format(chr(chosenChar+97).upper(), font = "3x5" ).split(" \n")
    getChar.pop(0)
    getChar.pop(5)
    for i in range(6):
        getChar[i-1] = getChar[i-1].replace(" ", "0").replace("#", str(selectedColor))
    for line in reversed(getChar):
        for char in list(line):
            matrix[startPos[0]][startPos[1]] = int(char)
            startPos = [startPos[0] + 1, startPos[1]]
        startPos = [startPos[0] - 3, startPos[1] - 1]

def displayMatrix2():
    global matrix
    for i in range(8):
        for j in range(8):
            if [i,j] == [2,3]:
                sense.set_pixel(i, j, (255, 0, 0))
                continue
            if matrix[i][j] == 0:
                sense.set_pixel(i, j, (0, 0, 0)) 
            if matrix[i][j] == 1:
                sense.set_pixel(i, j, (0, 255, 0))
            if matrix[i][j] == 3:
                sense.set_pixel(i, j, (255, 255, 0))
            elif matrix[i][j] == 4:
                sense.set_pixel(i, j, (0, 255, 0))
            elif matrix[i][j] == 5:
                sense.set_pixel(i, j, (0, 0, 255))
            elif matrix[i][j] == 6:
                sense.set_pixel(i, j, (0, 0, 100))

def selectCharacter():
    global matrix, snakeDirection, startButton

    matrix = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]

    selectedChar = 0
    skip = False
    snakeDirection = "middle"

    while True:

        if snakeDirection == "up":
            if selectedChar != 0:
                selectedChar -= 1
                snakeDirection = "middle"
        elif snakeDirection == "down":
            if selectedChar != 25:
                selectedChar += 1
                snakeDirection = "middle"
        elif snakeDirection == "left":
            skip = True
            break

        juttu = 3 - selectedChar
        if juttu < 0:
            juttu = 0

        juttu2 = selectedChar - 21
        if juttu2 < 0:
            juttu2 = 0

        for c in range(0,8):
            matrix[2][c] = 0

        if selectedChar % 2 == 0:
            for i in range(juttu,8-juttu2):
                if i % 2 == 0:
                    matrix[2][i] = 6
                else:
                    matrix[2][i] = 5
        else:
            for i in range(juttu,8-juttu2):
                if i % 2 != 0:
                    matrix[2][i] = 6
                else:
                    matrix[2][i] = 5

        set_char(selectedChar,1)

        if startButton:
            for i in range(8):
                if i % 2 == 0:
                    set_char(selectedChar,3)
                else:
                    set_char(selectedChar,1)
                displayMatrix2()
                time.sleep(0.1)
            time.sleep(2)
            break

        displayMatrix2()
        time.sleep(0.2)
    if skip == True:
        return(None)
    return(chr(selectedChar+97).upper())

def randomApple():
    global matrix
    
    while True:
        randoms = (random.randint(0,7), random.randint(0,7))
        if matrix[randoms[0]][randoms[1]] == 0:
            matrix[randoms[0]][randoms[1]] = 2
            break

def displayMatrix():
    global matrix

    for i in range(8):
        for j in range(8):
            if matrix[i][j] == 1:
                try:
                    if snakeCoords.index((i,j)) == 0:
                        sense.set_pixel(i, j, (0,0,255))
                        continue
                    elif snakeCoords.index((i,j)) % 2 != 0:
                        sense.set_pixel(i, j, (39, 110, 7))
                        continue
                    sense.set_pixel(i, j, (0, 255, 0))
                except:
                    pass
            elif matrix[i][j] == 2:
                sense.set_pixel(i, j, (255, 0, 0))
            else:
                sense.set_pixel(i, j, (0, 0, 0))

def move(direction):
    global snakeCoords
    global matrix
    global length

    moveSet = (0,0)
    if direction == "left":
        moveSet = (-1,0)
    elif direction == "right":
        moveSet = (1,0)
    elif direction == "up":
        moveSet = (0,-1)
    elif direction == "down":
        moveSet = (0,1)

    if snakeCoords[0][0] + moveSet[0] < 0 or snakeCoords[0][0] + moveSet[0] > 7 or snakeCoords[0][1] + moveSet[1] < 0 or snakeCoords[0][1] + moveSet[1] > 7:
        return("dead")

    futureTile = matrix[snakeCoords[0][0] + moveSet[0]][snakeCoords[0][1] + moveSet[1]]

    if futureTile == 1 and moveSet != (0,0):
        if (snakeCoords[1][0], snakeCoords[1][1]) == (snakeCoords[0][0] + moveSet[0], snakeCoords[0][1] + moveSet[1]):
            return("nodead")
        else:
            return("dead")
        
    if futureTile == 2 or futureTile == 0:
        snakeCoords.insert(0, (snakeCoords[0][0] + moveSet[0], snakeCoords[0][1] + moveSet[1]))
        matrix[snakeCoords[0][0]][snakeCoords[0][1]] = 1
        if futureTile == 2:
            randomApple()
            length += 1
        else:
            sense.set_pixel(snakeCoords[len(snakeCoords) - 1][0], snakeCoords[len(snakeCoords) - 1][1], (0, 0, 0))
            matrix[snakeCoords[len(snakeCoords) - 1][0]][snakeCoords[len(snakeCoords) - 1][1]] = 0
            snakeCoords.pop(len(snakeCoords) - 1)
        return("nodead")

    return("nodead")

def checkIfDirectionFine(futureSuunta):
    global snakeCoords
    global matrix

    moveSet = (0,0)
    if futureSuunta == "left":
        moveSet = (-1,0)
    elif futureSuunta == "right":
        moveSet = (1,0)
    elif futureSuunta == "up":
        moveSet = (0,-1)
    elif futureSuunta == "down":
        moveSet = (0,1)

    try:
        futureTile = matrix[snakeCoords[0][0] + moveSet[0]][snakeCoords[0][1] + moveSet[1]]

        if futureTile == 1 and moveSet != (0,0):
            if (snakeCoords[1][0], snakeCoords[1][1]) == (snakeCoords[0][0] + moveSet[0], snakeCoords[0][1] + moveSet[1]):
                return(False)
    except:
        return(True)
    return(True)

def getInput():
    global snakeDirection
    global startButton
    global isGameStarted

    while True:
        startButton = False
        for event in sense.stick.get_events():
            if event.action != "released" and event.direction != "middle":
                if checkIfDirectionFine(event.direction) == True:
                    snakeDirection = event.direction
            elif event.direction == "middle":
                if isGameStarted == False:
                    startButton = True
                    time.sleep(1)

def mainFunc():
    global snakeDirection
    global matrix
    global snakeCoords
    global length
    global startButton
    global isGameStarted

    sense.clear()

    isGameStarted = False

    while True:

        sense.clear()

        while True:
            try:
                if startButton:
                    break
            except:
                pass

        matrix = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        snakeCoords = [(3,4), (4,4)]

        snakeDirection = "middle"
        length = 2

        sense.clear()
        randomApple()

        time.sleep(0.2)

        isGameStarted = True

        while True:
            moveResults = move(snakeDirection)
            displayMatrix()
            if moveResults == "dead":
                time.sleep(0.5)
                for i in range(8):
                    for pixel in snakeCoords:
                        if i % 2 == 0:
                            sense.set_pixel(pixel[0], pixel[1], (0, 0, 150))
                        else:
                            sense.set_pixel(pixel[0], pixel[1], (0, 0, 255))
                    time.sleep(0.2)

                sense.show_message(f"S: {length-2}", text_colour=[0,0,255], scroll_speed=0.05)
                startButton = False
                isGameStarted = False
                selectedCharacterInput = selectCharacter()
                if selectedCharacterInput == None:
                    break
                else:
                    save_highscore(selectedCharacterInput,length-2)
                break

            waitTime = 0.5 * math.exp(-0.15 * (length - 2))
            if waitTime < 0.2:
                waitTime = 0.2
            time.sleep(waitTime)
        isGameStarted = False

sense = SenseHat()
sense.clear()

input_thread = threading.Thread(target=getInput)
main_thread = threading.Thread(target=mainFunc)

input_thread.start()
main_thread.start()
