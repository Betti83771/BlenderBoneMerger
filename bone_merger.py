import bpy
from mathutils import Matrix

class BoneMergerOperator(bpy.types.Operator):
    """Creates a parenting chain as follows: 
    bone in starting bone prop -> empty -> empty -> bone in  target bone prop"""
    bl_idname = "b_m.parent_constraint"
    bl_label = "Parent and Constraint"
    
    bl_options = {'REGISTER', 'UNDO'}
    

    @classmethod
    def poll(cls, context):
        return context.window_manager.bm_subtarget_parent

    def execute(self, context):
        b_m_func(context.window_manager.bm_subtarget_parent, context.window_manager.bm_subtarget_child, context.window_manager.bm_target_parent, context.window_manager.bm_target_child)
        return {'FINISHED'}

def snap_objs(to_snap, target):
    to_snap.matrix_world =  target.matrix_world

def b_m_func(bone_parent, bone_child,  arm_parent, arm_child):
    bm_parent_empty = arm_child.data.bones[bone_child].bm_parent_empty
    bm_child_empty = arm_child.data.bones[bone_child].bm_child_empty
    #check for empties or create the new ones
    if bm_parent_empty != "":
        empty1 = bpy.data.objects[bm_parent_empty]
    else:
        empty1 = bpy.data.objects.new( bone_parent, None )
        empty1.empty_display_type = 'CUBE'
        bpy.context.scene.collection.objects.link(empty1)
        matrix_1 = arm_parent.pose.bones[bone_parent].matrix.copy()
        empty1.matrix_world = arm_parent.matrix_world @ matrix_1
    
    if bm_child_empty != "":
        empty2 = bpy.data.objects[bm_child_empty]
    else:
        empty2 = bpy.data.objects.new(bone_child, None )
        empty2.empty_display_type = 'SPHERE'
        bpy.context.scene.collection.objects.link(empty2)
        matrix_2 = arm_child.pose.bones[bone_child].matrix.copy()
        empty2.matrix_world = arm_child.matrix_world @ matrix_2

    #snap the second empty on the first
    if bpy.context.window_manager.bm_use_snap:
        snap_objs(empty2, empty1) 

    #make the constraints
    const1 = next((const for const in empty1.constraints if const.name == 'bm_const1'), None)
    const2 = next((const for const in arm_child.pose.bones[bone_child].constraints if const.name == 'bm_const2'), None)
    if not const1:
        const1 = empty1.constraints.new(type='COPY_TRANSFORMS')
        const1.name = 'bm_const1'
    const1.target = arm_parent
    const1.subtarget = bone_parent
    if not const2:
        const2 = arm_child.pose.bones[bone_child].constraints.new(type='COPY_TRANSFORMS')
        const2.name = 'bm_const2'
    const2.target = empty2
    

    #parent the empties
    empty2_mat_bk = empty2.matrix_world.copy()
    empty2.parent = empty1
    empty2.matrix_world = empty2_mat_bk

    #set the external parent and empty properties
    arm_child.data.bones[bone_child].bm_external_armature = arm_parent.name
    arm_child.data.bones[bone_child].bm_external_parent = bone_parent
    arm_child.data.bones[bone_child].bm_child_empty = empty2.name
    arm_child.data.bones[bone_child].bm_parent_empty = empty1.name
    
    return