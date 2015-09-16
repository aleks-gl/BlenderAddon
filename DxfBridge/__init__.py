# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
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
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import os
import codecs
import math
from math import sin, cos, radians
import bpy
from mathutils import Vector, Matrix

from .importer import DxfImportProcessor

bl_info = {
    "name": "Dxf Bridge - v0.1",
    "author": "Aleks Galdin",
    "version": (0, 0, 1),
    "blender": (2, 71, 0),
    "location": "File > Import > DXF Import file - 0.1",
    "description": "Import Autocad Dxf file into scene",
    "warning": "Development version",
    "wiki_url": "http://wiki.blender.org",
    "category": "Import-Export",
}

__version__ = '.'.join([str(s) for s in bl_info['version']])
    
   
def menu_func(self, context):
    self.layout.operator(DxfImportProcessor.bl_idname, text="Import Autocad (.dxf)")   

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_func)

 
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_func)


if __name__ == "__main__":
    register()
