import bpy
import time
import socket
import pickle
import random


def reset_shape_keys(key_value):
    shape_keys = bpy.data.shape_keys
    
    for key in shape_keys:
        for key_block in key.key_blocks:
            key_block.value = key_value
    
def del_shape_keys():
    
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Blob.001'].select_set(True)
    bpy.context.object.active_shape_key_index = 1
    bpy.ops.object.shape_key_remove(all=True)
    

def apply_subsurf():
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivider")

def subdivisionObject(name_object):
    base_geometry = bpy.data.objects[name_object]

    # Add subdivider
    name_sub = 'Subdivider'
    subd = base_geometry.modifiers.new(name_sub, type='SUBSURF')
    base_geometry.modifiers[name_sub].levels = 1

    # Duplicate object
    bpy.ops.object.duplicate_move()

    # Reset all keys
    reset_shape_keys(0)
    del_shape_keys()
    apply_subsurf()

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    #Select object
    bpy.data.objects['Blob'].select_set(True)
    bpy.ops.object.duplicate_move()
    reset_shape_keys(0.8)

    # Convert Mesh
    bpy.ops.object.select_all(action='DESELECT')
    blob_2 = bpy.data.objects['Blob.002']
    blob_2.select_set(True)
    bpy.context.view_layer.objects.active = blob_2
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.select_all(action='DESELECT')
    
    blob_1 = bpy.data.objects['Blob.001']
    blob_2 = bpy.data.objects['Blob.002']
    blob_1.select_set(True)
    blob_2.select_set(True)
    bpy.context.view_layer.objects.active = blob_1
    

    # Join keyshapes
    bpy.ops.object.join_shapes()

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')


    bpy.data.objects['Blob'].select_set(True)
    bpy.ops.object.delete()
    bpy.data.objects['Blob.002'].select_set(True)
    bpy.ops.object.delete()
    bpy.data.objects['Blob.001'].name = 'Blob'
    bpy.data.objects['Blob'].select_set(True)
    bpy.context.active_object

def blobNeutral(size: float, depth: int, turbulence: float, file_nr: int):
    
    name_geo = 'Blob'
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, enter_editmode=False, location=(0, 0, 0))
    base_geometry = bpy.data.objects['Sphere']
    base_geometry.name = name_geo

    # Smooth Shading
    bpy.ops.object.shade_smooth()
    
    # Create displacement modifier
    modifier = base_geometry.modifiers.new(name="Displace", type='DISPLACE')

    # Create Texture
    name_text = 'blob_neutral'
    blob_texture = bpy.data.textures.new(name=name_text, type='MARBLE')

    modifier.texture = bpy.data.textures[name_text]
    modifier.texture.noise_scale = size #float 0 - 2
    modifier.texture.noise_depth = depth #int 0 - 4 
    modifier.texture.turbulence = turbulence #float 1 - 30

    # Apply as shape Key
    bpy.ops.object.modifier_apply(apply_as="SHAPE", modifier="Displace")

    # Change Keyname
    bpy.data.objects[name_geo].data.shape_keys.name = 'KeyBlob'


    # Set shapekey
    bpy.context.object.active_shape_key_index = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_min = -1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_max = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].value = 0.8
    
    # Apply subsurf
    subdivisionObject(name_geo)
    
    # All normals to the outside
    ob = bpy.data.objects['Blob']
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    # Export fbx + settings
    bpy.ops.export_scene.fbx(filepath=f"D:\\_Projects\\_Pater_Noster_2020\\_ParametricBlob\\_Objects\\parametricblob_neutral_{file_nr}.fbx", use_selection=True, global_scale=1.0, mesh_smooth_type='FACE', use_mesh_modifiers=False, bake_anim_use_all_actions=False, object_types={'ARMATURE', 'MESH'})

    bpy.ops.object.delete()
    
    # Remove all meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    bpy.ops.object.delete()
        
    # Remove all textures
    bpy.data.textures.remove(blob_texture, do_unlink=True)
    
    # remove all shape keys
    #bpy.ops.object.shape_key_remove(all=True)
    
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    
def blobHappy(repeat_x: int, repeat_y: int, brightness: float, file_nr: int):
    
    name_geo = 'Blob'
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, enter_editmode=False, location=(0, 0, 0))
    base_geometry = bpy.data.objects['Sphere']
    base_geometry.name = name_geo

    # Smooth Shading
    bpy.ops.object.shade_smooth()

    # Create displacement modifier
    modifier = base_geometry.modifiers.new(name="Displace", type='DISPLACE')
    
    # Create Texture
    name_text = 'blob_happy'
    blob_texture = bpy.data.textures.new(name=name_text, type='IMAGE')
    bpy.data.textures["blob_happy"].name = "blob_happy"

    bpy.ops.image.open(filepath="//_Maps\Emotion_happy.png", \
                        directory="D:\\_Projects\\_Pater_Noster_2020\\_ParametricBlob\\_Maps\\", \
                        files=[{"name":"Emotion_happy.png", "name":"Emotion_happy.png"}], \
                        show_multiview=False)
   
    
    bpy.data.images["Emotion_happy.png"].pack()#.name = "Emotion_happy.png"
    blob_texture.image = bpy.data.images['Emotion_happy.png']

    # set parameters
    modifier.texture = blob_texture #bpy.data.textures[name_text]
    modifier.texture.repeat_x = repeat_x #int 1 - 3
    modifier.texture.repeat_y = repeat_y #int 1 - 3 
    modifier.texture.intensity = brightness #float 0.1 - 1.4
    
   
    # Apply as shape Key
    bpy.ops.object.modifier_apply(apply_as="SHAPE", modifier="Displace")

    # Change Keyname
    bpy.data.objects[name_geo].data.shape_keys.name = 'KeyBlob'


    # Set shapekey
    bpy.context.object.active_shape_key_index = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_min = -1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_max = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].value = 0.8
    
    # Apply subsurf
    subdivisionObject(name_geo)
    
    # All normals to the outside
    ob = bpy.data.objects['Blob']
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    # Export fbx + settings
    bpy.ops.export_scene.fbx(filepath=f"D:\\_Projects\\_Pater_Noster_2020\\_ParametricBlob\_Objects\\parametricblob_happy_{file_nr}.fbx", use_selection=True, global_scale=1.0, mesh_smooth_type='FACE',
                            use_mesh_modifiers=False, bake_anim_use_all_actions=False, object_types={'ARMATURE', 'MESH'})

       
    bpy.ops.object.delete()
    
    # Remove all meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    bpy.ops.object.delete()
        
    # Remove all textures
    bpy.data.textures.remove(blob_texture, do_unlink=True)
    
    # remove all shape keys
    #bpy.ops.object.shape_key_remove(all=True)
    
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)    
    

