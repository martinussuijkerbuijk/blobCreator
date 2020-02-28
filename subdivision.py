import bpy


def reset_shape_keys(key_value):
    shape_keys = bpy.data.shape_keys
    
    for key in shape_keys:
        for key_block in key.key_blocks:
            key_block.value = key_value
    
def del_shape_keys(object):
    active_object(object)
    bpy.ops.object.shape_key_remove(all=True)
    

def apply_subsurf():
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivider")

def active_object(object):
    bpy.ops.object.select_all(action='DESELECT')
    blob = bpy.data.objects[object]
    bpy.context.view_layer.objects.active = blob
    blob.select_set(True)
   
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
    active_object(object)
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
    
    
base_geometry = bpy.data.objects['Blob']
bpy.context.view_layer.objects.active = base_geometry

# Add subdivider
name_sub = 'Subdivider'
subd = base_geometry.modifiers.new(name_sub, type='SUBSURF')
base_geometry.modifiers[name_sub].levels = 1

# Duplicate object
bpy.ops.object.duplicate_move()

# applyDisplacement
applyDisplace('Blob.001')

# Reset all keys
reset_shape_keys(0.0)
del_shape_keys('Blob.001')
apply_subsurf()

# Deselect all
bpy.ops.object.select_all(action='DESELECT')

#Select original and duplicate
bpy.data.objects['Blob'].select_set(True)
bpy.ops.object.duplicate_move()
reset_shape_keys(0.8)

convertMesh('Blob.002')

# Join keyshapes    
joinShapes('Blob.002', 'Blob.001')

# Deselect all
bpy.ops.object.select_all(action='DESELECT')

for i in ['', '.002']:
    bpy.data.objects[f'Blob{i}'].select_set(True)
    bpy.ops.object.delete()
