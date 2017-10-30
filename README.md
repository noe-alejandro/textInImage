# Text In Image Program
Name: Noe Rojas

## Image Requirements
1. Input image must be JPG or JPEG formats only.<br>
  &nbsp;&nbsp;**example: *my_image.jpg***
2. Pixels must be in R,G,B format (red, blue, green) only.<br>
&nbsp;&nbsp;**example: *(164,124,124)***<br>
&nbsp;&nbsp;Note: Program does not support R,G,B,A or R,G,B,W encoded pixels.

## Running The Program
#### Embedding Text In Image
To embed text in the image run: <br>

```
python3 insert-text.py <ARG1> <ARG2>
```
where **&lt;ARG1&gt;** is the name of the image, and **&lt;ARG2&gt;** is the name of the file with the hidden text <br>

**Example:**
```
python3 insert-text.py image.jpg hidden-message.txt
```