def blobAnger(brightness: float, contrast: float, file_nr: int):
    
    name_geo = 'Blob'
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, enter_editmode=False, location=(0, 0, 0))
    base_geometry = bpy.data.objects['Sphere']
    base_geometry.name = name_geo

    # Smooth Shading
    bpy.ops.object.shade_smooth()
    
    # Create displacement modifier
    modifier = base_geometry.modifiers.new(name="Displace", type='DISPLACE')

    # Create Texture
    name_text = 'blob_neutral'
    blob_texture = bpy.data.textures.new(name=name_text, type='DISTORTED_NOISE')

    modifier.texture = bpy.data.textures[name_text]
    modifier.texture.intensity = brightness #float 1 - 1.5
    modifier.texture.contrast = contrast #int 0 - 4 

    # Apply as shape Key
    bpy.ops.object.modifier_apply(apply_as="SHAPE", modifier="Displace")

    # Change Keyname
    bpy.data.objects[name_geo].data.shape_keys.name = 'KeyBlob'


    # Set shapekey
    bpy.context.object.active_shape_key_index = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_min = -1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_max = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].value = 0.8
    
    # Apply subsurf
    subdivisionObject(name_geo)
    
    # All normals to the outside
    ob = bpy.data.objects['Blob']
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    # Export fbx + settings
    bpy.ops.export_scene.fbx(filepath=f"D:\\_Projects\\_Pater_Noster_2020\\_ParametricBlob\\_Objects\\parametricblob_anger_{file_nr}.fbx", use_selection=True, global_scale=1.0, mesh_smooth_type='FACE', use_mesh_modifiers=False, bake_anim_use_all_actions=False, object_types={'ARMATURE', 'MESH'})

    bpy.ops.object.delete()
    
    # Remove all meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    bpy.ops.object.delete()
        
    # Remove all textures
    bpy.data.textures.remove(blob_texture, do_unlink=True)
    
    # remove all shape keys
    #bpy.ops.object.shape_key_remove(all=True)
    
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

