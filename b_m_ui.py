import bpy

class BoneMergerPanel(bpy.types.Panel):
    """Creates a Panel that houses the buttons  """
    bl_label = "Bone Merger"
    bl_idname = "OBJECT_PT_MBPanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "Bone Merger"
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Parent and constraint")
        row = layout.row()
        row.prop(context.window_manager, 'bm_target_parent', text='Parent', icon='ARMATURE_DATA')
        if context.window_manager.bm_target_parent:
            row = layout.row()
            row.prop_search(context.window_manager, "bm_subtarget_parent", context.window_manager.bm_target_parent.data, "bones", text="")
        row = layout.row()
        row.prop(context.window_manager, 'bm_target_child', text='Child', icon='ARMATURE_DATA')
        if context.window_manager.bm_target_child:
            row = layout.row()
            row.prop_search(context.window_manager, "bm_subtarget_child", context.window_manager.bm_target_child.data, "bones", text="")
            
        row = layout.row()
        row.prop(context.window_manager, 'bm_use_snap')
        row = layout.row()
        row.operator("b_m.parent_constraint")

#TODO: add descriptions
def properties_register():
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
    bpy.types.WindowManager.intlist = bpy.props.IntProperty(default=0,
                                                name='intlist', 
                                                description="intprop for list")     
    bpy.types.WindowManager.bm_use_snap = bpy.props.BoolProperty(default=False,
                                                name='Snap empty on parent', 
                                                description="If checked, the child bone's empty gets put in the parent's position.")   
    bpy.types.Bone.bm_external_parent = bpy.props.StringProperty(default="",
                                                name='External parent', 
                                                description="External parent")
    bpy.types.Bone.bm_external_armature = bpy.props.StringProperty(default="",
                                                name='External armature', 
                                                description="External armature")       
    bpy.types.Bone.bm_child_empty = bpy.props.StringProperty(default="",
                                                name='Child empty', 
                                                description="Child empty")     
    bpy.types.Bone.bm_parent_empty = bpy.props.StringProperty(default="",
                                                name='Parent empty', 
                                                description="Parent empty")                                 

def properties_unregister():
    del bpy.types.WindowManager.bm_target_parent
    del bpy.types.WindowManager.bm_subtarget_parent
    del bpy.types.WindowManager.bm_target_child
    del bpy.types.WindowManager.bm_subtarget_child
    del bpy.types.WindowManager.intlist
    del bpy.types.PoseBone.bm_external_armature
    del bpy.types.PoseBone.bm_external_parent