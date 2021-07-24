import bpy
from .bone_merger import b_m_checker, b_m_func, b_m_parent_rel_remove, b_m_auto_recognize_parenting, b_m_manual_register_relations



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
            if context.window_manager.bm_target_parent.data:
                if context.window_manager.bm_target_parent.data in bpy.data.armatures.values():
                    row = layout.row()
                    row.prop_search(context.window_manager, "bm_subtarget_parent", context.window_manager.bm_target_parent.data, "bones", text="")
        row = layout.row()
        row.prop(context.window_manager, 'bm_target_child', text='Child', icon='ARMATURE_DATA')
        if context.window_manager.bm_target_child:
            if context.window_manager.bm_target_child.data:
                if context.window_manager.bm_target_child.data in bpy.data.armatures.values():
                    row = layout.row()
                    row.prop_search(context.window_manager, "bm_subtarget_child", context.window_manager.bm_target_child.data, "bones", text="")
            
        row = layout.row()
        row.prop(context.window_manager, 'bm_relation_slot_ui')
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
    relation_slot: bpy.props.IntProperty()

    parenting_remove: bpy.props.BoolProperty(default=False, description="Remove")
    parenting_update: bpy.props.BoolProperty(default=False, description="Update")


class BMManageParenting(bpy.types.Operator):
    bl_idname = "wm.bm_manage_parenting"
    bl_label = "Manage Parenting"
    bl_options = {'UNDO'}

    links: bpy.props.CollectionProperty(type=BMParentingLink)
    register_new_link: bpy.props.BoolProperty(default=False)
    try_auto_link: bpy.props.BoolProperty(default=False, description="(Only works for bones for now)")

    def links_populate(self):
        self.links.clear()
        bm_chk_dict = b_m_checker()
        for link in bm_chk_dict.keys():
                new = self.links.add()

                new.bone_parent = bm_chk_dict[link][5]

                if bm_chk_dict[link][0] == 'BONE':
                    new.bone_child = link[0]

                new.arm_parent = bm_chk_dict[link][4]

                if bm_chk_dict[link][0] == 'BONE':
                    new.arm_child = bm_chk_dict[link][1]
                else:
                    new.arm_child = link[0]

                new.empty_parent = bm_chk_dict[link][2]

                new.empty_child = bm_chk_dict[link][3]

                new.relation_slot = link[1]


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
            row7 = col.row()
            row7.row().label(text="Relation slot:")
        
            col = split.column()
            col.row().label(text=link.bone_child)
            col.row().label(text=link.arm_child)
            col.row().label(text=link.empty_child)
            col.row().label(text=link.empty_parent)
            col.row().label(text=link.arm_parent)
            col.row().label(text=link.bone_parent)
            col.row().label(text=str(link.relation_slot))

            col = out_split.column()
            row = col.row()
            row.prop(link, 'parenting_remove',  text="", icon='REMOVE')
            row = col.row()
            row.prop(link, 'parenting_update',  text="Update", toggle=True)

        
        
        row = layout.row()
        layout.operator_context = 'INVOKE_DEFAULT'
       # row.prop(self, "register_new_link", text="Register new parenting", icon='ADD')
        row.operator("b_m.manual_parenting_popup", icon='ADD')
        row = layout.row()
        row.prop(self, "try_auto_link", text="Try auto recognize parenting", icon='ADD')

    def check(self, context):
        changed = False
        if self.register_new_link:
            self.register_new_link = False
            context.window_manager.invoke_popup()
            self.links_populate()
            changed = True


        if self.try_auto_link:
            self.try_auto_link = False
            self.links.clear()
            found_relations = b_m_auto_recognize_parenting()
            if found_relations == {}:
                def  message(self, context):
                   self.layout.label(text="No relations found", icon='INFO')
                context.window_manager.popup_menu(message)
            self.links_populate()
            changed = True

        for linki, link in enumerate(self.links):
            if link.parenting_remove:
               link.parenting_remove = False
               b_m_parent_rel_remove(link.bone_parent, link.bone_child,  link.arm_parent, link.arm_child, link.relation_slot)
               self.links.remove(linki)
               changed = True 

            if link.parenting_update:
               link.parenting_update = False
               b_m_func(link.bone_parent, link.bone_child,  bpy.data.objects[link.arm_parent], bpy.data.objects[link.arm_child], link.relation_slot)
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

