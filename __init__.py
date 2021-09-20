# ====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, version 3.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ======================= END GPL LICENSE BLOCK ========================


bl_info = {
    "name": "Bone Merger Package",
    "author": "Betti",
    "version": (2, 3),
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
from . import bm_properties

reload(bone_merger)
reload(b_m_ui)
reload(bm_properties)


from .bone_merger import *
from .b_m_ui import *
from .bm_properties import *

def register():
    properties_register()
    bpy.utils.register_class(BoneMergerOperator)
    bm_ui_register()


def unregister():
    bm_ui_unregister()
    bpy.utils.unregister_class(BoneMergerOperator)
    properties_unregister()

if __name__ == "__main__":
    register()