def blobSurprise(brightness: float, contrast: float, file_nr: int):
    
    name_geo = 'Blob'
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, enter_editmode=False, location=(0, 0, 0))
    base_geometry = bpy.data.objects['Sphere']
    base_geometry.name = name_geo

    # Smooth Shading
    bpy.ops.object.shade_smooth()
    
    # Create displacement modifier
    modifier = base_geometry.modifiers.new(name="Displace", type='DISPLACE')

    # Create Texture
    name_text = 'blob_neutral'
    blob_texture = bpy.data.textures.new(name=name_text, type='WOOD')

    modifier.texture = bpy.data.textures[name_text]
    modifier.texture.intensity = brightness #float 0.4 - 1
    modifier.texture.contrast = contrast #float 1 - 2

    # Apply as shape Key
    bpy.ops.object.modifier_apply(apply_as="SHAPE", modifier="Displace")

    # Change Keyname
    bpy.data.objects[name_geo].data.shape_keys.name = 'KeyBlob'


    # Set shapekey
    bpy.context.object.active_shape_key_index = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_min = -1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_max = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].value = 0.8
    
    # Apply subsurf
    subdivisionObject(name_geo)
    
    # All normals to the outside
    ob = bpy.data.objects['Blob']
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    # Export fbx + settings
    bpy.ops.export_scene.fbx(filepath=f"D:\\_Projects\\_Pater_Noster_2020\\_ParametricBlob\\_Objects\\parametricblob_surprise_{file_nr}.fbx", use_selection=True, global_scale=1.0, mesh_smooth_type='FACE', use_mesh_modifiers=False, bake_anim_use_all_actions=False, object_types={'ARMATURE', 'MESH'})

    bpy.ops.object.delete()
    
    # Remove all meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    bpy.ops.object.delete()
        
    # Remove all textures
    bpy.data.textures.remove(blob_texture, do_unlink=True)
    
    # remove all shape keys
    #bpy.ops.object.shape_key_remove(all=True)
    
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    
def blobSad(brightness: float, contrast: float, file_nr: int):
    
    name_geo = 'Blob'
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, enter_editmode=False, location=(0, 0, 0))
    base_geometry = bpy.data.objects['Sphere']
    base_geometry.name = name_geo

    # Smooth Shading
    bpy.ops.object.shade_smooth()
    
    # Create displacement modifier
    modifier = base_geometry.modifiers.new(name="Displace", type='DISPLACE')

    # Create Texture
    name_text = 'blob_neutral'
    blob_texture = bpy.data.textures.new(name=name_text, type='BLEND')
    blob_texture.progression = 'RADIAL'

    modifier.texture = bpy.data.textures[name_text]
    modifier.texture.intensity = brightness #float 0.3 - 1.5
    modifier.texture.contrast = contrast #float 1 - 3.5

    # Apply as shape Key
    bpy.ops.object.modifier_apply(apply_as="SHAPE", modifier="Displace")

    # Change Keyname
    bpy.data.objects[name_geo].data.shape_keys.name = 'KeyBlob'


    # Set shapekey
    bpy.context.object.active_shape_key_index = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_min = -1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].slider_max = 1
    bpy.data.shape_keys["KeyBlob"].key_blocks["Displace"].value = 0.8
    
    # Apply subsurf
    subdivisionObject(name_geo)
    
    # All normals to the outside
    ob = bpy.data.objects['Blob']
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    # Export fbx + settings
    bpy.ops.export_scene.fbx(filepath=f"D:\\_Projects\\_Pater_Noster_2020\\_ParametricBlob\\_Objects\\parametricblob_sad_{file_nr}.fbx", use_selection=True, global_scale=1.0, mesh_smooth_type='FACE', use_mesh_modifiers=False, bake_anim_use_all_actions=False, object_types={'ARMATURE', 'MESH'})

    bpy.ops.object.delete()
    
    # Remove all meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    bpy.ops.object.delete()
        
    # Remove all textures
    bpy.data.textures.remove(blob_texture, do_unlink=True)
    
    # remove all shape keys
    #bpy.ops.object.shape_key_remove(all=True)
    
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    
    
    
#blobNeutral(size=random.uniform(0,2), depth=random.randint(1,4), turbulence=random.uniform(0,30), file_nr=13)
#blobHappy(repeat_x=random.randint(1,3), repeat_y=random.randint(1,3), brightness=random.uniform(0.1,1.4), file_nr=14)
#blobAnger(brightness=random.uniform(1,1.5), contrast=random.uniform(1,2.5), file_nr=15)
#blobSurprise(brightness=random.uniform(0.4,1), contrast=random.uniform(1,2), file_nr=16)
#blobSad(brightness=random.uniform(0.3,1.5), contrast=random.uniform(1,3.5), file_nr=17)
    

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
                print("No data received!")
            else:
                d = pickle.loads(data)
                
                # Parsing data for conditions
                name = d['name']
                
                if name == 'neutral':
                    size = d['size']
                    depth = d['depth']
                    turbulence = d['turbulence']
                    file_nr = d['file_nr']
                    blobNeutral(size, depth, turbulence, file_nr)
                if name == 'happy':
                    repeat_x = d['repeat_x']
                    repeat_y = d['repeat_y']
                    brightness = d['brightness']
                    file_nr = d['file_nr']
                    blobHappy(repeat_x, repeat_y, brightness, file_nr)
                if name == 'angry':
                    brightness = d['brightness']
                    contrast = d['contrast']
                    file_nr = d['file_nr']
                    blobAnger(brightness, contrast, file_nr)
                if name == 'surprise':
                    brightness = d['brightness']
                    contrast = d['contrast']
                    file_nr = d['file_nr']
                    blobSurprise(brightness, contrast, file_nr)
                if name == 'sad':
                    brightness = d['brightness']
                    contrast = d['contrast']
                    file_nr = d['file_nr']
                    blobSad(brightness, contrast, file_nr)
                    
                
            conn.sendall(b'Done!')




