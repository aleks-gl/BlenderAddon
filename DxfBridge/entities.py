import os
import codecs
import math
from math import sin, cos, radians
import bpy
from bpy.props import StringProperty, EnumProperty, BoolProperty, FloatProperty, IntProperty
from mathutils import Vector, Matrix
#
#    class CSection:
#

class CSection:
    type = None

    def __init__(self):
        self.data = []

    def display(self):
        print("Section", self.type)
        for datum in self.data:
            datum.display()

#
#    class CTable:
#

class CTable:
    def __init__(self):
        self.type = None
        self.name = None
        self.handle = None
        self.owner = None
        self.subclass = None
        self.nEntries = 0
    def display(self):
        print("Table %s %s %s %s %s %d" % (self.type, self.name, self.handle, self.owner, self.subclass, self.nEntries))

#
#    class CEntity:
#
class CEntity:
    def __init__(self, typ, drawtype):
        self.type = typ
        self.drawtype = drawtype
        self.handle = None
        self.owner = None
        self.subclass = None
        self.layer = 0
        self.color = 0
        self.invisible = 0
        self.linetype_name = ''
        self.linetype_scale = 1.0
        self.paperspace = 0
        #self.normal = Vector((0,0,1))

    def display(self):
        print("Entity %s %s %s %s %s %s %x" % 
            (self.type, self.handle, self.owner, self.subclass, self.layer, self.color, self.invisible))

    def build(self, vn=0):
        global toggle
        if toggle & T_Debug:
            raise NameError("Warning: can not build - unsupported entity type: %s" % self.type)
        return(([], [], [], vn)) 

    def draw(self):
        global toggle
        if toggle & T_Debug:
            raise NameError("Warning: can not draw - unsupported entity type: %s" % self.type)
        return




#
#    class C3dFace(CEntity):
#    10 : 'point0.x', 20 : 'point0.y', 30 : 'point0.z', 
#    11 : 'point1.x', 21 : 'point1.y', 31 : 'point1.z', 
#    12 : 'point2.x', 22 : 'point2.y', 32 : 'point2.z', 
#    13 : 'point3.x', 23 : 'point3.y', 33 : 'point3.z', 
#    70 : 'flags',
#

class C3dFace(CEntity):
    def __init__(self):
        CEntity.__init__(self, '3DFACE', 'Mesh')
        self.point0 = Vector()
        self.point1 = Vector()
        self.point2 = Vector()
        self.point3 = Vector()

    def display(self):
        CEntity.display(self)
        print(self.point0)
        print(self.point1)
        print(self.point2)
        print(self.point3)

    def build(self, vn=0):
        verts = [self.point0, self.point1, self.point2]
        if self.point3 == Vector((0,0,0)) or self.point2 == self.point3:
            faces = [(vn+0, vn+1, vn+2)]
            vn += 3
        else:
            verts.append( self.point3 )
            faces = [(vn+0, vn+1, vn+2, vn+3)]
            vn += 4            
        return((verts, [], faces, vn))

#
#    class C3dSolid(CEntity):
#    1 : 'data', 3 : 'more', 70 : 'version',
#

class C3dSolid(CEntity):
    def __init__(self):
        CEntity.__init__(self, '3DSOLID', 'Mesh')
        self.data = None
        self.more = None
        self.version = 0

#
#    class CAcadProxyEntity(CEntity):
#    70 : 'format',
#    90 : 'id', 91 : 'class', 92 : 'graphics_size', 93 : 'entity_size', 95: 'format',
#    310 : 'data', 330 : 'id1', 340 : 'id2', 350 : 'id3', 360 : 'id4', 
#

class CAcadProxyEntity(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'ACAD_PROXY_ENTITY', None)


#
#    class CArc(CEntity):
#    10 : 'center.x', 20 : 'center.y', 30 : 'center.z', 
#    40 : 'radius',
#    50 : 'start_angle', 51 : 'end_angle'
#

class CArc(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'ARC', 'Mesh')
        self.center = Vector()
        self.radius = 0.0
        self.start_angle = 0.0
        self.end_angle = 0.0
        self.thickness = 0.0
        self.normal = Vector((0,0,1))
        
    def display(self):
        CEntity.display(self)
        print(self.center)
        print("%.4f %.4f %.4f " % (self.radius, self.start_angle, self.end_angle))

    def build(self, vn=0):
        start, end = self.start_angle, self.end_angle
        if end > 360: end = end % 360.0
        if end < start: end +=360.0
        # angle = end - start  # UNUSED

        deg2rad = math.pi/180.0
        start *= deg2rad
        end *= deg2rad
        dphi = end - start
        phi0 = start
        w = dphi/theCircleRes
        r = self.radius
        center = self.center
        v0 = vn
        points = []
        edges, faces = [], []
        for n in range(theCircleRes + 1):
            s = math.sin(n*w + phi0)
            c = math.cos(n*w + phi0)
            v = center + Vector((r*c, r*s, 0.0))
            points.append(v)
        pn = len(points)
        thic = self.thickness
        t_vector = Vector((0, 0, thic))
        if thic != 0 and (toggle & T_ThicON):
            thic_points = [v + t_vector for v in points]
            if thic < 0.0:
                thic_points.extend(points)
                points = thic_points
            else:
                points.extend(thic_points)
            faces = [(v0+nr+0,v0+nr+1,v0+pn+nr+1,v0+pn+nr+0) for nr in range(pn)]
            faces.pop()
            self.drawtype = 'Mesh'
            vn += 2*pn
        else:
            edges = [(v0+nr+0,v0+nr+1) for nr in range(pn)]
            edges.pop()
            vn += pn

        if self.normal!=Vector((0,0,1)):
            ma = getOCS(self.normal)
            if ma:
                #ma.invert()
                points = [ma * v for v in points]
        #print ('arc vn=', vn)
        #print ('faces=', len(faces))
        return ((points, edges, faces, vn))

