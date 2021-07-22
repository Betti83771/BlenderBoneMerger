import bpy
from .bone_merger import b_m_checker, b_m_func, b_m_parent_rel_remove

class BoneMergerPanel(bpy.types.Panel):
    """Creates a Panel that houses the buttons  """
    bl_label = "Bone Merger"
    bl_idname = "OBJECT_PT_BMPanel"
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
        row = layout.row()
        row.operator("wm.bm_manage_parenting")

class BMParentingLink(bpy.types.PropertyGroup):
    bone_parent: bpy.props.StringProperty(name='Parent bone', 
                                          description="Starting bone")
    bone_child: bpy.props.StringProperty(name='Child bone', 
                                         description="Target bone")
    arm_parent: bpy.props.StringProperty(name='Parent armature', 
                                                description="Starting armature")
    arm_child: bpy.props.StringProperty(name='Child armature')
    empty_parent: bpy.props.StringProperty(name='Empty parent', 
                                                description="")
    empty_child: bpy.props.StringProperty(name='Empty child', 
                                                description="")

    parenting_remove: bpy.props.BoolProperty(default=False, description="Remove")
    parenting_update: bpy.props.BoolProperty(default=False, description="Update")


class BMManageParenting(bpy.types.Operator):
    bl_idname = "wm.bm_manage_parenting"
    bl_label = "Manage Parenting"
    bl_options = {'UNDO'}

    links: bpy.props.CollectionProperty(type=BMParentingLink)
    register_new_link: bpy.props.BoolProperty(default=False)
    try_auto_link: bpy.props.BoolProperty(default=False)

    def links_populate(self):
        self.links.clear()
        bm_chk_dict = b_m_checker()
        for link in bm_chk_dict.keys():
                new = self.links.add()

                new.bone_parent = bm_chk_dict[link][5]

                if bm_chk_dict[link][0] == 'BONE':
                    new.bone_child = link 

                new.arm_parent = bm_chk_dict[link][4]

                if bm_chk_dict[link][0] == 'BONE':
                    new.arm_child = bm_chk_dict[link][1]
                else:
                    new.arm_child = link

                new.empty_parent = bm_chk_dict[link][2]

                new.empty_child = bm_chk_dict[link][3]



    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="All Bone Merger parentings")

        row = layout.row()
        row.label(text="Current scene: {0}".format(bpy.context.scene.name))

        

        for link in self.links:
            row = layout.row()
            out_split=row.split(factor=0.85)
            box = out_split.box()
            split = box.split(align=True, factor=0.25)
            col = split.column()
            row1 = col.row()
            row1.row().label(text="Child Bone:")
            row2 = col.row()
            row2.row().label(text="Child:")
            row3 = col.row()
            row3.row().label(text="Child Empty:")
            row4 = col.row()
            row4.row().label(text="Parent Emprty:")
            row5 = col.row()
            row5.row().label(text="Parent:")
            row6 = col.row()
            row6.row().label(text="Parent Bone:")
        
            col = split.column()
            col.row().label(text=link.bone_child)
            col.row().label(text=link.arm_child)
            col.row().label(text=link.empty_child)
            col.row().label(text=link.empty_parent)
            col.row().label(text=link.arm_parent)
            col.row().label(text=link.bone_parent)

            col = out_split.column()
            row = col.row()
            row.prop(link, 'parenting_remove',  text="", icon='REMOVE')
            row = col.row()
            row.prop(link, 'parenting_update',  text="Update", toggle=True)

        
        row = layout.row()
        row.prop(self, "register_new_link", text="Register new parenting", icon='ADD')
        row = layout.row()
        row.prop(self, "try_auto_link", text="Try auto recognize parenting", icon='ADD')

    def check(self, context):
        changed = False
        if self.register_new_link:
            self.register_new_link = False
            #call operator /func /whatever
            changed = True

        if self.try_auto_link:
            self.try_auto_link = False
            #call operator /func /whatever
            changed = True

        for linki, link in enumerate(self.links):
            if link.parenting_remove:
               link.parenting_remove = False
               b_m_parent_rel_remove(link.bone_parent, link.bone_child,  link.arm_parent, link.arm_child)
               self.links.remove(linki)
               changed = True 

            if link.parenting_update:
               link.parenting_update = False
               b_m_func(link.bone_parent, link.bone_child,  link.arm_parent, link.arm_child)
               changed = True 
        return changed

    def execute(self, context):
        self.links.clear()
        return {'FINISHED'}
    
    def invoke(self, context, event):
        #populate self.links func
        self.links_populate()
        width = 400
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=width)



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