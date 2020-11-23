import os
import sys
import time


def readBMP(filePath):
    file = open(filePath,"rb")

    #Header
    byte = returnBytes(file,14)
    #print(str(byte))

    #Size of Info Header
    byte = returnBytes(file, 4)
    #print(str(byte.hex()))

    #Width
    imageWidth = returnIntFromBytes(file,4)
    #print(str(imageWidth))

    #Height
    imageHeight = returnIntFromBytes(file, 4)
    #print(str(imageHeight))

    #Number of Planes
    byte = returnBytes(file, 2)
    #print(str(byte.hex()))

    #Bits per Pixel
    byte = returnBytes(file, 2)
    #print(str(byte.hex()))

    #Compression
    byte = returnBytes(file, 4)
    #print(str(byte.hex()))

    #image size
    byte = returnBytes(file, 4)
    #print(str(byte.hex()))

    #Horizontal Resolution: Pixels/meter
    byte = returnBytes(file, 4)
    #print(str(byte.hex()))

    #Vertical Resolution: Pixels/meter
    byte = returnBytes(file, 4)
    #print(str(byte.hex()))

    #Colors Used
    byte = returnBytes(file, 4)
    #print(str(byte.hex()))

    #Important Colors
    byte = returnBytes(file, 4)
    #print(str(byte.hex()))


    columns = []

    rowLength = imageWidth
    columnLength = imageHeight

    index = 0

    while index < columnLength:
        row = []
        index2 = 0
        while index2 < rowLength:
            row.append(returnBytes(file,3))
            index2 += 1
        columns.append(row)
        index += 1

    columns.reverse()

    for i in columns:
        stringtoPrint = ""
        for x in i:
            stringtoPrint += x.hex()

        #print(stringtoPrint)

    """This is a Test Area"""

    for i in columns:
        Newindexvar = 1
        stringtoPrint = ""
        for x in i:
            print("#"+str(Newindexvar)+"["+str(x[0])+"]"+"["+str(x[1])+"]"+"["+str(x[2])+"]")
            Newindexvar += 1

    """End Test Area"""


    for i in columns:
        stringtoPrint = ""
        for x in i:
            stringtoPrint += "["+str(x[0])+"]"

        #print(stringtoPrint)

    stringToReturn = ""
    for i in columns:
        stringtoPrint = ""
        characterList = []
        characterList.append(" ")
        characterList.append(".")
        characterList.append(",")
        characterList.append(":")
        characterList.append(";")
        characterList.append("~")
        characterList.append("=")
        characterList.append("o")
        characterList.append("O")
        characterList.append("b")
        characterList.append("P")
        characterList.append("X")
        characterList.append("8")
        characterList.append("B")
        characterList.append("#")
        characterList.append("@")

        for x in i:
            value = x[0]
            index = 1
            numberOfCharacters = len(characterList)
            increment = int(255 / numberOfCharacters)

            while index <= numberOfCharacters:
                if index == numberOfCharacters:
                    stringtoPrint += characterList[index-1]
                elif value <= increment*index:
                    stringtoPrint += characterList[index-1]
                    index = numberOfCharacters
                index += 1

        #print(stringtoPrint)
        stringToReturn += stringtoPrint+"\n"

    file.close()
    return(stringToReturn)


def returnBytes(file, numberOfBytes):

    numberOfBytes = int(numberOfBytes)
    bytesToReturn = bytes(0)
    index = 0

    while index < numberOfBytes:
        bytesToReturn += file.read(1)
        index += 1

    #print(bytesToReturn.hex())
    return bytesToReturn


def calculateNumberPaddingforBlenderImageIndex(frameNumber):
    if frameNumber <= 9:
        return "000"
    elif frameNumber <= 99:
        return "00"
    elif frameNumber <= 999:
        return "0"
    else:
        return ""


def writeAnimation(ArrayToWrite):
    file = open("asciiAnimation.txt","w")
    stringToWrite = ""
    index = 1
    for i in ArrayToWrite:
        stringToWrite += i + "\n"
        index += 1

    file.write(stringToWrite)
    print("Animation written...")
    file.close()


def returnIntFromBytes(file, numberOfBytes):
    listOfBytes = []
    index = 1
    listOfBytes.append(returnBytes(file, 1))
    while index < numberOfBytes:
        listOfBytes.insert(0, returnBytes(file, 1))
        index += 1
    returnedValue = bytes()
    for i in listOfBytes:
        returnedValue += i
    return int.from_bytes(returnedValue, "big")


def processAnimation(filePathString,animationStartFrame,animationEndFrame):
    fileIndexPadding = "000"
    currentFrame = animationStartFrame
    endFrame = animationEndFrame
    animationString = []
    while currentFrame <= endFrame:
        fileIndexPadding = calculateNumberPaddingforBlenderImageIndex(currentFrame)
        filePath = filePathString + fileIndexPadding + str(currentFrame) + ".bmp"
        animationString.append(readBMP(filePath))
        print("Finished Processing Frame: " + str(currentFrame))
        currentFrame += 1

    writeAnimation(animationString)

    playAnimation = int(input("Type '1' to Play the finished animation or '0' to exit:"))
    while bool(playAnimation):
        for i in animationString:
            time.sleep(.1)
            os.system('cls')
            print(i)
        playAnimation = int(input("Type '1' to Replay animation or '0' to exit:"))

    return animationString


def main():
    processAnimation("C:\\tmp\\",60,180)

main()