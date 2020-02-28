import bpy 
import random
import time
import threading
import socket
import pickle


def createSphere(name_geo):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, enter_editmode=False, location=(0, 0, 0))
    base_geometry = bpy.data.objects['Sphere']
    base_geometry.name = name_geo

    # Smooth Shading
    bpy.ops.object.shade_smooth()
    
def reset_shape_keys(key_value):
    shape_keys = bpy.data.shape_keys
    
    for key in shape_keys:
        for key_block in key.key_blocks:
            key_block.value = key_value
    
def del_shape_keys(base_geometry):
    activeObject(base_geometry)
    bpy.ops.object.shape_key_remove(all=True)
    

def apply_subsurf(name_sub):
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=name_sub)

def activeObject(base_geometry):
    bpy.ops.object.select_all(action='DESELECT')
    blob = bpy.data.objects[base_geometry]
    bpy.context.view_layer.objects.active = blob
    blob.select_set(True)
   
def createModifiers(base_geometry, name_sub, noise, strength):
    # Create displacement modifier
    objectMod = bpy.data.objects[base_geometry]
    modifier = objectMod.modifiers.new(name="Displace", type='DISPLACE')

    # Create Texture
    name_text = 'blob_text'
    blob_texture = bpy.data.textures.new(name=name_text, type='MARBLE')

    modifier.texture = bpy.data.textures[name_text]
    modifier.texture.noise_scale = noise #random.random() #0.25
    modifier.strength = strength #random.random() #0.4
    
    # Add subsurf
    subd = objectMod.modifiers.new(name_sub, type='SUBSURF')
    objectMod.modifiers[name_sub].levels = 1
    
    return blob_texture
    
def applyDisplace(name_geo):

    # Apply as shape Key
    bpy.ops.object.modifier_apply(apply_as="SHAPE", modifier="Displace")

    # Change Keyname
    bpy.data.objects[name_geo].data.shape_keys.name = 'KeyBlob'


    # Set shapekey
    bpy.context.object.active_shape_key_index = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_min = -1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_max = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].value = 0.8
    
def convertMesh(object):
    activeObject(object)
    # Convert Mesh
    bpy.ops.object.convert(target='MESH')
    
def joinShapes(object1, object2):
    
    bpy.ops.object.select_all(action='DESELECT')
    blob1 = bpy.data.objects[object1]
    blob2 = bpy.data.objects[object2]
    blob1.select_set(True)
    blob2.select_set(True)
    bpy.context.view_layer.objects.active = blob2
    
    bpy.ops.object.join_shapes()
   
def subsurfShapekeys(base_geometry, name_sub):
    
    activeObject(base_geometry)
    
    # Duplicate object
    bpy.ops.object.duplicate_move()
    
    # applyDisplacement
    applyDisplace(base_geometry + '.001')

    # Reset all keys
    reset_shape_keys(0.0)
    del_shape_keys(base_geometry + '.001')
    apply_subsurf(name_sub)
    
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    #Select original and duplicate
    bpy.data.objects[base_geometry].select_set(True)
    bpy.ops.object.duplicate_move()
    reset_shape_keys(0.8)
    
    convertMesh(base_geometry + '.002')
    
    # Join keyshapes    
    joinShapes(base_geometry + '.002', base_geometry + '.001')

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    for i in ['', '.002']:
        bpy.data.objects[f'Blob{i}'].select_set(True)
        bpy.ops.object.delete()
     


def exportGeo(base_geometry, blob_texture, fileName): # base_geometry is str(name) object
    
    # All normals to the outside
    bpy.context.scene
    activeObject(base_geometry)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.editmode_toggle()

    # Export fbx + settings
    bpy.ops.export_scene.fbx(filepath=fileName, use_selection=True, global_scale=1.0, mesh_smooth_type='FACE',
                            use_mesh_modifiers=False, bake_anim_use_all_actions=False, object_types={'ARMATURE', 'MESH'})

    # remove all shape keys
    bpy.ops.object.shape_key_remove(all=True)


    # Remove all meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    bpy.ops.object.delete()
        
    # Remove all textures
    bpy.data.textures.remove(blob_texture, do_unlink=True)
    

# Variables
name_sub = 'Subdivider'
base_geometry = 'Blob'

# File name
number = 0


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            d = pickle.loads(data)
            
            # Parsing data for conditions
            toggle = d['toggle']
            noise = d['noise']
            strength = d['strength']
            number = d['number']
            
            if toggle == True:
                print(f"Noise is {noise} and strength is {strength}")
                # Create base geometry
                createSphere(base_geometry)

                # Create Displacement modifier
                blob_texture = createModifiers(base_geometry, name_sub, noise=random.random(), strength=random.random()) 
                number += 1
                fileName = f"D:\\_Projects\\_Pater_Noster_2020\\_ParametricBlob\_Objects\\parametricblob_{number}.fbx"
                # Apply subdivision
                meshExport = subsurfShapekeys(base_geometry, name_sub)

                exportGeo(base_geometry + '.001', blob_texture, fileName)
                
            conn.sendall(b'Done!')