import os
import codecs
import math
from math import sin, cos, radians
import bpy
from bpy.props import StringProperty, EnumProperty, BoolProperty, FloatProperty, IntProperty
from mathutils import Vector, Matrix

from .domain.dxf.constants import *
from .entities import *
#
#    Global flags
#

T_Merge = 0x01
T_NewScene = 0x02
T_Curves = 0x04
T_DrawOne = 0x08
T_Debug = 0x10
T_Verbose = 0x20
T_ThicON = 0x40

toggle = T_Merge | T_NewScene | T_DrawOne | T_ThicON
theCircleRes = 32
theMergeLimit = 1e-4

#
#
#
WORLDX = Vector((1.0,0.0,0.0))
WORLDY = Vector((0.0,1.0,0.0))
WORLDZ = Vector((0.0,0.0,1.0))


def getOCS(az):  #-----------------------------------------------------------------
    """An implimentation of the Arbitrary Axis Algorithm.
    """
    #decide if we need to transform our coords
    #if az[0] == 0 and az[1] == 0: 
    if abs(az.x) < 0.00001 and abs(az.y) < 0.00001:
        if az.z > 0.0:
            return False
        elif az.z < 0.0:
            return Matrix((-WORLDX, WORLDY*1, -WORLDZ)).transposed()

    cap = 0.015625 # square polar cap value (1/64.0)
    if abs(az.x) < cap and abs(az.y) < cap:
        ax = WORLDY.cross(az)
    else:
        ax = WORLDZ.cross(az)
    ax.normalize()
    ay = az.cross(ax)
    ay.normalize()
    # Matrices are now constructed from rows, transpose to make the rows into cols
    return Matrix((ax, ay, az)).transposed()



def transform(normal, rotation, obj):  #--------------------------------------------
    """Use the calculated ocs to determine the objects location/orientation in space.
    """
    ma = Matrix()
    o = Vector(obj.location)
    ma_new = getOCS(normal)
    if ma_new:
        ma_new.resize_4x4()
        ma = ma_new
        o = ma * o

    if rotation != 0:
        rmat = Matrix.Rotation(radians(rotation), 4, 'Z')
        ma = ma * rmat

    obj.matrix_world = ma
    obj.location = o


#
#    readDxfFile(filePath):
#

def readDxfFile(fileName):    
    global toggle, theCodec

    print( "Opening DXF file "+ fileName )

    # fp= open(fileName, "rU")
    fp = codecs.open(fileName, "r", encoding=theCodec)
    first = True
    statements = []
    no = 0
    for line in fp: 
        word = line.strip()
        no += 1
        if first:
            if word:
                code = int(word)
                first = False
        else:
            if toggle & T_Verbose:
                print("%4d: %4d %s" % (no, code, word))
            if code < 10:
                data = word
            elif code < 60:
                data = float(word)
            elif code < 100:
                data = int(word)
            elif code < 140:
                data = word
            elif code < 150:
                data = float(word)
            elif code < 200:
                data = int(word)
            elif code < 300:
                data = float(word)
            elif code < 370:
                data = word
            elif code < 390:
                data = int(word)
            elif code < 400:
                data = word
            elif code < 410:
                data = int(word)
            elif code < 1010:
                data = word
            elif code < 1060:
                data = float(word)
            elif code < 1080:
                data = int(word)

            statements.append((code,data))
            first = True
    fp.close()

    statements.reverse()
    sections = {}
    handles = {}
    while statements:
        (code,data) = statements.pop()
        if code == 0:
            if data == 'SECTION':
                section = CSection()
        elif code == 2:
            section.type = data
            if data == 'HEADER':
                parseHeader(section, statements, handles)
                known = False
            elif data == 'CLASSES':
                parseClasses(section, statements, handles)
                known = False
            elif data == 'TABLES':
                parseTables(section, statements, handles)
                known = False
            elif data == 'BLOCKS':
                parseBlocks(section, statements, handles)
                known = False
            elif data == 'ENTITIES':
                parseEntities(section, statements, handles)
                known = False
            elif data == 'OBJECTS':
                parseObjects(section, statements, handles)
            elif data == 'THUMBNAILIMAGE':
                parseThumbnail(section, statements, handles)
            sections[data] = section
        elif code == 999:
            pass
        else:
            raise NameError("Unexpected code in SECTION context: %d %s" % (code,data))

    if toggle & T_Verbose:
        for (typ,section) in sections.items():
            section.display()
    return sections
    