#
#    class CArcAlignedText(CEntity):
#    1 : 'text', 2 : 'font', 3 : 'bigfont', 7 : 'style',
#    10 : 'center.x', 20 : 'center.y', 30 : 'center.z', 
#    40 : 'radius', 41 : 'width', 42 : 'height', 43 : 'spacing', 
#    44 : 'offset', 45 : 'right_offset', 46 : 'left_offset', 
#    50 : 'start_angle', 51 : 'end_angle',
#    70 : 'order', 71 : 'direction', 72 : 'alignment', 73 : 'side', 
#    74 : 'bold', 75 : 'italic', 76 : 'underline',
#    77 : 'character_set', 78 : 'pitch', 79 'fonttype',
#    90 : 'color',
#    280 : 'wizard', 330 : 'id'
#

class CArcAlignedText(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'ARCALIGNEDTEXT', 'Mesh')
        self.text = ""
        self.style = ""
        self.center = Vector()
        self.radius = 0.0
        self.width = 1.0
        self.height = 1.0
        self.spacing = 1.0
        self.offset = 0.0
        self.right_offset = 0.0
        self.left_offset = 0.0
        self.start_angle = 0.0
        self.end_angle = 0.0
        self.order = 0
        self.directions = 0
        self.alignment = 0
        self.side = 0
        self.bold = 0
        self.italic = 0
        self.underline = 0
        self.character_set = 0
        self.pitch = 0
        self.fonttype = 0
        self.color = 0
        self.wizard = None
        self.id = None
        self.normal = Vector((0,0,1))


#
#    class CAttdef(CEntity):
#    1 : 'text', 2 : 'tag', 3 : 'prompt', 7 : 'style',
#    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
#    11 : 'alignment_point.x', 21 : 'alignment_point.y', 31 : 'alignment_point.z', 
#    40 : 'height', 41 : 'x_scale', 
#    50 : 'rotation_angle', 51 : 'oblique_angle', 
#    70 : 'flags', 71 : 'text_generation_flags', 
#    72 : 'horizontal_justification',  74 : 'vertical_justification',    
#

class CAttdef(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'ATTDEF', None)
        self.value = ""
        self.tag = ""
        self.prompt = ""
        self.style = ""
        self.insertion_point = Vector()
        self.alignment_point = Vector()
        self.height = 1.0
        self.x_scale = 1.0
        self.rotation_angle = 0.0
        self.oblique_angle = 0.0
        self.flags = 0
        self.text_generation_flags = 0
        self.horizontal_justification = 0.0
        self.vertical_justification = 0.0
        self.normal = Vector((0,0,1))

    def draw(self):
        drawText(self.text,  self.insertion_point, self.height, self.x_scale, self.rotation_angle, self.oblique_angle, self.normal)
        return

#
#    class CAttrib(CEntity):
#    1 : 'text', 2 : 'tag', 3 : 'prompt', 7 : 'style',
#    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
#    11 : 'alignment_point.x', 21 : 'alignment_point.y', 31 : 'alignment_point.z', 
#    40 : 'height', 41 : 'x_scale', 
#    50 : 'rotation_angle', 51 : 'oblique_angle', 
#    70 : 'flags', 73 : 'length', 
#    71 : 'text_generation_flags', 72 : 'horizontal_justification',  74 : 'vertical_justification',     
#

class CAttrib(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'ATTRIB', None)
        self.text = ""
        self.tag = ""
        self.prompt = ""

        self.style = ""
        self.insertion_point = Vector()
        self.alignment_point = Vector()
        self.height = 1.0
        self.x_scale = 1.0
        self.rotation_angle = 0.0
        self.oblique_angle = 0.0
        self.flags = 0
        self.length = 1.0
        self.text_generation_flags = 0
        self.horizontal_justification = 0.0
        self.vertical_justification = 0.0
        self.normal = Vector((0,0,1))

    def draw(self):
        drawText(self.text,  self.insertion_point, self.height, self.x_scale, self.rotation_angle, self.oblique_angle, self.normal)
        return


