###################################################
#             Insert Text In Image                #
###################################################
from PIL import Image
import sys
import math


def getLengthOfMessage(hide_text_file):  # {
    with open(hide_text_file, 'r') as File:  # {
        # Read the file contents
        file_contents = File.read()
        # Get the character count and multiply by 8
        # ASCII represention contains 8 bits
        message_length = (len(file_contents) * 8)
        # Close the file
        File.close()
        # Return the message length
        return message_length
    # }
# }


def hideMessageLength(hidden_message_length, text_in_image):  # {
    # Open the image
    image = Image.open(text_in_image)
    # Get the dimensions of the image
    width, height = image.size
    # PIL uses zero based coordinates (0,0)
    # starting from the top left corner.
    # Subtracting 1 from both the width and height
    # to start from the bottom right coner.
    widthPixel = width - 1
    heightPixel = height - 1
    # Convert the hidden message length to binary
    hidden_message_length_binary = '{0:032b}'.format(hidden_message_length)
    pixel_index = 0
    message_length_index = 0

    while (pixel_index < 11):  # {
        # Grab the current RGB pixel from the image
        current_pixel = image.getpixel((widthPixel, heightPixel))
        # getpixel() returns a tuple, separate the RGB pixel
        red, green, blue = current_pixel
        # Convert the red, blue, green pixels to 8-bit binary representation
        red_binary = '{0:08b}'.format(red)
        green_binary = '{0:08b}'.format(green)
        blue_binary = '{0:08b}'.format(blue)
        # Slice the least significant bit, RED
        red_binary = red_binary[:7]
        # Append 1 bit from the 32 bit message length to the R, G, B binary strings
        red_binary += hidden_message_length_binary[message_length_index]
        # Update the message length index
        message_length_index += 1
        # Same previous steps but for GREEN
        green_binary = green_binary[:7]
        green_binary += hidden_message_length_binary[message_length_index]
        message_length_index += 1

        # BLUE is a special case since 11 x 3 = 33, and we're only
        # using 32 bits for the message length
        if (message_length_index < 32):  # {
            blue_binary = blue_binary[:7]
            blue_binary += hidden_message_length_binary[message_length_index]
            message_length_index += 1
        # }

        # After modifications convert back to decimal
        red_decimal = int(red_binary, 2)
        green_decimal = int(green_binary, 2)
        blue_decimal = int(blue_binary, 2)

        # Create a tuple of the new R, G, B values for inserting
        encoded_pixel = (red_decimal, green_decimal, blue_decimal)
        # Insert the modified pixel back into the image
        image.putpixel((widthPixel, heightPixel), encoded_pixel)
        # Move the width pixel to the right by 1
        widthPixel -= 1
        # Update the pixel index
        pixel_index += 1
    # }

    # Save a copy of the new image, slice the last 4 characters (extension) of
    # original image and append new PNG extension
    newly_saved_image_name = text_in_image[:-4] + '_hidden.png'
    image.save(newly_saved_image_name, 'PNG')
    # Delete the image from memory
    del image
    # Return the newly created image name
    return newly_saved_image_name
# }