#
#     0
#    SECTION
#      2
#    HEADER
#    
#      9
#    $<variable>
#    <group code>
#    <value>
#    
#      0
#    ENDSEC

    
def parseHeader(section, statements, handles):
    while statements:
        (code,data) = statements.pop()
        if code == 0:
            if data == 'ENDSEC':
                return

    return


#      0
#    SECTION
#      2
#    CLASSES
#    
#      0
#    CLASS
#      1
#    <class dxf record>
#      2
#    <class name>
#      3
#    <app name>
#    90
#    <flag>
#    280
#    <flag>
#    281
#    <flag>
#    
#      0
#    ENDSEC         

def parseClasses(section, statements, handles):
    while statements:
        (code,data) = statements.pop()
        if code == 0:
            if data == 'ENDSEC':
                return

    return
    

#      0
#    SECTION
#      2
#    TABLES
#    
#      0
#    TABLE
#      2
#    <table type>
#      5
#    <handle>
#    100
#    AcDbSymbolTable
#    70
#    <max. entries>
#    
#      0
#    <table type>
#      5
#    <handle>
#    100
#    AcDbSymbolTableRecord
#    .
#    . <data>
#    .
#    
#      0
#    ENDTAB
#    
#      0
#    ENDSEC 

#
#      APPID (application identification table)
#
#      BLOCK_RECORD (block reference table)
#
#      DIMSTYLE (dimension style table)
#
#      LAYER (layer table)
#
#      LTYPE (linetype table)
#
#      STYLE (text style table)
#
#      UCS (User Coordinate System table)
#
#      VIEW (view table)
#
#      VPORT (viewport configuration table)


def parseTables(section, statements, handles):
    tables = []
    section.data = tables
    while statements:
        (code,data) = statements.pop()
        if code == 0:
            if data == 'ENDSEC':
                return
    '''
                known = False
            elif data == 'TABLE':
                table = CTable()
                tables.append(table)
                known = False
            elif data == 'ENDTAB':
                pass
                known = False
            elif data == table.type:
                parseTableType
                table = CTable()
                tables.append(table)
                table.type = word
        elif code == 2:
            table.type = word
        elif code == 5:
            table.handle = word
            handles[word] = table
        elif code == 330:
            table.owner = word
        elif code == 100:
            table.subclass = word
        elif code == 70:
            table.nEntries = int(word)
    '''
    return
    
#      0
#    SECTION
#      2
#    BLOCKS
#    
#      0
#    BLOCK
#      5
#    <handle>
#    100
#    AcDbEntity
#      8
#    <layer>
#    100
#    AcDbBlockBegin
#      2
#    <block name>
#    70
#    <flag>
#    10
#    <X value>
#    20
#    <Y value>
#    30
#    <Z value>
#      3
#    <block name>
#      1
#    <xref path>
#    
#      0
#    <entity type>
#    .
#    . <data>
#    .
#    
#      0
#    ENDBLK
#      5
#    <handle>
#    100
#    AcDbBlockEnd
#    
#      0
#    ENDSEC 

def parseBlocks(section, statements, handles):
    while statements:
        (code,data) = statements.pop()
        if code == 0:
            if data == 'ENDSEC':
                return

    return

#      0
#    SECTION
#      2
#    ENTITIES
#    
#      0
#    <entity type>
#      5
#    <handle>
#    330
#    <pointer to owner>
#    100
#    AcDbEntity
#      8
#    <layer>
#    100
#    AcDb<classname>
#    .
#    . <data>
#    .
#    
#      0
#    ENDSEC

Ignorables = ['DIMENSION', 'TEXT', 'VIEWPORT']