#
#    class CBlock(CEntity):
#    1 : 'xref', 2 : 'name', 3 : 'also_name', 
#    10 : 'base_point.x', 20 : 'base_point.y', 30 : 'base_point.z', 
#    40 : 'size', 41 : 'x_scale', 
#    50 : 'rotation_angle', 51 : 'oblique_angle',     
#    70 : 'flags', 
#

class CBlock(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'BLOCK', None)
        self.xref = ""
        self.name = ""
        self.also_name = ""
        self.base_point = Vector()
        self.size = 1.0
        self.x_scale = 1.0
        self.rotation_angle = 0.0
        self.oblique_angle = 0.0
        self.flags = 0
        self.normal = Vector((0,0,1))

    def display(self):
        CEntity.display(self)
        print("%s %s %s " % (self.xref, self.name, self.also_name))
        print(self.base_point)

    def draw(self):
        # Todo
        return

#
#    class CCircle(CEntity):
#    10 : 'center.x', 20 : 'center.y', 30 : 'center.z', 
#    40 : 'radius'
#

class CCircle(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'CIRCLE', 'Mesh')
        self.center = Vector()
        self.radius = 0.0
        self.thickness = 0.0
        self.normal = Vector((0,0,1))

    def display(self):
        CEntity.display(self)
        print(self.center)
        print("%.4f" % self.radius)

    def build(self, vn=0):
        w = 2*math.pi/theCircleRes
        r = self.radius
        center = self.center
        points = []
        edges, faces = [], []
        v0 = vn
        for n in range(theCircleRes):
            s = math.sin(n*w)
            c = math.cos(n*w)
            v = center + Vector((r*c, r*s, 0))
            points.append(v)

        pn = len(points)
        thic = self.thickness
        t_vector = Vector((0, 0, thic))
        if thic != 0 and (toggle & T_ThicON):
            thic_points = [v + t_vector for v in points]
            if thic < 0.0:
                thic_points.extend(points)
                points = thic_points
            else:
                points.extend(thic_points)
            faces = [(v0+nr,v0+nr+1,pn+v0+nr+1,pn+v0+nr) for nr in range(pn)]
            nr = pn -1
            faces[-1] = (v0+nr,v0,pn+v0,pn+v0+nr)
            self.drawtype = 'Mesh'
            vn += 2*pn
        else:
            edges = [(v0+nr,v0+nr+1) for nr in range(pn)]
            nr = pn -1
            edges[-1] = (v0+nr,v0)
            vn += pn
        if self.normal!=Vector((0,0,1)):
            ma = getOCS(self.normal)
            if ma:
                #ma.invert()
                points = [ma * v for v in points]
        #print ('cir vn=', vn)
        #print ('faces=',len(faces))
        return( (points, edges, faces, vn) )
            
#
#    class CDimension(CEntity):
#    1 : 'text', 2 : 'name', 3 : 'style',
#    10 : 'def_point.x', 20 : 'def_point.y', 30 : 'def_point.z', 
#    11 : 'mid_point.x', 21 : 'mid_point.y', 31 : 'mid_point.z', 
#    12 : 'vector.x', 22 : 'vector.y', 32 : 'vector.z', 
#    13 : 'def_point2.x', 23 : 'def_point2.y', 33 : 'def_point2.z', 
#    14 : 'vector2.x', 24 : 'vector2.y', 34 : 'vector2.z', 
#    15 : 'vector3.x', 25 : 'vector3.y', 35 : 'vector3.z', 
#    16 : 'vector4.x', 26 : 'vector4.y', 36 : 'vector4.z', 
#    70 : 'dimtype',
#

class CDimension(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'DIMENSION', None)
        self.text = ""
        self.name = ""
        self.style = ""
        self.def_point = Vector()
        self.mid_point = Vector()
        self.vector = Vector()
        self.def_point2 = Vector()
        self.vector2 = Vector()
        self.vector3 = Vector()
        self.vector4 = Vector()
        self.dimtype = 0
        self.normal = Vector((0,0,1))

    def draw(self):
        return

#
#    class CEllipse(CEntity):
#    10 : 'center.x', 20 : 'center.y', 30 : 'center.z', 
#    11 : 'end_point.x', 21 : 'end_point.y', 31 : 'end_point.z', 
#    40 : 'ratio', 41 : 'start', 42 : 'end',
#

