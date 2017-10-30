###################################################
#            Extract Text From Image              #
###################################################
from PIL import Image
import sys
import math


def getMessageLength(file_name):  # {
    # open the image using PIL library
    image = Image.open(file_name)
    # get the dimensions of the image
    width, height = image.size
    # get width and height pixels. zero based coordinates
    widthPixel = width - 1
    heightPixel = height - 1
    # loop through the first 11 pixels
    # starting from the bottom right moving left
    length = 0
    # a list to contain the first 11 pixels
    rgbPixelList = []

    while (length < 11):  # {

        rgbPixel = image.getpixel((widthPixel, heightPixel))
        rgbPixelList.append(rgbPixel)

        length += 1
        widthPixel -= 1
    # }

    # delete the image from memory
    del image

    # parse the rgb pixels
    index = 0

    # the least significant bit in 8 bit is the last bit
    # zero based therefore 7
    leastSignificantBit = 7

    # list to store the message length from the
    # 33 rgb pixel least significant bits
    messageLengthBinary = []

    # loop through the tuples to convert to binary
    while (index < len(rgbPixelList)):  # {

        red = rgbPixelList[index][0]
        green = rgbPixelList[index][1]
        blue = rgbPixelList[index][2]

        redPixelBinaryData = "{0:08b}".format(red)
        greenPixelBinaryData = "{0:08b}".format(green)
        bluePixelBinaryData = "{0:08b}".format(blue)

        # append to the list
        messageLengthBinary.append(redPixelBinaryData[leastSignificantBit])
        messageLengthBinary.append(greenPixelBinaryData[leastSignificantBit])
        messageLengthBinary.append(bluePixelBinaryData[leastSignificantBit])

        index += 1
    # }

    x = ''.join(messageLengthBinary[:-1])
    messageLengthDecimal = int(x, 2)

    return messageLengthDecimal
# }


def getMessageText(messageLength, file_name):  # {
    # open the image using PIL library
    image = Image.open(file_name)
    # get the dimensions of the image
    width, height = image.size
    # starting at pixel 12 from the bottom right
    widthPixel = width - 12
    heightPixel = height - 1

    pixelBits = math.ceil(messageLength / 3)

    messagePixelList = []

    while (pixelBits > 0):  # {

        if(widthPixel == -1):  # {
            widthPixel = width - 1
            heightPixel -= 1
        # }

        messagePixel = image.getpixel((widthPixel, heightPixel))
        messagePixelList.append(messagePixel)

        pixelBits -= 1
        widthPixel -= 1
    # }

    # Delete the image from memory
    del image

    # Parse the list
    # Create a new list without RBG tuples
    newMessageList = []
    # Postion in the newMessageList
    index = 0

    # Append each RGB value to the newMessageList
    while(index < len(messagePixelList)):  # {

        red = messagePixelList[index][0]
        green = messagePixelList[index][1]
        blue = messagePixelList[index][2]

        newMessageList.append(red)
        newMessageList.append(green)
        newMessageList.append(blue)

        index += 1
    # }

    # Convert each index to binary and extract the least significant bit
    index = 0
    bit = 1
    characterList = []
    leastSignificantBitList = []
    # Loop through the new message list and convert to binary
    while (index < len(newMessageList)):  # {
        binaryText = "{0:08b}".format(newMessageList[index])
        leastSignificantBit = binaryText[-1]
        leastSignificantBitList.append(leastSignificantBit)
        # For every 8th bit, convert to ASCII
        if(bit % 8 == 0):  # {
            characterBinary = ''.join(leastSignificantBitList)
            characterDecimal = int(characterBinary, 2)
            ASCIICharacter = chr(characterDecimal)
            characterList.append(ASCIICharacter)
            # python 3.3 and above
            leastSignificantBitList.clear()
            bit = 0
        # }
        index += 1
        bit += 1
    # }
    # Join the character list (the hidden message)
    hiddenMessage = ''.join(characterList)
    # Return the hidden message
    return hiddenMessage
# }


if (__name__ == "__main__"):  # {
    # Get the image filename
    file_name = sys.argv[1]
    # Get the hidden message text length
    messageLength = getMessageLength(file_name)
    print('Extracted text length:', messageLength)
    # Extract the message text from the image
    message = getMessageText(messageLength, file_name)
    # Print the hidden message to the console
    print(message)
# }
