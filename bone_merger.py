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
        return context.window_manager.bm_target_parent and context.window_manager.bm_target_child

    def execute(self, context):
        b_m_func(context.window_manager.bm_subtarget_parent, context.window_manager.bm_subtarget_child, context.window_manager.bm_target_parent, context.window_manager.bm_target_child)
        return {'FINISHED'}

def snap_objs(to_snap, target):
    to_snap.matrix_world =  target.matrix_world

def b_m_func(bone_parent, bone_child,  arm_parent, arm_child):
    if bone_child != "":
        bm_parent_empty = arm_child.data.bones[bone_child].bm_parent_empty
        bm_child_empty = arm_child.data.bones[bone_child].bm_child_empty
    else:
        if 'bm_parent_empty' in arm_child.keys():
            bm_parent_empty = arm_child['bm_parent_empty']
        else:
            bm_parent_empty = ""

        if 'bm_child_empty' in arm_child.keys():
            bm_child_empty = arm_child['bm_child_empty']
        else:
            bm_child_empty = ""
        
    #check for empties or create the new ones
    if bm_parent_empty != "":
        empty1 = bpy.data.objects[bm_parent_empty]
    else:
        empty1 = bpy.data.objects.new(arm_parent.name + "_" + bone_parent, None)
        empty1.empty_display_type = 'CUBE'
        bpy.context.scene.collection.objects.link(empty1)
        if bone_parent != "":
            matrix_1 = arm_parent.pose.bones[bone_parent].matrix.copy()
            empty1.matrix_world = arm_parent.matrix_world @ matrix_1
        else:
            empty1.matrix_world = arm_parent.matrix_world

    if bm_child_empty != "":
        empty2 = bpy.data.objects[bm_child_empty]
    else:
        empty2 = bpy.data.objects.new(arm_child.name + "_" + bone_child, None )
        empty2.empty_display_type = 'SPHERE'
        bpy.context.scene.collection.objects.link(empty2)
        if bone_child != "":
            matrix_2 = arm_child.pose.bones[bone_child].matrix.copy()
            empty2.matrix_world = arm_child.matrix_world @ matrix_2
        else:
            empty2.matrix_world = arm_child.matrix_world

    #snap the second empty on the first
    if bpy.context.window_manager.bm_use_snap:
        snap_objs(empty2, empty1) 

    #make the constraints
    const1 = next((const for const in empty1.constraints if const.name == 'bm_const1'), None)
    if bone_child != "":
        const2 = next((const for const in arm_child.pose.bones[bone_child].constraints if const.name == 'bm_const2'), None)
    else:
        const2 = next((const for const in arm_child.constraints if const.name == 'bm_const2'), None)
    if not const1:
        const1 = empty1.constraints.new(type='COPY_TRANSFORMS')
        const1.name = 'bm_const1'
    const1.target = arm_parent
    const1.subtarget = bone_parent
    if not const2:
        if bone_child != "":
            const2 = arm_child.pose.bones[bone_child].constraints.new(type='COPY_TRANSFORMS')
        else:
            const2 = arm_child.constraints.new(type='COPY_TRANSFORMS')
        const2.name = 'bm_const2'
    const2.target = empty2
    

    #parent the empties
    empty2_mat_bk = empty2.matrix_world.copy()
    empty2.parent = empty1
    empty2.matrix_world = empty2_mat_bk

    #set the external parent and empty properties
    #print(arm_child.data.bones[bone_child].bm_external_armature, arm_child.data.bones[bone_child].bm_external_parent, arm_child.data.bones[bone_child].bm_parent_empty)
    if bone_child != "":
        arm_child.data.bones[bone_child].bm_external_armature = arm_parent.name
        if bone_parent != "":
            arm_child.data.bones[bone_child].bm_external_parent = bone_parent
        else:
            arm_child.data.bones[bone_child].bm_external_parent = ""
        arm_child.data.bones[bone_child].bm_child_empty = empty2.name
        arm_child.data.bones[bone_child].bm_parent_empty = empty1.name
    else:
        arm_child["bm_external_armature"] = arm_parent.name
        arm_child["bm_child_empty"] = empty2.name
        arm_child["bm_parent_empty"] = empty1.name
        if bone_parent != "":
            arm_child["bm_external_parent"] = bone_parent
        else:
            if 'bm_external_parent' in arm_child.keys():
                del arm_child["bm_external_parent"]
            

    #print(arm_child.data.bones[bone_child].bm_external_armature, arm_child.data.bones[bone_child].bm_external_parent, arm_child.data.bones[bone_child].bm_parent_empty)
    
    return

