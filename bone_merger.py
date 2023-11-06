import bpy
from mathutils import Vector
from .constr_influence_ui import *

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
        if context.window_manager.bm_target_child.data in bpy.data.armatures.values():
            subtarget = context.window_manager.bm_target_child.data.bones[context.window_manager.bm_subtarget_child]
            if context.window_manager.bm_relation_mode_ui == "overwrite":
                relation_slot = context.window_manager.bm_relation_slot_ui
            else:
                relation_slot = len(subtarget.bm_relations)
        else:
            subtarget = context.window_manager.bm_target_child
            if context.window_manager.bm_relation_mode_ui == "overwrite":
                relation_slot = context.window_manager.bm_relation_slot_ui
            else:
                props = [prop for prop in subtarget.keys() if prop.startswith("bm_external_parent_")]
                if props != []:
                    relation_slot = len(props)
                else:
                    relation_slot = 0

        b_m_func(context,
            context.window_manager.bm_subtarget_parent, 
            context.window_manager.bm_subtarget_child, 
            context.window_manager.bm_target_parent, 
            context.window_manager.bm_target_child, 
            relation_slot,
            context.window_manager.bm_empty_collection,
            use_snap=context.window_manager.bm_use_snap, 
            hide_empties=context.window_manager.bm_hide_empties)

        return {'FINISHED'}

def snap_objs(to_snap, target):
    to_snap.matrix_world =  target.matrix_world