class CEllipse(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'ELLIPSE', 'Mesh')
        self.center = Vector()
        self.end_point = Vector()
        self.ratio = 1.0
        self.start = 0.0
        self.end = 2*math.pi
        self.thickness = 0.0
        self.normal = Vector((0,0,1))

    def display(self):
        CEntity.display(self)
        print(self.center)
        print("%.4f" % self.ratio)
                
    def build(self, vn=0):
        dphi = (self.end - self.start)
        phi0 = self.start
        w = dphi/theCircleRes
        r = self.end_point.length
        f = self.ratio
        a = self.end_point.x/r
        b = self.end_point.y/r
        center = self.center
        v0 = vn
        points = []
        edges, faces = [], []
        for n in range(theCircleRes):
            x = r*math.sin(n*w + phi0)
            y = f*r*math.cos(n*w + phi0)
            v = (center.x - a*x + b*y, center.y - a*y - b*x, center.z)
            points.append(v)

        pn = len(points)
        thic = self.thickness
        t_vector = Vector((0, 0, thic))
        if thic != 0 and (toggle & T_ThicON):
            thic_points = [v + t_vector for v in points]
            if thic < 0.0:
                thic_points.extend(points)
                points = thic_points
            else:
                points.extend(thic_points)
            faces = [(v0+nr,v0+nr+1,pn+v0+nr+1,pn+v0+nr) for nr in range(pn)]
            nr = pn -1
            faces[-1] = (v0+nr,v0,pn+v0,pn+v0+nr)
            #self.drawtype = 'Mesh'
            vn += 2*pn
        else:
            edges = [(v0+nr,v0+nr+1) for nr in range(pn)]
            nr = pn -1
            edges[-1] = (v0+nr,v0)
            vn += pn


        if thic != 0 and (toggle & T_ThicON):
            pass
        if self.normal!=Vector((0,0,1)):
            ma = getOCS(self.normal)
            if ma:
                #ma.invert()
                points = [ma * v for v in points]
        return ((points, edges, faces, vn))

#
#    class CHatch(CEntity):
#    2 : 'pattern',
#    10 : 'point.x', 20 : 'point.y', 30 : 'point.z', 
#    41 : 'scale', 47 : 'pixelsize', 52 : 'angle',
#    70 : 'fill', 71 : 'associativity', 75: 'style', 77 : 'double', 
#    78 : 'numlines', 91 : 'numpaths', 98 : 'numseeds',
#

class CHatch(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'HATCH', None)
        self.pattern = 0
        self.point = Vector()
        self.scale = 1.0
        self.pixelsize = 1.0
        self.angle = 0.0
        self.fill = 0
        self.associativity = 0
        self.style = 0
        self.double = 0
        self.numlines = 0
        self.numpaths = 0
        self.numseeds = 0
        self.normal = Vector((0,0,1))


#    class CImage(CEntity):
#    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
#    11 : 'u_vector.x', 21 : 'u_vector.y', 31 : 'u_vector.z', 
#    12 : 'v_vector.x', 22 : 'v_vector.y', 32 : 'v_vector.z', 
#    13 : 'size.x', 23 : 'size.y', 33 : 'size.z', 
#    14 : 'clip.x', 24 : 'clip.y', 34 : 'clip.z', 
#    70 : 'display', 71 : 'cliptype', 
#    90 : 'version',
#    280 : 'clipstate', 281 : 'brightness', 282 : 'contrast', 283 : 'fade', 
#    340 : 'image', 360 : 'reactor'
#

class CImage(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'IMAGE', None)
        self.insertion_point = Vector()
        self.u_vector = Vector()
        self.v_vector = Vector()
        self.size = Vector()
        self.clip = Vector()
        self.display = 0
        self.cliptype = 0
        self.version = 1
        self.clipstate = 0
        self.brightness = 0
        self.constrast = 0
        self.fade = 0
        self.image = None
        self.reactor = None
        self.normal = Vector((0,0,1))

#
#    class CInsert(CEntity):
#    1 : 'attributes_follow', 2 : 'name',
#    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
#    41 : 'x_scale', 42 : 'y_scale', 43 : 'z_scale', 
#    44 : 'column_spacing', 45 : 'row_spacing', 
#    50 : 'rotation_angle', 66 : 'attributes_follow',
#    70 : 'column_count', 71 : 'row_count', 
#

class CInsert(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'INSERT', None)
        self.attributes_follow = 1
        self.name = ""
        self.insertion_point = Vector()
        self.x_scale = 1.0
        self.y_scale = 1.0
        self.z_scale = 1.0
        self.column_spacing = 1.0
        self.row_spacing = 1.0
        self.rotation_angle = 0.0
        self.column_count = 1
        self.row_count = 1
        self.attributes_follow = 0
        self.normal = Vector((0,0,1))

    def display(self):
        CEntity.display(self)
        print(self.insertion_point)

    def draw(self):
        # Todo
        return

#
#    class CLeader(CEntity):
#    3 : 'style',
#    10 : ['new_vertex(data)'], 20 : 'vertex.y', 30 : 'vertex.z', 
#    40 : 'height', 41 : 'width',
#    71 : 'arrowhead', 72 : 'pathtype', 73 : 'creation', 
#    74 : 'hookdir', 75 : 'hookline', 76 : 'numverts', 77 : 'color',
#    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
#    211 : 'horizon.x', 221 : 'horizon.y', 231 : 'horizon.z', 
#    212 : 'offset_ins.x', 222 : 'offset_ins.y', 232 : 'offset_ins.z', 
#    213 : 'offset_ann.x', 223 : 'offset_ann.y', 233 : 'offset_ann.z', 
#