def hideMessageText(hidden_message_length, new_image, hidden_message_text_file):  # {
    # Open the image that was previously saved from hideMessageLength function
    image = Image.open(new_image)
    # Get the dimensions of the image
    width, height = image.size
    # Since we know the length of the message, we can extract the appropriate pixels
    # Create a list of the pixels needed for modification
    pixel_list = []
    # The width is minus 12 because the first 11 bits
    # contain the length of the message
    widthPixel = width - 12
    heightPixel = height - 1
    # Each pixel contains R, G, B values, so the amount of pixels needed is
    # the length of the message divided by 3 rounded up if not divided evenly
    # Use the math.ceil function to round up to the nearst whole number
    number_of_pixels = math.ceil(hidden_message_length / 3)
    pixel_index = 0

    while(pixel_index < number_of_pixels):  # {
        # If the width pixel exceeds the width of the image, move the width back to the
        # right most position of the image and decrement the height pixel to move up by 1
        # The image coordinate system starts at (0,0), therefore inclusive (zero based)
        if(widthPixel == -1):  # {
            widthPixel = width - 1
            heightPixel -= 1
        # }

        # Get the current pixel position starting from the
        # bottom right on the 12th pixel going left
        current_pixel = image.getpixel((widthPixel, heightPixel))
        # Append the current pixel to the pixel list
        pixel_list.append(current_pixel)
        # Increment the pixel index
        pixel_index += 1
    # }

    # Remove the image from memeory
    del image

    # Context Manager for reading the hidden message text file
    with open(hidden_message_text_file, 'r') as File:  # {
        # Read the entire contents of the file
        file_contents = File.read()
        # Close the file
        File.close()
    # }

    # Creating a variable for the file contents position starting at index 0 (the first character in the file)
    text_file_binary_contents = []
    # Position index for the text_file_binary_contents list
    character_position = 0

    # Loop through the text file contents and
    # covert the character to ASCII binary notation
    while (character_position < len(file_contents)):  # {
        # Convert the current character from the file contents to
        # ASCII decimal representation
        character_ascii_decimal = ord(file_contents[character_position])
        # Convert the ASCII decimal to 8-bit binary representation
        file_character_binary = '{0:08b}'.format(character_ascii_decimal)
        # Append the binary contents to the text file binary list
        text_file_binary_contents.append(file_character_binary)
        # Increment the character postion to move to get the next character
        character_position += 1
    # }

    text_file_binary_contents = ''.join(text_file_binary_contents)

    # Loop through the text file binary contents string and append to
    # the pixel's R, G, B least significant bit
    character_position = 0
    pixel_list_position = 0

    while(character_position < len(text_file_binary_contents)):  # {

        # Get the R, G, B values from the pixel list
        red = pixel_list[pixel_list_position][0]
        green = pixel_list[pixel_list_position][1]
        blue = pixel_list[pixel_list_position][2]

        # Convert the pixel values to 8-bit binary representation
        red_binary = '{0:08b}'.format(red)
        green_binary = '{0:08b}'.format(green)
        blue_binary = '{0:08b}'.format(blue)

        # Slice the least significant bit (8th bit) from the R, G, B values
        # Append the file contents character (binary) to each R, G, B value and
        # increment the character position to get the next binary character
        if(character_position < len(text_file_binary_contents)):  # {
            red_binary = red_binary[:7]
            red_binary += text_file_binary_contents[character_position]
            character_position += 1
        # }

        if(character_position < len(text_file_binary_contents)):  # {
            green_binary = green_binary[:7]
            green_binary += text_file_binary_contents[character_position]
            character_position += 1
        # }

        if(character_position < len(text_file_binary_contents)):  # {
            blue_binary = blue_binary[:7]
            blue_binary += text_file_binary_contents[character_position]
            character_position += 1
        # }

        # Convert back to decimal
        red_decimal = int(red_binary, 2)
        green_decimal = int(green_binary, 2)
        blue_decimal = int(blue_binary, 2)

        # Create a new tuple with the modified R, G, B values
        new_pixel_tuple = (red_decimal, green_decimal, blue_decimal)
        # Insert the new pixel tuple into the pixel list
        pixel_list[pixel_list_position] = new_pixel_tuple
        pixel_list_position += 1
    # }

    # Open the image one last time...
    image = Image.open(new_image)
    # Get the dimensions
    width, height = image.size
    # The width is minus 12 because the first 11 bits
    # contain the length of the message
    widthPixel = width - 12
    heightPixel = height - 1
    # Zero out the pixel list index
    pixel_list_position = 0
    x = 0

    while(x < len(pixel_list)):  # {

        if(widthPixel == -1):  # {
            widthPixel = width - 1
            heightPixel -= 1
        # }

        image.putpixel((widthPixel, heightPixel), pixel_list[pixel_list_position])
        pixel_list_position += 1
        widthPixel -= 1
        x += 1
    # }

    # Save a copy of the new image
    image.save(new_image, 'PNG')
    # Delete the image from memory
    del image
# }


if (__name__ == "__main__"):  # {
    # The image to hide text into
    text_in_image = sys.argv[1]
    # The text file with its contents
    hide_text_file = sys.argv[2]
    # Get the text file message length
    hidden_message_length = getLengthOfMessage(hide_text_file)
    # Hide the message length in the image
    new_image = hideMessageLength(hidden_message_length, text_in_image)
    # Hide the message text in the image
    hideMessageText(hidden_message_length, new_image, hide_text_file)
# }