def b_m_checker():
    """Checks all the bone merger parenting relations in the scene. Returns dictionary -  child name: relationship details (5 props + bone_or_obj)"""
    bm_chk_dict = {}
    # THIS IS THE OUTPUT DICTIONARY STRUCTURE
    # { name: [
    #0 bone_or_obj
    #1 arm_child 
    #2 parent_empty
    #3 child_empty
    #4 arm_parent
    #5 bone_parent
    # ]  }
    for obj in bpy.context.scene.objects:
        if not 'bm_external_armature' in obj.keys():
            continue
        print(obj) #check if it's not processing all objects but only useful ones
        parent_empty = ""
        child_empty = ""
        arm_parent = ""
        bone_parent = ""
        if 'bm_parent_empty' in obj.keys():
            parent_empty = obj['bm_parent_empty']
        if 'bm_child_empty' in obj.keys():
            child_empty = obj['bm_child_empty']
        if 'bm_external_armature' in obj.keys():
            arm_parent = obj['bm_external_armature']
        if 'bm_external_parent' in obj.keys():
            bone_parent = obj['bm_external_parent']
        
        bm_chk_dict[obj.name] = ['OBJ', "", parent_empty, child_empty, arm_parent, bone_parent]
    
    for armature in [arm for arm in bpy.context.scene.objects if arm.data in bpy.data.armatures.values()]:
        for bone in armature.data.bones:
            if bone.bm_external_armature == "":
                continue
            arm_child = armature.name
            parent_empty = bone.bm_parent_empty
            child_empty = bone.bm_child_empty
            arm_parent = bone.bm_external_armature
            bone_parent = bone.bm_external_parent

            bm_chk_dict[bone.name] = ['BONE', arm_child, parent_empty, child_empty, arm_parent, bone_parent]

    return bm_chk_dict

def b_m_parent_rel_remove(bone_parent, bone_child,  arm_parent, arm_child_str):
    arm_child = bpy.data.objects[arm_child_str]
    if bone_child != "":
        bm_parent_empty = arm_child.data.bones[bone_child].bm_parent_empty
        bm_child_empty = arm_child.data.bones[bone_child].bm_child_empty
    else:
        if 'bm_parent_empty' in arm_child.keys():
            bm_parent_empty = arm_child['bm_parent_empty']
        else:
            bm_parent_empty = ""

        if 'bm_child_empty' in arm_child.keys():
            bm_child_empty = arm_child['bm_child_empty']
        else:
            bm_child_empty = ""

    bpy.data.objects.remove(bpy.data.objects[bm_parent_empty])
    bpy.data.objects.remove(bpy.data.objects[bm_child_empty])

    if bone_child != "":
        const2 = next((const for const in arm_child.pose.bones[bone_child].constraints if const.name == 'bm_const2'), None)
        arm_child.pose.bones[bone_child].constraints.remove(const2)
    else:
        const2 = next((const for const in arm_child.constraints if const.name == 'bm_const2'), None)
        arm_child.constraints.remove(const2)

    if bone_child != "":
        arm_child.data.bones[bone_child].bm_external_armature = ""
        arm_child.data.bones[bone_child].bm_external_parent = ""
        arm_child.data.bones[bone_child].bm_child_empty = ""
        arm_child.data.bones[bone_child].bm_parent_empty = ""
    else:
        del arm_child["bm_external_armature"]
        del arm_child["bm_child_empty"]
        del arm_child["bm_parent_empty"] 
        if bone_parent != "":
            del arm_child["bm_external_parent"]
        else:
            if 'bm_external_parent' in arm_child.keys():
                del arm_child["bm_external_parent"]
    return


def b_m_auto_recognize_parenting():
    # THIS IS THE OUTPUT DICTIONARY STRUCTURE
    # { name: [
    #0 arm_child 
    #1 child_empty
    #2 parent_empty
    #3 arm_parent
    #4 bone_parent
    # ]  }
    found_relations = {}

    # try to see if a bone is child 
    empties = [empty for empty in bpy.data.objects if empty.data == None]
    for armature in [arm for arm in bpy.context.scene.objects if arm.data in bpy.data.armatures.values()]:
        for pbone in armature.pose.bones:
            
            if armature.data.bones[pbone.name].bm_external_armature != "":
                continue

            empty_target_consts = []
            for const in pbone.constraints:
                try:
                    if const.target in empties:
                        empty_target_consts.append(const)
                except AttributeError:
                    continue
            
            for const in empty_target_consts:
                if const.target.parent in empties:
                    for parentconst in  const.target.parent.constraints:
                        try:
                            if parentconst.target:
                                found_relations[pbone.name] = [armature.name, const.target.name, const.target.parent.name, parentconst.target.name, parentconst.subtarget]
                                
                                const.name = "bm_const2"
                                parentconst.name = "bm_const1"
                        except AttributeError:
                            continue
    
    #set the found relations
    
    for child in found_relations.keys():
        bone = bpy.data.objects[found_relations[child][0]].data.bones[child]
        bone.bm_external_armature = found_relations[child][3]
        bone.bm_external_parent = found_relations[child][4]
        bone.bm_parent_empty = found_relations[child][2]
        bone.bm_child_empty = found_relations[child][1]

    #TODO: try to see if a object is a child

    return found_relations
