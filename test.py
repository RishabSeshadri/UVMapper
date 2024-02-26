import cv2
import numpy as np
import bpy

bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0


# TODO
# move to directory containing the blender.exe file
# run blender -b
# set up script to do that
# https://cd3dtech.com/posts/blender-rendering-from-the-command-line/




lower_H = 131
lower_S = 211
lower_V = 225

upper_H = 151
upper_S = 255
upper_V = 255
import cv2
import numpy as np

image = cv2.imread('updated.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_purple = np.array([lower_H, lower_S, lower_V])
upper_purple = np.array([upper_H, upper_S, upper_V])

mask = cv2.inRange(hsv, lower_purple, upper_purple)

# Find contours and hierarchy
contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

# Check if hierarchy is not empty
if hierarchy is not None:
    # Loop through the contours and hierarchy
    for i, (contour, h) in enumerate(zip(contours, hierarchy[0])):
        # Check if contour has a parent, indicating it's an inner contour
        if h[3] != -1:  # h[3] is the parent index
            # This contour is an inner contour
            # Draw or process the inner contour as needed
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

# Display the result
image = cv2.resize(image, (960, 540))  
cv2.imshow('Inner Contours Only', image)
cv2.waitKey(0)
cv2.destroyAllWindows()