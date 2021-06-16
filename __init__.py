bl_info = {
    "name": "Bone Merger Package",
    "author": "Betti",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Bone Merger",
    "description": """Creates a chain of parenting between two bones, placing two intermediary empties""",
    "warning": "",
    "doc_url": "",
    "category": "Rigging",
}


import bpy
from .b_m_ui import *
from .bone_merger import *

def register():
    properties_register()
    bpy.utils.register_class(BoneMergerOperator)
    bpy.utils.register_class(BoneMergerPanel)


def unregister():
    bpy.utils.unregister_class(BoneMergerPanel)
    bpy.utils.unregister_class(BoneMergerOperator)
    properties_unregister()

if __name__ == "__main__":
    register()