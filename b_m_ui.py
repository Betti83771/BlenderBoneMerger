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
        row.prop(context.window_manager, 'bm_target_1', text='From', icon='ARMATURE_DATA')
        if context.window_manager.bm_target_1:
            row = layout.row()
            row.prop_search(context.window_manager, "bm_subtarget_1", context.window_manager.bm_target_1.data, "bones", text="")
        row = layout.row()
        row.prop(context.window_manager, 'bm_target_2', text='To', icon='ARMATURE_DATA')
        if context.window_manager.bm_target_2:
            row = layout.row()
            row.prop_search(context.window_manager, "bm_subtarget_2", context.window_manager.bm_target_2.data, "bones", text="")
        row = layout.row()
        row.operator("b_m.parent_constraint")

#TODO: add descriptions
def properties_register():
    bpy.types.WindowManager.bm_target_1 = bpy.props.PointerProperty(type=bpy.types.Object,
                                                name='Starting armature', 
                                                description="")
    bpy.types.WindowManager.bm_subtarget_1 = bpy.props.StringProperty(default="",
                                                name='Starting bone', 
                                                description="")
    bpy.types.WindowManager.bm_target_2 = bpy.props.PointerProperty(type=bpy.types.Object,
                                                name='Target armature', 
                                                description="")
    bpy.types.WindowManager.bm_subtarget_2 = bpy.props.StringProperty(default="",
                                                name='Target bone', 
                                                description="")
    bpy.types.WindowManager.intlist = bpy.props.IntProperty(default=0,
                                                name='intlist', 
                                                description="intprop for list")     

def properties_unregister():
    del bpy.types.WindowManager.bm_target_1
    del bpy.types.WindowManager.bm_subtarget_1
    del bpy.types.WindowManager.bm_target_2
    del bpy.types.WindowManager.bm_subtarget_2
    del bpy.types.WindowManager.intlist