class CLeader(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'LEADER', 'Mesh')
        self.style = ""
        self.vertex = None
        self.verts = []
        self.height = 1.0
        self.width = 1.0
        self.arrowhead = 0
        self.pathtype = 0
        self.creation = 0
        self.hookdir = 0
        self.hookline = 0
        self.numverts = 0
        self.color = 0
        self.normal = Vector((0,0,1))
        self.horizon = Vector()
        self.offset_ins = Vector()
        self.offset_ann = Vector()

    def new_vertex(self, data):
        self.vertex = Vector()
        self.vertex.x = data
        self.verts.append(self.vertex)

    def build(self, vn=0):
        edges = []
        for v in self.verts:
            edges.append((vn, vn+1))
            vn += 1
        edges.pop()
        return (self.verts, edges, [], vn)

#    class CLwPolyLine(CEntity):
#    10 : ['new_vertex(data)'], 20 : 'vertex.y', 30 : 'vertex.z', 
#    38 : 'elevation', 39 : 'thickness',
#    40 : 'start_width', 41 : 'end_width', 42 : 'bulge', 43 : 'constant_width',
#    70 : 'flags', 90 : 'numverts'
#

class CLWPolyLine(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'LWPOLYLINE', None)
        self.vertex = None
        self.verts = []
        self.elevation = 0
        self.thickness = 0.0
        self.start_width = 0.0
        self.end_width = 0.0
        self.bulge = 0.0
        self.constant_width = 0.0
        self.flags = 0
        self.numverts = 0
        self.normal = Vector((0,0,1))

    def new_vertex(self, data):
        self.vertex = Vector()
        self.vertex.x = data
        self.verts.append(self.vertex)

    def build(self, vn=0):
        edges = []
        v_start = vn
        for v in self.verts:
            edges.append((vn, vn+1))
            vn += 1
        if self.flags & PL_CLOSED:
            edges[-1] = (vn-1, v_start)
        else:
            edges.pop()
        verts = self.verts
        if self.normal!=Vector((0,0,1)):
            ma = getOCS(self.normal)
            if ma:
                #ma.invert()
                verts = [ma * v for v in verts]
        return (verts, edges, [], vn-1)
        
#
#    class CLine(CEntity):
#    10 : 'start_point.x', 20 : 'start_point.y', 30 : 'start_point.z', 
#    11 : 'end_point.x', 21 : 'end_point.y', 31 : 'end_point.z', 
#    39 : 'thickness',
#

class CLine(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'LINE', 'Mesh')
        self.start_point = Vector()
        self.end_point = Vector()
        self.thickness = 0.0
        self.normal = Vector((0,0,1))

    def display(self):
        CEntity.display(self)
        print(self.start_point)
        print(self.end_point)

    def build(self, vn=0):
        points = [self.start_point, self.end_point]
        faces, edges = [], []
        n = vn
        thic = self.thickness
        if thic != 0 and (toggle & T_ThicON):
            t_vector = thic * self.normal
            #print 'deb:thic_vector: ', t_vector #---------------------
            points.extend([v + t_vector for v in points])
            faces = [[0+n, 1+n, 3+n, 2+n]]
            self.drawtype = 'Mesh'
        else:
            edges = [[0+n, 1+n]]
        vn +=2
        return((points, edges, faces, vn))

#    class CMLine(CEntity):
#    10 : 'start_point.x', 20 : 'start_point.y', 30 : 'start_point.z', 
#    11 : ['new_vertex(data)'], 21 : 'vertex.y', 31 : 'vertex.z', 
#    12 : ['new_seg_dir(data)'], 22 : 'seg_dir.y', 32 : 'seg_dir.z', 
#    13 : ['new_miter_dir(data)'], 23 : 'miter_dir.y', 33 : 'miter_dir.z', 
#    40 : 'scale', 41 : 'elem_param', 42 : 'fill_param',
#    70 : 'justification', 71 : 'flags'
#    72 : 'numverts', 73 : 'numelems', 74 : 'numparam', 75 : 'numfills',
#    340 : 'id'
#

class CMLine(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'MLINE', None)
        self.start_point = Vector()
        self.vertex = None
        self.seg_dir = None
        self.miter_dir = None
        self.verts = []
        self.seg_dirs = []
        self.miter_dirs = []
        self.scale = 1.0
        self.elem_param = 0
        self.fill_param = 0
        self.justification = 0
        self.flags = 0
        self.numverts = 0
        self.numelems = 0
        self.numparam = 0
        self.numfills = 0
        self.id = 0
        self.normal = Vector((0,0,1))

    def new_vertex(self, data):
        self.vertex = Vector()
        self.vertex.x = data
        self.verts.append(self.vertex)

    def new_seg_dir(self, data):
        self.seg_dir = Vector()
        self.seg_dir.x = data
        self.seg_dirs.append(self.seg_dir)

    def new_miter_dir(self, data):
        self.miter_dir = Vector()
        self.miter_dir.x = data
        self.miter_dirs.append(self.miter_dir)