def b_m_func(context, bone_parent, bone_child,  arm_parent, arm_child, rel_i, empties_coll, use_snap=False, hide_empties=True):
    
    
    if arm_child.type == 'ARMATURE' and bone_child != "":
        bone_child_present = True
    else:
        bone_child_present = False

    if not empties_coll:
        empties_coll = bpy.data.collections.new("bm_empties")
        context.scene.collection.children.link(empties_coll)
        context.window_manager.bm_empty_collection = empties_coll

    if bone_child_present:
        relation = next((rel for rel in arm_child.data.bones[bone_child].bm_relations if rel.bm_relation_slot == rel_i), None)
   
        if not relation:
            relation = arm_child.data.bones[bone_child].bm_relations.add()
            relation.bm_relation_slot = rel_i
    name_suffix = (str(rel_i).zfill(2))
    if bone_child_present:
        bm_parent_empty = relation.bm_parent_empty
        bm_child_empty = relation.bm_child_empty
    else:
        if 'bm_parent_empty_' + name_suffix in arm_child.keys():
            bm_parent_empty = arm_child['bm_parent_empty_' + name_suffix]
        else:
            bm_parent_empty = ""

        if 'bm_child_empty_' + name_suffix in arm_child.keys():
            bm_child_empty = arm_child['bm_child_empty_' + name_suffix]
        else:
            bm_child_empty = ""
        
    #check for empties or create the new ones
    if bm_parent_empty != "" and bm_parent_empty in bpy.data.objects.keys():
        empty1 = bpy.data.objects[bm_parent_empty]
        
    else:
       
        if bone_parent != "":
            size = arm_parent.data.bones[bone_parent].length * 1.2
        else:
            if arm_parent.dimensions.z == 0.0:
                size = 0.5
                
            else:
                size = arm_parent.dimensions.z * 0.85


        empty1 = bpy.data.objects.new(arm_parent.name + "_" + bone_parent, None)
        empty1.empty_display_type = 'CUBE'
        empty1.empty_display_size = size
        empties_coll.objects.link(empty1)
        if bone_parent != "":
            matrix_1 = arm_parent.pose.bones[bone_parent].matrix.copy()
            empty1.matrix_world = arm_parent.matrix_world @ matrix_1
        else:
            empty1.matrix_world = arm_parent.matrix_world

    if bm_child_empty != "" and bm_child_empty in bpy.data.objects.keys():
        empty2 = bpy.data.objects[bm_child_empty]
    else:
        if bone_child_present:
            size = arm_child.data.bones[bone_child].length * 1.2
        else:
            if arm_child.dimensions.z == 0.0:
                size = 0.5
                
            else:
                size = arm_child.dimensions.z * 0.85
        empty2 = bpy.data.objects.new(arm_child.name + "_" + bone_child, None )
        empty2.empty_display_type = 'SPHERE'
        empty2.empty_display_size = size
        empties_coll.objects.link(empty2)
        if bone_child_present:
            matrix_2 = arm_child.pose.bones[bone_child].matrix.copy()
            empty2.matrix_world = arm_child.matrix_world @ matrix_2
        else:
            empty2.matrix_world = arm_child.matrix_world

    #snap the second empty on the first
    if use_snap:
        snap_objs(empty2, empty1) 

    #hide the empties
    if hide_empties:
        empty1.hide_viewport = True
        empty2.hide_viewport = True

    #make the constraints
    const1 = next((const for const in empty1.constraints if const.name == 'bm_const1_{0}'.format(str(rel_i).zfill(2))), None)
    if bone_child_present:
        const2 = next((const for const in arm_child.pose.bones[bone_child].constraints if const.name == 'bm_const2_{0}'.format(str(rel_i).zfill(2))), None)
    else:
        const2 = next((const for const in arm_child.constraints if const.name == 'bm_const2_{0}'.format(str(rel_i).zfill(2))), None)
    if not const1:
        const1 = empty1.constraints.new(type='COPY_TRANSFORMS')
        const1.name = 'bm_const1_{0}'.format(str(rel_i).zfill(2))
    const1.target = arm_parent
    const1.subtarget = bone_parent
    if not const2:
        if bone_child_present:
            const2 = arm_child.pose.bones[bone_child].constraints.new(type='COPY_TRANSFORMS')
        else:
            const2 = arm_child.constraints.new(type='COPY_TRANSFORMS')
        const2.name = 'bm_const2_{0}'.format(str(rel_i).zfill(2))
    const2.target = empty2
    

    #parent the empties
    empty2_mat_bk = empty2.matrix_world.copy()
    empty2.parent = empty1
    empty2.matrix_world = empty2_mat_bk

    #set the external parent and empty properties
   
    if bone_child_present:
        relation.bm_external_armature = arm_parent.name
        if bone_parent != "":
            relation.bm_external_parent = bone_parent
        else:
            relation.bm_external_parent = ""
        relation.bm_child_empty = empty2.name
        relation.bm_parent_empty = empty1.name
    else:
        arm_child["bm_external_armature_" + name_suffix] = arm_parent.name
        arm_child["bm_child_empty_" + name_suffix] = empty2.name
        arm_child["bm_parent_empty_" + name_suffix] = empty1.name
        if bone_parent != "":
            arm_child["bm_external_parent_" + name_suffix] = bone_parent
        else:
            if 'bm_external_parent' in arm_child.keys():
                del arm_child["bm_external_parent_" + name_suffix]
            
    run_constr_infl_ui_script()
    return