ClassCreators = {
    '3DFACE':         'C3dFace()', 
    '3DSOLID':        'C3dSolid()',
    'ACAD_PROXY_ENTITY':    'CAcadProxyEntity()',
    'ACAD_ZOMBIE_ENTITY':    0,
    'ARC':            'CArc()',
    'ARCALIGNEDTEXT':    'CArcAlignedText()',
    'ATTDEF':        'CAttdef()',
    'ATTRIB':        'CAttrib()',
    'BODY':            0,
    'CIRCLE':        'CCircle()',
    'DIMENSION':        'CDimension()',
    'ELLIPSE':        'CEllipse()',
    'HATCH':        'CHatch()',
    'IMAGE':        'CImage()',
    'INSERT':        'CInsert()',
    'LEADER':        'CLeader()',
    'LINE':            'CLine()',
    'LWPOLYLINE':        'CLWPolyLine()',
    'MLINE':        'CMLine()',
    'MTEXT':        'CMText()',
    'OLEFRAME':        0,
    'OLE2FRAME':        0,
    'POINT':        'CPoint()',
    'POLYLINE':        'CPolyLine()',
    'RAY':            'CRay()',
    'REGION':        0,
    'RTEXT':        'CRText',
    'SEQEND':        0,
    'SHAPE':        'CShape()',
    'SOLID':        'CSolid()',
    'SPLINE':        'CSpline()',
    'TEXT':            'CText()',
    'TOLERANCE':        'CTolerance()',
    'TRACE':        'CTrace()',
    'VERTEX':        'CVertex()',
    'VIEWPORT':        'CViewPort()',
    'WIPEOUT':        'CWipeOut()',
    'XLINE':        'CXLine()',
}

def parseEntities(section, statements, handles):
    entities = []
    section.data = entities
    while statements:
        (code,data) = statements.pop()
        if toggle & T_Verbose:
            print("ent", code,data)
        if code == 0:
            known = True
            if data in Ignorables:
                ignore = True
            else:
                ignore = False

            try:
                creator = ClassCreators[data]
            except:
                creator = None
                
            if creator:
                entity = eval(creator)
            elif data == 'ENDSEC':
                return
            else:
                known = False
                
            if data == 'POLYLINE':
                verts = entity.verts
            elif data == 'VERTEX':
                verts.append(entity)
            
            if data == 'SEQEND':
                attributes = []
                known = False
            elif creator == 0:
                ignore = True
            elif known:
                entities.append(entity)
                attributes = DxfEntityAttributes[data]
            else:
                raise NameError("Unknown data %s" % data)

        elif not known:
            pass
        else:
            expr = getAttribute(attributes, code)
            if expr:
                exec(expr)
            else:
                expr = getAttribute(DxfCommonAttributes, code)
                if expr:
                    exec(expr)
                elif code >= 1000 or ignore:
                    pass
                elif toggle & T_Debug:
                    raise NameError("Unknown code %d for %s" % (code, entity.type))
                
    return

def getAttribute(attributes, code):
    try:
        ext = attributes[code]
        if type(ext) == str:
            expr = "entity.%s = data" % ext
        else:
            name = ext[0]
            expr = "entity.%s" % name
    except:
        expr = None
    return expr


#      0
#    SECTION
#      2
#    OBJECTS
#    
#      0
#    DICTIONARY
#      5
#    <handle>
#    100
#    AcDbDictionary
#    
#      3
#    <dictionary name>
#    350
#    <handle of child>
#    
#      0
#    <object type>
#    .
#    . <data>
#    .
#    
#      0
#    ENDSEC 

def parseObjects(data, statements, handles):
    while statements:
        (code,data) = statements.pop()
        if code == 0:
            if data == 'ENDSEC':
                return

    return

#    
#    THUMBNAILIMAGE
#     90
#        45940
#    310
#    28000000B40000005500000001001800000000000000000000000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFF
#FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
#FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
#    310
#    FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
#FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
#FFFFFFFFFFFFFFFFFFFFFFFFFF
#    310
#    .......
#      0
#    ENDSEC

def parseThumbnail(section, statements, handles):
    """ Just skip these """
    while statements:
        (code,data) = statements.pop()
        if code == 0:
            if data == 'ENDSEC':
                return

    return

#
#    buildGeometry(entities):
#    addMesh(name, verts, edges, faces):                            
#

