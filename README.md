# Text In Image
Author: Noe Rojas

## Software Architecture & Requirements
Software performs steganography on images.

**insert-text.py** hides text within an image by extracting the least significant bit of each pixel starting from the bottom-left corner of the image. <br>

**extract-text.py** extracts text that was performed by **insert-text.py**. <br>

1. Python 3.6 or higher
2. PIL (python image library) version 4.3.0 or higher
## Image Requirements
1. Input image must be **JPG** or **JPEG** formats only.<br>
  &nbsp;&nbsp;**example: *my_image.jpg***
2. Pixels must be in R, G, B format (red, green, blue) only.<br>
&nbsp;&nbsp;**example: *(164,124,124)***<br>
&nbsp;&nbsp;Note: Program does not support (R, G, B, A) or (R, G, B, W) encoded pixels.

## Running The Program
### Embedding Text In Image
To embed text in the image run: <br>

```
python3 insert-text.py <ARG1> <ARG2>
```
Where **&lt;ARG1&gt;** is the name of the image, and **&lt;ARG2&gt;** is the name of the file with the hidden text <br>

**Note:** You must create your own **text file** that will contain your message to hide. **The file must be .txt**

**Example:**
```
python3 insert-text.py image.jpg hidden-message.txt
```

When the program completes, there will be an image file that contains the embedded text at the project root folder. The image will contain its original file name, but with the file extension as **PNG**

**Example**
```
orginal-file-name_hidden.png
```

### Extracting Text From Image
To extract text from a text embeded image run:
```
python3 extract-text.py <ARG1>
```
Where **&lt;ARG1&gt;** is the name of the text embedded image.

**Example:**
```
python3 extract-text.py image_hidden.png
```
