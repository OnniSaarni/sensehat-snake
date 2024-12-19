from sense_hat import SenseHat
import random
import time
import math
import threading

def save_highscore(score):
    try:
        with open("highscore.txt", "r") as file:
            highscore = int(file.read())
    except:
        highscore = 0

    if score > highscore:
        with open("highscore.txt", "w") as file:
            file.write(str(score))
    # Make a request to the webserver to save the highscore
    # data = {"highscore": score}
    # response = requests.post("http://

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
                    if snakeCoords.index((i,j)) % 2 != 0:
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

                sense.show_message(f"Score: {length-2}", text_colour=[0,0,255], scroll_speed=0.05)
                save_highscore(length-2)
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
