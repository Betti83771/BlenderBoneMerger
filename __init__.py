bl_info = {
    "name": "Bone Merger Package",
    "author": "Betti",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Bone Merger",
    "description": """Creates a chain of parenting between two bones, placing two intermediary empties""",
    "warning": "",
    "doc_url": "",
    "category": "Rigging",
}


import bpy
from importlib import reload

from . import b_m_ui
from . import bone_merger

reload(bone_merger)
reload(b_m_ui)


from .bone_merger import *
from .b_m_ui import *


def register():
    properties_register()
    bpy.utils.register_class(BoneMergerOperator)
    bpy.utils.register_class(BoneMergerPanel)
    bpy.utils.register_class(BMParentingLink)
    bpy.utils.register_class(BMManageParenting)


def unregister():
    bpy.utils.unregister_class(BMParentingLink)
    bpy.utils.unregister_class(BMManageParenting)
    bpy.utils.unregister_class(BoneMergerPanel)
    bpy.utils.unregister_class(BoneMergerOperator)
    properties_unregister()

if __name__ == "__main__":
    register()