class BMManualParentingPopup(bpy.types.Operator):
    bl_idname = "b_m.manual_parenting_popup"
    bl_label = "Manual register new parenting"
    
    empty_parent: bpy.props.StringProperty(name="Empty parent name")
    empty_child: bpy.props.StringProperty(name="Empty child name")

    def draw(self, context):
        layout = self.layout
        split = layout.split(factor=0.5)
        col1 = split.column()
        col1.row().label(text='Parent')
        if context.window_manager.bm_target_parent:
            if context.window_manager.bm_target_parent.data:
                if context.window_manager.bm_target_parent.data in bpy.data.armatures.values():
                    row = col1.row()
                    col1.row().label(text= "Bone")
        
        col1.row().label(text='Child')
        if context.window_manager.bm_target_child:
            if context.window_manager.bm_target_child.data:
                if context.window_manager.bm_target_child.data in bpy.data.armatures.values():
                    row = col1.row()
                    col1.row().label(text= "Bone")
        
        col1.row().label(text='Empty parent name')
        col1.row().label(text='Empty child name')
        col1.row().label(text='')


        col2 = split.column()
        row = col2.row()
        row.prop(context.window_manager, 'bm_target_parent',  icon='ARMATURE_DATA', text="")
        if context.window_manager.bm_target_parent:
            if context.window_manager.bm_target_parent.data:
                if context.window_manager.bm_target_parent.data in bpy.data.armatures.values():
                    row = col2.row()
                    row.prop_search(context.window_manager, "bm_subtarget_parent", context.window_manager.bm_target_parent.data, "bones", text="")
        row = col2.row()
        row.prop(context.window_manager, 'bm_target_child', icon='ARMATURE_DATA', text="")
        if context.window_manager.bm_target_child:
            if context.window_manager.bm_target_child.data:
                if context.window_manager.bm_target_child.data in bpy.data.armatures.values():
                    row = col2.row()
                    row.prop_search(context.window_manager, "bm_subtarget_child", context.window_manager.bm_target_child.data, "bones", text="")
        row = col2.row()
        row.prop(self, 'empty_parent', text="")

        row = col2.row()
        row.prop(self, 'empty_child', text="")

        row = layout.row()
        row.prop(context.window_manager, 'bm_relation_slot_ui')

    def check(self, context):
        return True
    
    def execute(self, context):
        report = b_m_manual_register_relations(context.window_manager.bm_subtarget_parent, context.window_manager.bm_subtarget_child, context.window_manager.bm_target_parent, context.window_manager.bm_target_child, self.empty_parent, self.empty_child, context.window_manager.bm_relation_slot_ui)
        if report == 'NO_CHILD_EMPTY':
            self.report(type={'ERROR'}, message="Can't find this child empty.")
        if report == 'NO_PARENT_EMPTY':
            self.report(type={'ERROR'}, message="Can't find this parent empty.")
        if report == 'REL_SLOT_FULL':
            self.report(type={'ERROR'}, message="This relation slot is already occupied. Please select another slot or update the relation.")
        if report == 'NO_CHILD_CONST':
            self.report(type={'ERROR'}, message="Can't find the constraint on the child.")
        if report == 'NO_PARENT_CONST':
            self.report(type={'ERROR'}, message="Can't find the constraint on the parent empty.")
        if report == 'SUCCESS':
            self.report(type={'INFO'}, message="Success!")
        return {'FINISHED'}

    def invoke(self, context, event):
        width = 300
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=width)


        



def bm_ui_register():
    bpy.utils.register_class(BoneMergerPanel)
    bpy.utils.register_class(BMParentingLink)
    bpy.utils.register_class(BMManageParenting)
    bpy.utils.register_class(BMManualParentingPopup)

def bm_ui_unregister():
    bpy.utils.unregister_class(BMManualParentingPopup)
    bpy.utils.unregister_class(BMManageParenting)
    bpy.utils.unregister_class(BMParentingLink)
    bpy.utils.unregister_class(BoneMergerPanel)
    
   
    