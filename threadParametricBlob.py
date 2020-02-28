import bpy
import random
import time
import threading


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

def startUpOSC(ip: str, port: int):
    
    bpy.data.window_managers["WinMan"].addosc_udp_in = ip
    bpy.data.window_managers["WinMan"].addosc_port_in = port
    bpy.ops.addosc.startudp()
    
    osc_monitor = bpy.data.window_managers["WinMan"].addosc_monitor = True
    
    item = scene.OSC_keys.add()
    item.data_path = "bpy.data.objects['Cube']"
    item.id = "hide_viewport"
    item.address = "/blender/toggle"
    item.osc_type = "boolean" 
    #item.idx = 0
    
    item = scene.OSC_keys.add()
    item.data_path = "bpy.data.objects['Cube']"
    item.id = "location[0]"
    item.address = "/blender/noise"
    item.osc_type = "float" 
    #item.idx = 0
    
    item = scene.OSC_keys.add()
    item.data_path = "bpy.data.objects['Cube']"
    item.id = "location[1]"
    item.address = "/blender/strength"
    item.osc_type = "float" 
    #item.idx = 0
    time.sleep(3)
    
    
def getInput():
    
    thread = threading.Thread(target=runOSC)
    thread.start()
    
    thread.join()
    
    #startOSC('127.0.0.1', 5005)
    

def runOSC():
    
    bpy.ops.addosc.startudp()
    
    toggle = scene.OSC_keys[0].value
    
    while toggle == False:
        print("No input received!")
        time.sleep(1)
    
    else:
        noise = float(scene.OSC_keys[1].value)
        strength = float(scene.OSC_keys[2].value)
        
        parametricBlob(noise, strength)
        
        print(noise)
        print(strength) 
        
        time.sleep(1)
    
    #bpy.ops.addosc.stopudp()
    
scene = bpy.context.scene

ip = '127.0.0.1'
port = 5005

startUpOSC(ip, port)
bpy.ops.addosc.stopudp()
runOSC()




