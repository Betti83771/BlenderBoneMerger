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
                                                description="Choose which relation to overwrite. You can check out the slot number in the 'Manage relations' popup. The slot is recorded on the child; the child has slots, not the parent ")     
    bpy.types.WindowManager.bm_relation_mode_ui =  bpy.props.EnumProperty(name="Bone Merger Make Relation Mode",
                                                    description="""'Parent and constraint' mode. In 'overwrite' mode the relation will be updated as defined by the specified parent and child. 
                                                    In 'new' mode, a new relation will be created, but the child will keep the previous relations and the user would switch between parent.  Current mode""",
                                                    #update=update_mode,
                                                    items=( ('new', 'new', ''), ('overwrite', 'overwrite', '')),
                                                    default='new' )
    bpy.types.WindowManager.bm_use_snap = bpy.props.BoolProperty(default=False,
                                                name='Snap empty on parent', 
                                                description="If checked, the child bone's empty gets put in the parent's position.")   
    bpy.types.WindowManager.bm_hide_empties = bpy.props.BoolProperty(default=True,
                                                name='Hide new empties', 
                                                description="If checked, sets the newly created emties on hidden when creating a new relation.")   
    bpy.types.Bone.bm_relations = bpy.props.CollectionProperty(type=BMRelations,
                                                              name="Bone Merger relations",
                                                              description="Relations this bone is a child of in the 'Bone Merger' add-on",
                                                            override={'LIBRARY_OVERRIDABLE', 'USE_INSERTION'})                      

def properties_unregister():
    del bpy.types.WindowManager.bm_target_parent
    del bpy.types.WindowManager.bm_subtarget_parent
    del bpy.types.WindowManager.bm_target_child
    del bpy.types.WindowManager.bm_subtarget_child
    del bpy.types.WindowManager.bm_relation_mode_ui
    del bpy.types.WindowManager.bm_relation_slot_ui
    del bpy.types.Bone.bm_relations
    bpy.utils.unregister_class(BMRelations)