def buildGeometry(entities):
    try: bpy.ops.object.mode_set(mode='OBJECT')
    except: pass
    v_verts = []
    v_vn = 0
    e_verts = []
    e_edges = []
    e_vn = 0
    f_verts = []
    f_edges = []
    f_faces = []
    f_vn = 0
    for ent in entities:
        if ent.drawtype in {'Mesh', 'Curve'}:
            (verts, edges, faces, vn) = ent.build()
            if not toggle & T_DrawOne:
                drawGeometry(verts, edges, faces)
            else:
                if verts:
                    if faces:
                        for i,f in enumerate(faces):
                            #print ('face=', f)
                            faces[i] = tuple(it+f_vn for it in f)
                        for i,e in enumerate(edges):
                            edges[i] = tuple(it+f_vn for it in e)
                        f_verts.extend(verts)
                        f_edges.extend(edges)
                        f_faces.extend(faces)
                        f_vn += len(verts)
                    elif edges:
                        for i,e in enumerate(edges):
                            edges[i] = tuple(it+e_vn for it in e)
                        e_verts.extend(verts)
                        e_edges.extend(edges)
                        e_vn += len(verts)
                    else:
                        v_verts.extend(verts)
                        v_vn += len(verts)
        else:
            ent.draw()
                    
    if toggle & T_DrawOne:
        drawGeometry(f_verts, f_edges, f_faces)
        drawGeometry(e_verts, e_edges)
        drawGeometry(v_verts)



def drawGeometry(verts, edges=[], faces=[]):
    if verts:
        if edges and (toggle & T_Curves):
            print ('draw Curve')
            cu = bpy.data.curves.new('DXFlines', 'CURVE')
            cu.dimensions = '3D'
            buildSplines(cu, verts, edges)
            ob = addObject('DXFlines', cu)
        else:
            #for v in verts: print(v)
            #print ('draw Mesh with %s vertices' %(len(verts)))
            #for e in edges: print(e)
            #print ('draw Mesh with %s edges' %(len(edges)))
            #for f in faces: print(f)
            #print ('draw Mesh with %s faces' %(len(faces)))
            me = bpy.data.meshes.new('DXFmesh')
            me.from_pydata(verts, edges, faces)
            ob = addObject('DXFmesh', me)
            removeDoubles(ob)
    return



def buildSplines(cu, verts, edges):
    if edges:
        point_list = []
        (v0,v1) = edges.pop()
        v1_old = v1
        newPoints = [tuple(verts[v0]),tuple(verts[v1])]
        for (v0,v1) in edges:
            if v0==v1_old:
                newPoints.append(tuple(verts[v1]))
            else:
                #print ('newPoints=', newPoints)
                point_list.append(newPoints)
                newPoints = [tuple(verts[v0]),tuple(verts[v1])]
            v1_old = v1
        point_list.append(newPoints)
        for points in point_list:
            spline = cu.splines.new('POLY')
            #spline = cu.splines.new('BEZIER')
            #spline.use_endpoint_u = True
            #spline.order_u = 2
            #spline.resolution_u = 1
            #spline.bezier_points.add(2)

            spline.points.add(len(points)-1)
            #spline.points.foreach_set('co', points)
            for i,p in enumerate(points):
                spline.points[i].co = (p[0],p[1],p[2],0)
                
        #print ('spline.type=', spline.type)
        #print ('spline number=', len(cu.splines))
    
    
def addObject(name, data):
    ob = bpy.data.objects.new(name, data)
    scn = bpy.context.scene
    scn.objects.link(ob)
    return ob


def removeDoubles(ob):
    global theMergeLimit
    if toggle & T_Merge:
        scn = bpy.context.scene
        scn.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.remove_doubles(threshold=theMergeLimit)
        bpy.ops.object.mode_set(mode='OBJECT')



#
#    clearScene(context):
#
    
def clearScene():
    global toggle
    scn = bpy.context.scene
    print("clearScene %s %s" % (toggle & T_NewScene, scn))
    if not toggle & T_NewScene:
        return scn

    for ob in scn.objects:
        if ob.type in ["MESH", "CURVE", "TEXT"]:
            scn.objects.active = ob
            bpy.ops.object.mode_set(mode='OBJECT')
            scn.objects.unlink(ob)
            del ob
    return scn

#
#    readAndBuildDxfFile(filepath):
#

def readAndBuildDxfFile(filepath):
    fileName = os.path.expanduser(filepath)
    if fileName:
        (shortName, ext) = os.path.splitext(fileName)
        #print("filepath: ", filepath)
        #print("fileName: ", fileName)
        #print("shortName: ", shortName)
        if ext.lower() != ".dxf":
            print("Error: Not a dxf file: " + fileName)
            return
        if toggle & T_NewScene:
            clearScene()
            if 0: # how to switch to the new scene?? (migius)
                new_scn = bpy.data.scenes.new(shortName[-20:])
                #new_scn.layers = (1<<20) -1
                #new_scn_name = new_scn.name  # UNUSED
                bpy.data.screens.scene = new_scn
                #print("newScene: %s" % (new_scn))
        sections = readDxfFile(fileName)
        print("Building geometry")
        buildGeometry(sections['ENTITIES'].data)
        print("Done")
        return
    print("Error: Not a dxf file: " + filepath)
    return

