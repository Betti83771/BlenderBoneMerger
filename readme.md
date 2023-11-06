# The Bone Merger Addon for Blender

The Bone Merger for Blender is an useful addon for all the animators who are tired of props that don't follow their characters, of not being able to animate people people picking up things smoothly, and of objects that cannot change parent.

Sure enough, this addon allows to dynamically contruct relations between bones of different rigs; it makes use of a chain of parented and constrained empties (shown in detial in the image below).

One object or bone (child) can have multiple parents; the "Parent Switch" panel allows the user to switch parents on the fly, just by putting a keyframe on the right constraint influences; switching parent is one keyframe away and it can also be esaed, animated and mixed since it's a gradual influence going from 0 to 1.

Once you get used to the Bone Merger for Blender workflow it will be impossible to animate without it!



## The Bone Merger Panel
This panel gives access to the main operator of the addon, "Parent and Constraint", and its options;
as well as access to the "Manage Relations" panel.
Here is a descriptions of all the features of this panel:

**Parent**: The parent object of this relation. If it's an armature, a bone field will appear.
**Parent bone**: the bone of the parent armature which will be the parent in this relation.
**Child**: The child object of this relation. If it's an armature, a bone field will appear.
In case of specification of a bone, only the bone will follow the parent; 
if a bone is not specified, the whole child object will follow the parent object or bone.
**Child bone**: the bone of the parent armature which will be the parent in this relation.

**New**: a new relation will be registered, granted that the parent and child are different 
from a previously registered relation.

**Overwrite**: this option allows the user to quickly change the parent of a previously
registered relation. Upon selecting it, the user can choose which parent to overwrite in case
of multiple parents registered.
Note: due to Blender limitations, the scrubbing is not limited to existing parents, so the user
may "overwrite" an empty index that shows no parent name and it will count as a new relation.
However, it is advised to occupy the next index in order and not skip any indexes.

**Snap empty on parent**: check this box to snap the child on the parent. Useful if the user isn't
seeking an offset effect.

**Hide new empties**: check this box to automatically hide the newly created empties from the viewport.

**Empties collection**: select the collection where the empties will be linked. If no collection is
specified, a new collection by the name of "bm_empties" will be created in the scene main collection and used.

**Parent and Constraint**: click this button to create a new relation with the parameters specified above.

Warning:
- If you change the name of the empties or the bones after the relation is registrerd, you have to update them by clicking on "manage relations", typing the new namesw in the respective fields, then clicking "update".

**Manage Relations**: click to access the Manage Relations panel. See below.


## The "Manage Relations" panel

This panel allows the user to update relation informations, such as change a parent or an empty, or delete relations altogether.

**Update**
Note: the child can't be changed since the data of the relation is stored on the child.
To change the child, please make a new relation and remove the previous one.

**Remove**
Deletes this relation from the list; deletes the empties; removes the constraints. Does not remove any keys of animation.

**Manually register new relation**
Prompts empty fields to register an existing relation manually if it's not appearing in the list and can't be detected by "Try auto recognize parenting".

**Try auto recognize parenting**
This option may be used if one or more relations previously made with the addon have lost their parenting info and aren't shown in the Manage Relations panel.
This option may also be used if the parenting with the empties has been done by hand, using the same method as the addon: this allows these kind of relations to be managed, changed or removed by the Bone Merger.

Why "try"? Because it is not guaranteed to succeed, given the number of variables involved in the process and how humans may have not followed it precisely, as well as changes between different versions of the addon.

## The "Bone Merger: Parent Switch" panel

This panel is only visible in pose mode of the child rig. It is currently only available if the child is a bone and not an object.
This panel shows the influence of the Copy Transforms constraint on the bone, so that they can be animated and the relation can be switched or toggled on and off altogether.
By pressing  "I" on the influences a key will be put in place. Th epurpose of the panel is to quickly animate the influences while animating the rest of the character.

**Show all**: if off, only shows the influences of the active bone. If on, shows all influences of all relations in the rig.


## Technical notes and info
The relations info is stored on the child bone or on the child object if no bone is specified as a custom porperty.

This addon was used in many production of MAD Entertainment studio, such as Food wizards and Due Battiti.





## LICENSE
 ====================== BEGIN GPL LICENSE BLOCK ======================

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation, version 3.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software Foundation,
  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

 ======================= END GPL LICENSE BLOCK ========================

## CREDITS
Addon coded by Betti Abbattista https://github.com/Betti83771

Addon updater: https://github.com/CGCookie/blender-addon-updater

Base idea: Corrado Piscitelli https://github.com/GigiSpligi

Name idea: Gmod addon https://steamcommunity.com/sharedfiles/filedetails/?id=104601200


