import numpy as np
import cv2
import bpy
import bmesh
import os
from math import radians
from mathutils import Matrix, Euler

# TODO
# move to directory containing the blender.exe file
# run blender -b
# set up script to do that
# https://cd3dtech.com/posts/blender-rendering-from-the-command-line/

# Run admin powershell, then:
# conda activate myenv
# cd 'C:\Program Files\Blender Foundation\Blender 4.0\'
# blender -b .\4.0\python\cube.blend --python .\4.0\python\test.py
# Use `./bin/python.exe ...`

def look_down_z_axis():
    # Assuming you are in the 3D View, set the view to look down the Z-axis
    for area in bpy.context.screen.areas:
        print(area.type)
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            # Set the view rotation (looking straight down the Z-axis)
            space.region_3d.view_rotation = Euler((0.0, 0.0, 0.0), 'XYZ').to_quaternion()
            break

def select_object_portion():
    # Ensure the active object is in edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Assuming we're working with a mesh
    obj = bpy.context.edit_object
    me = obj.data
    
    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    
    # Deselect all
    bpy.ops.mesh.select_all(action='DESELECT')
    bm.select_mode = {'VERT'} # Change to {'EDGE'} or {'FACE'} as needed
    
    # Select a portion of the mesh here
    # Example: Selecting vertices based on a condition (e.g., z coordinate)
    for v in bm.verts:
        if v.co.z > 0: # Example condition, adjust as necessary
            v.select = True
    
    # Update the mesh to reflect the selection
    bmesh.update_edit_mesh(me)

select_object_portion()
bpy.context.window.workspace = bpy.data.workspaces['UV Editing']
look_down_z_axis()
# bpy.ops.uv.project_from_view()

cube = bpy.data.objects["Cube"]

bpy.context.view_layer.objects.active = cube

cube.select_set(True)

uv_layer = cube.data.uv_layers["UVMap"].data
'''
# Example: Move all UV coordinates slightly
for poly in cube.data.polygons:
    for loop_index in poly.loop_indices:
        loop_uv = uv_layer[loop_index]
        # This moves the UV coordinates by 0.1 on the U (x) and V (y) axes
        loop_uv.uv.x += 0.2
        loop_uv.uv.y += 0.2
'''

bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

'''
# Debug: Print UV coordinates
print("UV coordinates:")
for poly in cube.data.polygons:
    for loop_index in poly.loop_indices:
        loop_uv = uv_layer[loop_index]
        print(loop_uv.uv)
'''

# Commented: code to find points on the inside of the purple outline
'''
lower_H = 131
lower_S = 211
lower_V = 225

upper_H = 151
upper_S = 255
upper_V = 255 

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'updated.png')

bpy.data.objects["Cube"].data.vertices[0].co.x += 100.0

image = cv2.imread(image_path)
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
'''