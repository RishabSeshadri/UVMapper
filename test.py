import numpy as np
import cv2
import bpy
import bmesh
import os
from math import radians
import math
from mathutils import Euler
from time import sleep

# TODO
# move to directory containing the blender.exe file
# run blender -b
# set up script to do that
# https://cd3dtech.com/posts/blender-rendering-from-the-command-line/

# Run admin powershell, then:
# conda activate myenv
# cd 'C:\Program Files\Blender Foundation\Blender 4.0\'
# blender .\4.0\python\poster.blend --python .\4.0\python\test.py
# Use `./bin/python.exe ...`



# rotate -142
# scale to 0.9
# mirror x

# Placeholder functions for finding and adjusting UVs, to be implemented based on your model and requirements
def find_closest_vertex_to_landmark(landmark, uv_layer):
    pass

def adjust_uv_coordinate(vertex, landmark, uv_layer):
    pass

def rotate_uv(x1, y1, angle, origin=(0, 0)):
    angle = radians(angle)
    cos_theta, sin_theta = math.cos(angle), math.sin(angle)
    x0, y0 = origin    

    x, y = x1 - x0, y1 - y0
    return (x * cos_theta - y * sin_theta + x0,
            x * sin_theta + y * cos_theta + y0)

def scale_uv(uv, scale_factor):
    scaled_uv = (uv[0] * scale_factor, uv[1] * scale_factor)
    return scaled_uv

def mirror_uv(uv):
    mirrored_uv = (1 - uv[0], uv[1])
    return mirrored_uv

def look_down_z_axis():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            space.region_3d.view_rotation = Euler((0.0, 0.0, 0.0), 'XYZ').to_quaternion()
            break
    
def select_object_portion():
    bpy.ops.object.mode_set(mode='EDIT')

    context = bpy.context
    obj = context.edit_object
    me = obj.data

    bm = bmesh.from_edit_mesh(me)

    for v in bm.verts:
        v.select_set(v.co.y > 5.7)

    bm.select_mode = {'VERT', 'EDGE', 'FACE'}
    bm.select_flush_mode()
    #bm.select_flush(True) # or select flush, deselect all first. 
    # put in tool in face select mode (without op)    
    context.tool_settings.mesh_select_mode = (False, False, True)

    '''
    #bpy.ops.mesh.separate(type='SELECTED')
    for v in bm.verts:
        if v.co.z > 0: # Example condition, adjust
            v.select = True
    bm.select_mode = {'VERT'} # Change to {'EDGE'} or {'FACE'} as needed
    '''
    # Update the mesh to reflect the selection
    bmesh.update_edit_mesh(me)


# This is a conceptual snippet and may require adjustments to fit your specific model and landmarks
def adjust_uv_based_on_landmarks(landmarks, uv_layer):
    # Example: Adjust UVs to match landmarks
    for landmark in landmarks:
        # Find the closest vertex/UV coordinate to the landmark
        closest_vertex = find_closest_vertex_to_landmark(landmark, uv_layer)
        # Adjust the UV coordinate of the closest vertex
        adjust_uv_coordinate(closest_vertex, landmark, uv_layer)


select_object_portion()
bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.mesh.select_linked(delimit={'SEAM'})

bpy.context.window.workspace = bpy.data.workspaces['UV Editing']
bpy.ops.object.mode_set(mode='EDIT')
cube = bpy.data.objects["l_handMeshNode"]
cube.select_set(True)
bpy.context.view_layer.objects.active = cube

me = cube.data
bm = bmesh.from_edit_mesh(me)
uv_layer = bm.loops.layers.uv.active

# for area in bpy.context.screen.areas:
    # print(area)
#sleep(5)
look_down_z_axis()
#bpy.ops.uv. 
bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)


bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

ob = bpy.context.object

# rotate
for face in bm.faces:
    for loop in face.loops:
        uv = loop[uv_layer].uv
        rotated_uv = rotate_uv(uv[0], uv[1], 142, (0.5, 0.5))
        loop[uv_layer].uv = rotated_uv

# scale
for face in bm.faces:
    for loop in face.loops:
        uv = loop[uv_layer].uv
        scaled_uv = scale_uv(uv, 0.85)
        loop[uv_layer].uv = scaled_uv

# mirror
for face in bm.faces:
    for loop in face.loops:
        uv = loop[uv_layer].uv
        mirrored_uv = mirror_uv(uv)
        loop[uv_layer].uv = mirrored_uv

# shift up
for face in bm.faces:
    for loop in face.loops:
        loop[uv_layer].uv[1] += 0.1
        
        
bmesh.update_edit_mesh(me)

# bpy.ops.uv.project_from_view(override)


#bpy.ops.uv.project_from_view(Orothographic=True)
#
'''
cube.data.uv_layers["UVMap"].active = True

for pt in cube.data.uv_layers["UVMap"].uv:
    print("rchd")
    if pt.x > 0.5:
        print("rchd2")
        pt.x = 0.4
'''
#uv_layer = cube.data.uv_layers["UVMap"].data
'''
for poly in cube.data.polygons:
    if loop_uv.uv.x < 0.5:
        loop_uv.uv.x = 0.4
    else:
        loop_uv.uv.x = 0.8

    if loop_uv.uv.y < 0.5:
        loop_uv.uv.y = 0.4
    else:
        loop_uv.uv.y = 0.8    
'''


'''
# Example: Move all UV coordinates slightly
for poly in cube.data.polygons:
    for loop_index in poly.loop_indices:
        loop_uv = uv_layer[loop_index]
        # This moves the UV coordinates by 0.1 on the U (x) and V (y) axes
        loop_uv.uv.x += 0.2
        loop_uv.uv.y += 0.2
'''

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



'''
import bpy
import bmesh
from mathutils import Euler

def look_down_z_axis():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            space.region_3d.view_rotation = Euler((0.0, 0.0, 0.0), 'XYZ').to_quaternion()
            return area, space.region_3d  # Return the area and the region_3d for later use
    return None, None

def project_selected_faces(obj_name):
    # Ensure the object exists and is of type 'MESH'
    if obj_name not in bpy.data.objects or bpy.data.objects[obj_name].type != 'MESH':
        print(f"The object {obj_name} does not exist or is not a mesh")
        return

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Get the mesh object
    mesh_obj = bpy.data.objects[obj_name]
    bpy.context.view_layer.objects.active = mesh_obj
    mesh_obj.select_set(True)

    # Switch to Edit Mode and get the mesh data
    bpy.ops.object.mode_set(mode='EDIT')
    me = mesh_obj.data
    bm = bmesh.from_edit_mesh(me)

    # Select the faces you want to project
    # Modify this logic as needed to select the correct faces
    for face in bm.faces:
        face.select_set(True)

    # Update the mesh
    bmesh.update_edit_mesh(me, False, False)

    # Get the 3D view area and region_3d where we want to project from
    area, region_3d = look_down_z_axis()
    if not area or not region_3d:
        print("No 3D View area found")
        return

    # Construct the override dictionary for the 3D view context
    override = {
        'scene': bpy.context.scene,
        'region': area.regions[-1],
        'area': area,
        'space_data': area.spaces.active,
        'active_object': bpy.context.view_layer.objects.active,
        'window': bpy.context.window
, 'screen': bpy.context.screen,
'region_3d': region_3d
}

python
Copy code
# Use the override dictionary to call the project_from_view operator
bpy.ops.uv.project_from_view(override, camera_bounds=False, scale_to_bounds=True)

# Switch back to Object Mode
bpy.ops.object.mode_set(mode='OBJECT')
'''