import bpy
import time
import threading
import socket
import pickle


def parametricBlob(noise, strength):
    
    
    name_geo = 'Blob'
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, enter_editmode=False, location=(0, 0, 0))
    base_geometry = bpy.data.objects['Sphere']
    base_geometry.name = name_geo

    # Smooth Shading
    bpy.ops.object.shade_smooth()

    # Add subdivider
    name_sub = 'Subdivider'
    subd = base_geometry.modifiers.new(name='Subdivider', type='SUBSURF')
    base_geometry.modifiers[name_sub].levels = 1
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=name_sub)

    modifier = base_geometry.modifiers.new(name="Displace", type='DISPLACE')

    # Create Texture
    name_text = 'blob_text'
    blob_texture = bpy.data.textures.new(name=name_text, type='MARBLE')

    modifier.texture = bpy.data.textures[name_text]
    modifier.texture.noise_scale = noise #random.random() #0.25
    modifier.strength = strength #random.random() #0.4


    # Apply as shape Key
    bpy.ops.object.modifier_apply(apply_as="SHAPE", modifier="Displace")

    # Change Keyname
    bpy.data.objects[name_geo].data.shape_keys.name = 'KeyBlob'


    # Set shapekey
    bpy.context.object.active_shape_key_index = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_min = -1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_max = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].value = 0.8

    # All normals to the outside
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.editmode_toggle()

    # Export fbx + settings
    bpy.ops.export_scene.fbx(filepath="D:\\_Projects\\_Pater_Noster_2020\\_ParametricBlob\_Objects\\parametricblob.fbx", use_selection=True, global_scale=1.0, mesh_smooth_type='FACE',
                            use_mesh_modifiers=False, bake_anim_use_all_actions=False, object_types={'ARMATURE', 'MESH'})

    # remove all shape keys
    bpy.ops.object.shape_key_remove(all=True)


    # Remove all meshes
    #for mesh in bpy.data.meshes:
    #    bpy.data.meshes.remove(mesh)
    bpy.ops.object.delete()
        
    # Remove all textures
    bpy.data.textures.remove(blob_texture, do_unlink=True)

    
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
            
            if toggle == True:
                print(f"Noise is {noise} and strength is {strength}")
                parametricBlob(noise, strength)
            conn.sendall(b'Done!')



