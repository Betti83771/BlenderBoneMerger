import bpy
from mathutils import Matrix

class BoneMergerOperator(bpy.types.Operator):
    """Creates a parenting chain as follows: 
    bone in starting bone prop -> empty -> empty -> bone in  target bone prop"""
    bl_idname = "b_m.parent_constraint"
    bl_label = "Parent Constraint"
    
    bl_options = {'REGISTER', 'UNDO'}
    

    @classmethod
    def poll(cls, context):
        return context.window_manager.bm_subtarget_2 and context.window_manager.bm_subtarget_1

    def execute(self, context):
        b_m_func(context.window_manager.bm_subtarget_1, context.window_manager.bm_subtarget_2, context.window_manager.bm_target_1, context.window_manager.bm_target_2)
        return {'FINISHED'}

def snap_objs(to_snap, target):
    matrix_1 = target.matrix_world.copy()
    to_snap.matrix_world =  target.matrix_world

def b_m_func(bone_tg_1, bone_tg_2,  arm_1, arm_2):
    #create the empties
    empty1 = bpy.data.objects.new( bone_tg_1, None )
    bpy.context.scene.collection.objects.link(empty1)
    matrix_1 = arm_1.pose.bones[bone_tg_1].matrix.copy()
    empty1.matrix_world = arm_1.matrix_world @ matrix_1
    
    empty2 = bpy.data.objects.new(bone_tg_2, None )
    bpy.context.scene.collection.objects.link(empty2)
    matrix_2 = arm_2.pose.bones[bone_tg_2].matrix.copy()
    empty2.matrix_world = arm_2.matrix_world @ matrix_2

    #snap the second empty on the first
    snap_objs(empty2, empty1)

    #make the constraints
    const1 = empty1.constraints.new(type='COPY_TRANSFORMS')
    const1.target = arm_1
    const1.subtarget = bone_tg_1
    const2 = arm_2.pose.bones[bone_tg_2].constraints.new(type='COPY_TRANSFORMS')
    const2.target = empty2

    #parent the empties
    empty2_mat_bk = empty2.matrix_world.copy()
    empty2.parent = empty1
    empty2.matrix_world = empty2_mat_bk

    
    
    return