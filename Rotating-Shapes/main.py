# Within the terminal: pip install Pillow
# pip install numpy
# Code help here - https://pythonexamples.org/python-pillow-rotate-image-90-180-270-degrees/
# knowledge share on ranges https://pynative.com/python-range-for-float-numbers/

# This code will look to rotate the image for you and re-save the image down ready for use in Tableau.
import numpy as np
from PIL import Image

# Read the image
im = Image.open("Heart.png")

number_of_sections = float(input("How many points do you need?\n"))
#num_range = list((range(0,360,angle)))
#print(num_range)

angle = 0
save = 1  # We start at 1, because we will need this for the ranking section in Tableau.
angle_gap = float(360 / number_of_sections)

# float step
for i in np.arange(0, 360, angle_gap):
    print(angle)

    out = im.rotate(angle)
    out.save(f'{save}.png')  # Save each image.

    print(out)

    save = save + 1  # We will need this for the ranking section in Tableau.
    angle = angle - angle_gap  # We use minus here to make clockwise.

im.close()