#
#    class CMText(CText):
#    1 : 'text', 3: 'more_text', 7 : 'style',
#    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
#    11 : 'alignment_point.x', 21 : 'alignment_point.y', 31 : 'alignment_point.z', 
#    40 : 'nominal_height', 41 : 'reference_width', 42: 'width', 43 : 'height', 44 : 'line_spacing',
#    50 : 'rotation_angle', 
#    71 : 'attachment_point', 72 : 'drawing_direction',  73 : 'spacing_style',    
#

class CMText(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'MTEXT', 'Text')
        self.text = ""
        self.more_text = ""
        self.style = ""
        self.insertion_point = Vector()
        self.alignment_point = Vector()
        self.nominal_height = 1.0
        self.reference_width = 1.0
        self.width = 1.0
        self.height = 1.0
        self.rotation_angle = 0.0
        self.attachment_point = 0
        self.drawing_direction = 0
        self.spacing_style = 0
        self.normal = Vector((0,0,1))

    def display(self):
        CEntity.display(self)
        print("%s %s" % (self.text, self.style))
        print('MTEXTinsertion_point=',self.insertion_point)
        print('MTEXTalignment_point=',self.alignment_point)

    def draw(self):
        drawText(self.text,  self.insertion_point, self.height, self.width, self.rotation_angle, 0.0, self.normal)
        return

#
#    class CPoint(CEntity):
#    10 : 'point.x', 20 : 'point.y', 30 : 'point.z', 
#    39 : 'thickness', 50 : 'orientation'
#

class CPoint(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'POINT', 'Mesh')
        self.point = Vector()
        self.thickness = 0.0
        self.orientation = 0.0

    def display(self):
        CEntity.display(self)
        print(self.point)
        print("%.4f" % self.orientation)

    def build(self, vn=0):
        # draw as mesh-vertex
        verts = [self.point]
        return((verts, [], [], vn+1))

    def draw(self):
        #todo
        # draw as empty-object
        # loc = self.point  # UNUSED
        #bpy.ops.object.new('DXFpoint')
        pass

#
#    class CPolyLine(CEntity):
#    1 : 'verts_follow', 2 : 'name',
#    10 : 'elevation.x', 20 : 'elevation.y', 30 : 'elevation.z', 
#    40 : 'start_width', 41 : 'end_width', 
#    66 : 'verts_follow_flag',
#    70 : 'flags', 71 : 'row_count', 72 : 'column_count', 
#    73 : 'row_density', 74 : 'column_density', 75 : 'linetype',
#

class CPolyLine(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'POLYLINE', 'Mesh')
        self.verts = []
        self.verts_follow = 1
        self.name = ""
        self.elevation = Vector()
        self.thickness = 0.0
        self.start_width = 0.0
        self.end_width = 0.0
        self.verts_follow_flags = 0
        self.flags = 0
        self.row_count = 1
        self.column_count = 1
        self.row_density = 1.0
        self.column_density = 1.0
        self.linetype = 1
        self.normal = Vector((0,0,1))

    def display(self):
        CEntity.display(self)
        print("VERTS")
        for v in self.verts:
            print(v.location)
        print("END VERTS")

    def build(self, vn=0):
        verts = []
        lines = []
        v_start = vn
        for vert in self.verts:
            verts.append(vert.location)
            lines.append((vn, vn+1))
            vn += 1
        if self.flags & PL_CLOSED:
            lines[-1] = (vn-1, v_start)
        else:
            lines.pop()
        if self.normal!=Vector((0,0,1)):
            ma = getOCS(self.normal)
            if ma:
                verts = [ma * v for v in verts]
        return((verts, lines, [], vn-1))

#
#    class CShape(CEntity):
#    2 : 'name', 
#    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
#    39 : 'thickness',
#    40 : 'size', 41 : 'x_scale', 
#    50 : 'rotation_angle', 51 : 'oblique_angle',     
#

class CShape(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'SHAPE', None)
        self.name = ""
        self.insertion_point = Vector()
        self.thickness = 0.0
        self.size = 1.0
        self.x_scale = 1.0
        self.rotation_angle = 0.0
        self.oblique_angle = 0.0

    def display(self):
        CEntity.display(self)
        print("%s" % (self.name))
        print(self.insertion_point)

#
#    class CSpline(CEntity):
#    10 : ['new_control_point(data)'], 20 : 'control_point.y', 30 : 'control_point.z', 
#    11 : ['new_fit_point(data)'], 21 : 'fit_point.y', 31 : 'fit_point.z', 
#    40 : ['new_knot_value(data)'], 
#    12 : 'start_tangent.x', 22 : 'start_tangent.y', 32 : 'start_tangent.z', 
#    13 : 'end_tangent.x', 23 : 'end_tangent.y', 33 : 'end_tangent.z', 
#    41 : 'weight', 42 : 'knot_tol', 43 : 'control_point_tol', 44 : 'fit_tol',
#    70 : 'flag', 71 : 'degree', 
#    72 : 'num_knots', 73 : 'num_control_points', 74 : 'num_fit_points',
#    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
#

