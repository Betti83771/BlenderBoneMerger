import bpy
constr_influence_ui_script = """
import bpy
from bpy.types import Constraint
class ParentSwitchPanel(bpy.types.Panel):
    \"\"\"Creates a Panel that houses the constraint influence properties  \"\"\"
    bl_label = "Bone Merger: Parent Switch"
    bl_idname = "OBJECT_PT_BMParentSwitchPanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "Item"
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        return context.mode == 'POSE'


    def draw(self, context):
        use_showall = context.window_manager.bm_parsw_use_showall

        layout = self.layout
        row = layout.row()
        row.label(text="Influences:")

        posebones = []
        row = layout.row()
        row.prop(context.window_manager, "bm_parsw_use_showall")

        split = layout.split(factor=0.25)
        col1 = split.column()
        col2 = split.column()

        if not use_showall:
            if not context.active_pose_bone:
                return
            posebones.append(context.active_pose_bone)
        else:
            posebones.extend(context.object.pose.bones.values())

        for posebone in posebones:
            constraints = [const for const in posebone.constraints if const.name.startswith("bm_const2_")] 

            for constraint in constraints:
                bm_rels = context.object.data.bones[posebone.name].bm_relations
                rel = next((rel for rel in bm_rels if rel.bm_child_empty == constraint.target.name), None)
                if rel:
                    infl_label = rel.bm_external_parent + " (" +rel.bm_external_armature + ") "
                else:
                    infl_label = "Unknown parent"
                
                row = col1.row()
                row.label(text=posebone.name)

                row = col2.row()
                row.prop(constraint, 'influence', text=infl_label)

def constr_influence_panel_register():
    bpy.types.WindowManager.bm_parsw_use_showall = bpy.props.BoolProperty(name = "Show all", 
                                                    default=True,
                                                    description=\"\"\"If off, only shows the influences of the 
                                                    active bone.\"\"\")
    bpy.utils.register_class(ParentSwitchPanel)
 
def constr_influence_panel_unregister():
    bpy.utils.unregister_class(ParentSwitchPanel)

if __name__ == '__main__':
    constr_influence_panel_register()"""

def script_create_and_register():
    script = bpy.data.texts.new("constraint_influence_ui.py")
    script.write(constr_influence_ui_script)
    script.use_module = True