def b_m_checker():
    """Checks all the bone merger parenting relations in the scene. Returns dictionary -  child name: relationship details (5 props + bone_or_obj)"""
    bm_chk_dict = {}
    # THIS IS THE OUTPUT DICTIONARY STRUCTURE
    # { (name, rel_i): [
    #0 bone_or_obj
    #1 arm_child 
    #2 parent_empty
    #3 child_empty
    #4 arm_parent
    #5 bone_parent
    # ]  }
    for obj in bpy.context.scene.objects:
        bm_prop = next((prop for prop in obj.keys() if prop.startswith("bm_external_armature")), None) 
        if not bm_prop:
            continue
        print(obj) #check if it's not processing all objects but only useful ones
        for rel_i in range(0, 11):
            name_suffix = (str(rel_i).zfill(2))
            parent_empty = ""
            child_empty = ""
            arm_parent = ""
            bone_parent = ""
            if 'bm_external_armature_' + name_suffix in obj.keys():
                arm_parent = obj['bm_external_armature_' + name_suffix]
            else:
                continue
            if 'bm_parent_empty_' + name_suffix in obj.keys():
                parent_empty = obj['bm_parent_empty_' + name_suffix]
            if 'bm_child_empty_' + name_suffix in obj.keys():
                child_empty = obj['bm_child_empty_' + name_suffix]
            if 'bm_external_parent_' + name_suffix in obj.keys():
                bone_parent = obj['bm_external_parent_' + name_suffix]
            
            bm_chk_dict[(obj.name, rel_i)] = ['OBJ', "", parent_empty, child_empty, arm_parent, bone_parent]
    
    for armature in [arm for arm in bpy.context.scene.objects if arm.data in bpy.data.armatures.values()]:
        for bone in armature.data.bones:
            if  len(bone.bm_relations) < 1:
                continue
            for rel in bone.bm_relations:
                arm_child = armature.name
                parent_empty = rel.bm_parent_empty
                child_empty = rel.bm_child_empty
                arm_parent = rel.bm_external_armature
                bone_parent = rel.bm_external_parent
                rel_i = rel.bm_relation_slot

                bm_chk_dict[(bone.name, rel_i)] = ['BONE', arm_child, parent_empty, child_empty, arm_parent, bone_parent]

    return bm_chk_dict

def b_m_parent_rel_remove(bone_parent, bone_child,  arm_parent_str, arm_child_str, rel_i): 
    arm_child = bpy.data.objects[arm_child_str]
    name_suffix = (str(rel_i).zfill(2))

    if bone_child != "":
        relation = next((rel for rel in arm_child.data.bones[bone_child].bm_relations if rel.bm_relation_slot == rel_i), None)
        bm_parent_empty = relation.bm_parent_empty
        bm_child_empty = relation.bm_child_empty
    else:  
        if 'bm_parent_empty_' + name_suffix in arm_child.keys():
            bm_parent_empty = arm_child['bm_parent_empty_' + name_suffix]
        else:
            bm_parent_empty = ""

        if 'bm_child_empty_' + name_suffix in arm_child.keys():
            bm_child_empty = arm_child['bm_child_empty_' + name_suffix]
        else:
            bm_child_empty = ""
    if bm_parent_empty in bpy.data.objects.keys():
        bpy.data.objects.remove(bpy.data.objects[bm_parent_empty])
    if bm_child_empty in bpy.data.objects.keys():
        bpy.data.objects.remove(bpy.data.objects[bm_child_empty])
    
    
    if bone_child != "":
        const2 = next((const for const in arm_child.pose.bones[bone_child].constraints if const.name == 'bm_const2_' + name_suffix), None)
        if const2:
            arm_child.pose.bones[bone_child].constraints.remove(const2)
    else:
        const2 = next((const for const in arm_child.constraints if const.name == 'bm_const2_' + name_suffix), None)
        if const2:
            arm_child.constraints.remove(const2)

    if bone_child != "":
        index = arm_child.data.bones[bone_child].bm_relations.find(relation.name)
        arm_child.data.bones[bone_child].bm_relations.remove(index)
    
    else:
        del arm_child["bm_external_armature_" + name_suffix]
        del arm_child["bm_child_empty_" + name_suffix]
        del arm_child["bm_parent_empty_" + name_suffix] 
        if bone_parent != "":
            del arm_child["bm_external_parent_" + name_suffix]
        else:
            if 'bm_external_parent_' + name_suffix in arm_child.keys():
                del arm_child["bm_external_parent_" + name_suffix]
    return