class CSpline(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'SPLINE', 'Mesh')
        self.control_points = []
        self.fit_points = []
        self.knot_values = []
        self.control_point = None
        self.fit_point = None
        self.knot_value = None
        self.start_tangent = Vector()
        self.end_tangent = Vector()
        self.weight = 1.0
        self.knot_tol = 1e-6
        self.control_point_tol = 1e-6
        self.fit_tol = 1e-6
        self.flag = 0
        self.degree = 3
        self.num_knots = 0
        self.num_control_points = 0
        self.num_fit_points = 0
        self.thickness = 0.0
        self.normal = Vector((0,0,1))
        
    def new_control_point(self, data):
        self.control_point = Vector()
        self.control_point.x = data
        self.control_points.append(self.control_point)
        
    def new_fit_point(self, data):
        self.fit_point = Vector()
        self.fit_point.x = data
        self.fit_points.append(self.fit_point)

    def new_knot_value(self, data):
        self.knot_value = data
        self.knot_values.append(self.knot_value)
        
    def display(self):
        #not testet yet (migius)
        CEntity.display(self)
        print("CONTROL")
        for p in self.control_points:
            print(p)
        print("FIT")
        for p in self.fit_points:
            print(p)
        print("KNOT")
        for v in self.knot_values:
            print(v)

    def build(self, vn=0):
        verts = []
        lines = []
        for vert in self.control_points:
            verts.append(vert)
            lines.append((vn, vn+1))
            vn += 1
        lines.pop()
        return((verts, lines, [], vn))


#
#    class CSolid(CEntity):
#    10 : 'point0.x', 20 : 'point0.y', 30 : 'point0.z', 
#    11 : 'point1.x', 21 : 'point1.y', 31 : 'point1.z', 
#    12 : 'point2.x', 22 : 'point2.y', 32 : 'point2.z', 
#    13 : 'point3.x', 23 : 'point3.y', 33 : 'point3.z', 
#    39 : 'thickness',
#

class CSolid(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'SOLID', 'Mesh')
        self.point0 = Vector()
        self.point1 = Vector()
        self.point2 = Vector()
        self.point3 = Vector()
        self.normal = Vector((0,0,1))
        self.thickness = 0.0
        
    def display(self):
        CEntity.display(self)
        print(self.point0)
        print(self.point1)
        print(self.point2)
        print(self.point3)

    def build(self, vn=0):
        points, edges, faces = [],[],[]
        if self.point2 == self.point3:
            points = [self.point0, self.point1, self.point2]
        else:
            points = [self.point0, self.point1, self.point2, self.point3]
        pn = len(points)
        v0 = vn
        
        thic = self.thickness
        t_vector = Vector((0, 0, thic))
        if thic != 0 and (toggle & T_ThicON):
            thic_points = [v + t_vector for v in points]
            if thic < 0.0:
                thic_points.extend(points)
                points = thic_points
            else:
                points.extend(thic_points)

            if   pn == 4:
                faces = [[0,1,3,2], [4,6,7,5], [0,4,5,1],
                         [1,5,7,3], [3,7,6,2], [2,6,4,0]]
            elif pn == 3:
                faces = [[0,1,2], [3,5,4], [0,3,4,1], [1,4,5,2], [2,5,3,0]]
            elif pn == 2: faces = [[0,1,3,2]]
            vn += 2*pn
        else:
            if   pn == 4: faces = [[0,2,3,1]]
            elif pn == 3: faces = [[0,2,1]]
            elif pn == 2:
                edges = [[0,1]]
                self.drawtype = 'Mesh'
            vn += pn
        if self.normal!=Vector((0,0,1)):
            ma = getOCS(self.normal)
            if ma:
                points = [ma * v for v in points]
        return((points, edges, faces, vn))
        
#
#    class CText(CEntity):
#    1 : 'text', 7 : 'style',
#    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
#    11 : 'alignment_point.x', 21 : 'alignment_point.y', 31 : 'alignment_point.z', 
#    40 : 'height', 41 : 'x_scale', 
#    50 : 'rotation_angle', 51 : 'oblique_angle', 
#    71 : 'flags', 72 : 'horizontal_justification',  73 : 'vertical_justification',    
#

class CText(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'TEXT', 'Text')
        self.text = ""
        self.style = ""
        self.insertion_point = Vector()
        self.alignment_point = Vector()
        self.height = 1.0
        self.x_scale = 1.0
        self.rotation_angle = 0.0
        self.oblique_angle = 0.0
        self.flags = 0
        self.horizontal_justification = 0.0
        self.vertical_justification = 0.0
        self.thickness = 0.0
        self.normal = Vector((0,0,1))
       
    def display(self):
        CEntity.display(self)
        print("%s %s" % (self.text, self.style))
        print(self.insertion_point)
        print(self.alignment_point)
        
    def draw(self):
        drawText(self.text,  self.insertion_point, self.height, self.x_scale, self.rotation_angle, self.oblique_angle, self.normal)
        return


