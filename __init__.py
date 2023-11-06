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
    "name": "Bone Merger",
    "author": "Betti",
    "version": (2, 6),
    "blender": (2, 80, 0),
    "location": "View3D > Bone Merger",
    "description": """!!! DO NOT HESITATE TO REPORT ANY BUGS !!! Especially if the bug slows you down in the production. Use the button below""",
    "warning": "",
    "doc_url": "https://github.com/Betti83771/BlenderBoneMerger",
    "tracker_url": "https://github.com/Betti83771/BlenderBoneMerger/issues",
    "category": "Rigging",
}


import bpy
from importlib import reload

from . import b_m_ui
from . import bone_merger
from . import bm_properties
from . import constr_influence_ui
from . import addon_updater_ops
from . import addon_updater

reload(bone_merger)
reload(b_m_ui)
reload(bm_properties)
reload(constr_influence_ui)
reload(addon_updater_ops)
reload(addon_updater)


from .bone_merger import *
from .b_m_ui import *
from .bm_properties import *

@addon_updater_ops.make_annotations
class UpdaterPreferences(bpy.types.AddonPreferences):
	"""Addon updater preferences"""
	bl_idname = __package__

	auto_check_update = bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False)

	updater_interval_months = bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)

	updater_interval_days = bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)

	updater_interval_hours = bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)

	updater_interval_minutes = bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)

	def draw(self, context):
		layout = self.layout

		# Works best if a column, or even just self.layout.
		mainrow = layout.row()
		col = mainrow.column()

		# Updater draw function, could also pass in col as third arg.
		addon_updater_ops.update_settings_ui(self, context)


def register():
    addon_updater_ops.register(bl_info)
    properties_register()
    bpy.utils.register_class(BoneMergerOperator)
    bm_ui_register()
    


def unregister():
    bm_ui_unregister()
    bpy.utils.unregister_class(BoneMergerOperator)
    properties_unregister()
    addon_updater_ops.unregister(bl_info)

if __name__ == "__main__":
    register()