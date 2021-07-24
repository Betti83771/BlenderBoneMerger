import bpy

#TODO: add descriptions

class BMRelations(bpy.types.PropertyGroup):
    bm_external_parent: bpy.props.StringProperty(default="",
                                                name='External parent', 
                                                description="External parent")
    bm_external_armature: bpy.props.StringProperty(default="",
                                                name='External armature', 
                                                description="External armature") 
    bm_child_empty: bpy.props.StringProperty(default="",
                                                name='Child empty', 
                                                description="Child empty")    
    bm_parent_empty: bpy.props.StringProperty(default="",
                                                name='Parent empty', 
                                                description="Parent empty") 
    bm_relation_slot: bpy.props.IntProperty(default=0,
                                                min=0,
                                                max=10,
                                                name='Relation slot', 
                                                description="Slot number of the relation")     
    

def properties_register():
    bpy.utils.register_class(BMRelations)
    bpy.types.WindowManager.bm_target_parent = bpy.props.PointerProperty(type=bpy.types.Object,
                                                name='Starting armature', 
                                                description="Starting armature")
    bpy.types.WindowManager.bm_subtarget_parent = bpy.props.StringProperty(default="",
                                                name='Starting bone', 
                                                description="Starting bone")
    bpy.types.WindowManager.bm_target_child = bpy.props.PointerProperty(type=bpy.types.Object,
                                                name='Target armature', 
                                                description="Target armature")
    bpy.types.WindowManager.bm_subtarget_child = bpy.props.StringProperty(default="",
                                                name='Target bone', 
                                                description="Target bone")
    bpy.types.WindowManager.bm_relation_slot_ui = bpy.props.IntProperty(default=0,
                                                min=0,
                                                max=10,
                                                name='Relation slot', 
                                                description="Slot where to create the relation, to support multiple switchable relations via constraint influence")     
    bpy.types.WindowManager.bm_use_snap = bpy.props.BoolProperty(default=False,
                                                name='Snap empty on parent', 
                                                description="If checked, the child bone's empty gets put in the parent's position.")   
    bpy.types.Bone.bm_relations = bpy.props.CollectionProperty(type=BMRelations,
                                                              name="Bone Merger relations",
                                                              description="Relations this bone is a child of in the 'Bone Merger' add-on")                      

def properties_unregister():
    del bpy.types.WindowManager.bm_target_parent
    del bpy.types.WindowManager.bm_subtarget_parent
    del bpy.types.WindowManager.bm_target_child
    del bpy.types.WindowManager.bm_subtarget_child
    del bpy.types.WindowManager.bm_relation_slot_ui
    del bpy.types.PoseBone.bm_relations
    bpy.utils.unregister_class(BMRelations)