#
#    User interface
#

DEBUG= False
from bpy.props import *

def tripleList(list1):
    list3 = []
    for elt in list1:
        list3.append((elt,elt,elt))
    return list3

class DxfImportProcessor(bpy.types.Operator):
    """Import scene from DXF file format (.dxf)"""
    bl_idname = "import_scene.autocad_dxf"
    bl_description = 'Import scene from DXF file format (.dxf)'
    bl_label = "Import DXF"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'UNDO'}

    filepath = StringProperty(
            subtype='FILE_PATH',
            )
    new_scene = BoolProperty(
            name="Replace scene",
            description="Replace scene",
            default=toggle & T_NewScene,
            )
    curves = BoolProperty(
            name="Draw curves",
            description="Draw entities as curves",
            default=toggle & T_Curves,
            )
    thic_on = BoolProperty(
            name="Thick ON",
            description="Support THICKNESS",
            default=toggle & T_ThicON,
            )
    merge = BoolProperty(
            name="Remove doubles",
            description="Merge coincident vertices",
            default=toggle & T_Merge,
            )
    mergeLimit = FloatProperty(
            name="Limit",
            description="Merge limit * 0.0001",
            default=theMergeLimit * 1e4,
            min=1.0,
            soft_min=1.0,
            max=1000.0,
            soft_max=1000.0,
            )
    draw_one = BoolProperty(
            name="Merge all",
            description="Draw all into one mesh object",
            default=toggle & T_DrawOne,
            )
    circleResolution = IntProperty(
            name="Circle resolution",
            description="Circle/Arc are approximated with this factor",
            default=theCircleRes,
            min=4,
            soft_min=4,
            max=360,
            soft_max=360,
            )
    codecs = tripleList(['iso-8859-15', 'utf-8', 'ascii'])
    codec = EnumProperty(name="Codec",
            description="Codec",
            items=codecs,
            default='ascii',
            )
    debug = BoolProperty(
            name="Debug",
            description="Unknown DXF-codes generate errors",
            default=toggle & T_Debug,
            )
    verbose = BoolProperty(
            name="Verbose",
            description="Print debug info",
            default=toggle & T_Verbose,
            )

    ##### DRAW #####
    def draw(self, context):
        layout0 = self.layout
        #layout0.enabled = False

        #col = layout0.column_flow(2,align=True)
        layout = layout0.box()
        col = layout.column()
        #col.prop(self, 'KnotType') waits for more knottypes
        #col.label(text="import Parameters")
        #col.prop(self, 'replace')
        col.prop(self, 'new_scene')
        
        row = layout.row(align=True)
        row.prop(self, 'curves')
        row.prop(self, 'circleResolution')

        row = layout.row(align=True)
        row.prop(self, 'merge')
        if self.merge:
            row.prop(self, 'mergeLimit')
 
        row = layout.row(align=True)
        #row.label('na')
        row.prop(self, 'draw_one')
        row.prop(self, 'thic_on')

        col = layout.column()
        col.prop(self, 'codec')
 
        row = layout.row(align=True)
        row.prop(self, 'debug')
        if self.debug:
            row.prop(self, 'verbose')
         
    def execute(self, context):
        global toggle, theMergeLimit, theCodec, theCircleRes
        O_Merge = T_Merge if self.merge else 0
        #O_Replace = T_Replace if self.replace else 0
        O_NewScene = T_NewScene if self.new_scene else 0
        O_Curves = T_Curves if self.curves else 0
        O_ThicON = T_ThicON if self.thic_on else 0
        O_DrawOne = T_DrawOne if self.draw_one else 0
        O_Debug = T_Debug if self.debug else 0
        O_Verbose = T_Verbose if self.verbose else 0

        toggle =  O_Merge | O_DrawOne | O_NewScene | O_Curves | O_ThicON | O_Debug | O_Verbose
        theMergeLimit = self.mergeLimit*1e-4
        theCircleRes = self.circleResolution
        theCodec = self.codec
        
        

        readAndBuildDxfFile(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}