def drawText(text, loc, size, spacing, angle, shear, normal=Vector((0,0,1))):
    #print('angle_deg=',angle)
    bpy.ops.object.text_add(
        view_align=False, 
        enter_editmode=False, 
        location= loc, 
        #rotation=(0, 0, angle), #need radians here
        )
    cu = bpy.context.object.data
    cu.body = text
    cu.size = size #up 2.56
    cu.space_word = spacing #up 2.56
    cu.shear = shear
    if angle!=0.0 or normal!=Vector((0,0,1)):
        obj = bpy.context.object
        transform(normal, angle, obj)
    return

#
#    class CTolerance(CEntity):
#    3 : 'style',
#    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
#    11 : 'direction.x', 21 : 'direction.y', 31 : 'direction.z', 
#

class CTolerance(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'TOLERANCE', None)
        self.stype = ""
        self.insertion_point = Vector()
        self.direction = Vector()

#
#    class CTrace(CEntity):
#    10 : 'point0.x', 20 : 'point0.y', 30 : 'point0.z', 
#    11 : 'point1.x', 21 : 'point1.y', 31 : 'point1.z', 
#    12 : 'point2.x', 22 : 'point2.y', 32 : 'point2.z', 
#    13 : 'point3.x', 23 : 'point3.y', 33 : 'point3.z', 
#    39 : 'thickness',
#

class CTrace(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'TRACE', 'Mesh')
        self.point0 = Vector()
        self.point1 = Vector()
        self.point2 = Vector()
        self.point3 = Vector()
        self.normal = Vector((0,0,1))
        self.thickness = 0.0
    
    def display(self):
        CEntity.display(self)
        print(self.point0)
        print(self.point1)
        print(self.point2)
        print(self.point3)
   
    def build(self, vn=0):
        points, edges, faces = [],[],[]
        if self.point2 == self.point3:
            points = [self.point0, self.point2, self.point1]
        else:
            points = [self.point0, self.point2, self.point1, self.point3]
        pn = len(points)
        v0 = vn
        thic = self.thickness
        t_vector = Vector((0, 0, thic))
        if thic != 0 and (toggle & T_ThicON):
            thic_points = [v + t_vector for v in points]
            if thic < 0.0:
                thic_points.extend(points)
                points = thic_points
            else:
                points.extend(thic_points)

            if   pn == 4:
                faces = [[0,1,3,2], [4,6,7,5], [0,4,5,1],
                         [1,5,7,3], [3,7,6,2], [2,6,4,0]]
            elif pn == 3:
                faces = [[0,1,2], [3,5,4], [0,3,4,1], [1,4,5,2], [2,5,3,0]]
            elif pn == 2: faces = [[0,1,3,2]]
            vn += 2*pn
        else:
            if   pn == 4: faces = [[0,2,3,1]]
            elif pn == 3: faces = [[0,2,1]]
            elif pn == 2:
                edges = [[0,1]]
                self.drawtype = 'Mesh'
        if self.normal!=Vector((0,0,1)):
            ma = getOCS(self.normal)
            if ma:
                points = [ma * v for v in points]
        return ((points, edges, faces, vn))

#
#    class CVertex(CEntity):
#    10 : 'location.x', 20 : 'location.y', 30 : 'location.z', 
#    40 : 'start_width', 41 : 'end_width', 42 : 'bulge', 
#    50 : 'tangent',
#    70 : 'flags',
#    71 : 'index1', 72 : 'index2', 73 : 'index3', 74 : 'index4', 
#

class CVertex(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'VERTEX', None)
        self.location = Vector()
        self.start_width = 0.0
        self.end_width = 0.0
        self.bulge = 0.0
        self.tangent = 0.0
        self.flags = 0

    def display(self):
        return

    def draw(self):
        return

#            
#    class CViewPort(CEntity):
#    10 : 'center.x', 20 : 'center.y', 30 : 'center.z', 
#    12 : 'view_center.x', 22 : 'view_center.y', 32 : 'view_center.z', 
#    13 : 'snap_base.x', 23 : 'snap_base.y', 33 : 'snap_base.z', 
#    14 : 'snap_spacing.x', 24 : 'snap_spacing.y', 34 : 'snap_spacing.z', 
#    15 : 'grid_spacing.x', 25 : 'grid_spacing.y', 35 : 'grid_spacing.z', 
#    16 : 'view_direction.x', 26 : 'view_direction.y', 36 : 'view_direction.z', 
#    40 : 'width', 41 : 'height',
#    68 : 'status', 69 : 'id',
#

class CViewPort(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'VIEWPORT', None)
        self.center = Vector()
        self.view_center = Vector()
        self.snap_base = Vector()
        self.snap_spacing = Vector()
        self.grid_spacing = Vector()
        self.view_direction = Vector()
        self.width = 1.0
        self.height = 1.0
        self.status = 0
        self.id = 0

    def draw(self):
        # Todo
        return

#
#    class CWipeOut(CEntity):
#    10 : 'point.x', 20 : 'point.y', 30 : 'point.z', 
#    11 : 'direction.x', 21 : 'direction.y', 31 : 'direction.z', 
#

class CWipeOut(CEntity):
    def __init__(self):
        CEntity.__init__(self, 'WIPEOUT', None)
        self.point = Vector()
        self.direction = Vector()