def b_m_auto_recognize_parenting():
    # THIS IS THE OUTPUT DICTIONARY STRUCTURE
    # { (name, rel_i): [
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
            if len(armature.data.bones[pbone.name].bm_relations) > 1:
                continue

            empty_target_consts = []
            for const in pbone.constraints:
                try:
                    if const.target in empties:
                        empty_target_consts.append(const)
                except AttributeError:
                    continue
            rel_i = 0
            for const in empty_target_consts:
                if const.target.parent in empties:
                    print(const)
                    for parentconst in  const.target.parent.constraints:
                        try:
                            if parentconst.target:
                                found_relations[(pbone.name, rel_i)] = [armature.name, const.target.name, const.target.parent.name, parentconst.target.name, parentconst.subtarget]
                                
                                const.name = 'bm_const2_{0}'.format(str(rel_i).zfill(2))
                                parentconst.name = 'bm_const1_{0}'.format(str(rel_i).zfill(2))
                                rel_i += 1
                        except AttributeError:
                            continue
    
    #set the found relations
    print("found_relations", found_relations)
    
    for child_tup in found_relations.keys():
        child = child_tup[0]
        bone = bpy.data.objects[found_relations[child_tup][0]].data.bones[child]
        relation = next((rel for rel in bone.bm_relations if rel.bm_relation_slot == child_tup[1]), None)
        if not relation:
            relation = bone.bm_relations.add()
            relation.bm_relation_slot = child_tup[1]

        relation.bm_external_armature = found_relations[child_tup][3]
        relation.bm_external_parent = found_relations[child_tup][4]
        relation.bm_parent_empty = found_relations[child_tup][2]
        relation.bm_child_empty = found_relations[child_tup][1]

    #TODO: try to see if a object is a child

    return found_relations

def b_m_manual_register_relations(bone_parent, bone_child,  arm_parent, arm_child, empty_parent_str, empty_child_str, rel_i):
    if empty_child_str not in bpy.data.objects.keys():
        return 'NO_CHILD_EMPTY'
    
    if empty_parent_str not in bpy.data.objects.keys():
        return 'NO_PARENT_EMPTY'
    
    name_suffix = (str(rel_i).zfill(2))

    if bone_child != "":
        bone = bpy.data.objects[arm_child].data.bones[bone_child]
        relation = next((rel for rel in bone.bm_relations if rel.bm_relation_slot == rel_i), None)
        if not relation:
            relation = bone.bm_relations.add()
            relation.bm_relation_slot = rel_i
        else:
            return 'REL_SLOT_FULL'

    # find constraints
    const1_found = False
    const2_found = False
    if bone_child != "":
        constraints = arm_child.pose.bones[bone_child].constraints
    else:
        constraints = arm_child.constraints
    for const in constraints:
        try:
            if const.target == bpy.data.objects[empty_child_str]:
                const.name = 'bm_const2_{0}'.format(name_suffix)
                const1_found = True
        except AttributeError:
            continue
    
    for const in bpy.data.objects[empty_parent_str].constraints:
        try:
            if const.target == arm_parent:
                const.name = 'bm_const1_{0}'.format(name_suffix)
                const2_found = True
        except AttributeError:
            continue

    if not const1_found:
        return 'NO_CHILD_CONST'
    
    if not const2_found:
        return 'NO_PARENT_CONST'
    if bone_child != "":
        relation.bm_external_parent = bone_parent
        relation.bm_external_armature = arm_parent.name
        relation.bm_child_empty = empty_child_str
        relation.bm_parent_empty = empty_parent_str
    else:
        arm_child["bm_external_armature_" + name_suffix] = arm_parent.name
        arm_child["bm_child_empty_" + name_suffix] = empty_child_str
        arm_child["bm_parent_empty_" + name_suffix] = empty_parent_str
        if bone_parent != "":
            arm_child["bm_external_parent_" + name_suffix] = bone_parent
        else:
            if 'bm_external_parent' in arm_child.keys():
                del arm_child["bm_external_parent_" + name_suffix]

    return 'SUCCESS'


def run_constr_infl_ui_script():
    if "constraint_influence_ui.py" in bpy.data.texts:
        if  bpy.data.texts["constraint_influence_ui.py"].use_module:
            return
    script_create_and_register()
    script = bpy.data.texts["constraint_influence_ui.py"]

    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'TEXT_EDITOR':
                area.spaces[0].text = script 

                context = bpy.context.copy()
                context['edit_text'] = script 
                context['area'] = area
                context['region'] = area.regions[-1]
                bpy.ops.text.run_script(context)
                break