DxfCommonAttributes = {
    5 : 'handle',
    6 : 'linetype_name',
    8 : 'layer',
    48 : 'linetype_scale',
    60 : 'invisible',
    62 : 'color',
    67 : 'paperspace',
    100 : 'subclass',
    330 : 'owner',
    360 : 'owner',
}


DxfEntityAttributes = {
'3DFACE'    : {
    10 : 'point0.x', 20 : 'point0.y', 30 : 'point0.z', 
    11 : 'point1.x', 21 : 'point1.y', 31 : 'point1.z', 
    12 : 'point2.x', 22 : 'point2.y', 32 : 'point2.z', 
    13 : 'point3.x', 23 : 'point3.y', 33 : 'point3.z', 
    70 : 'flags',
    },

'3DSOLID'    : {
    1 : 'data', 3 : 'more', 70 : 'version',
    },

'ACAD_PROXY_ENTITY'    : {
    70 : 'format',
    90 : 'id', 91 : 'class', 92 : 'graphics_size', 93 : 'entity_size', 95: 'format',
    310 : 'data', 330 : 'id1', 340 : 'id2', 350 : 'id3', 360 : 'id4', 
    },

'ARC'        : {
    10 : 'center.x', 20 : 'center.y', 30 : 'center.z', 
    40 : 'radius',
    50 : 'start_angle', 51 : 'end_angle',
    39 : 'thickness',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'ARCALIGNEDTEXT'    : {
    1 : 'text', 2 : 'font', 3 : 'bigfont', 7 : 'style',
    10 : 'center.x', 20 : 'center.y', 30 : 'center.z', 
    40 : 'radius', 41 : 'width', 42 : 'height', 43 : 'spacing', 
    44 : 'offset', 45 : 'right_offset', 46 : 'left_offset', 
    50 : 'start_angle', 51 : 'end_angle',
    70 : 'order', 71 : 'direction', 72 : 'alignment', 73 : 'side', 
    74 : 'bold', 75 : 'italic', 76 : 'underline',
    77 : 'character_set', 78 : 'pitch', 79 : 'fonttype',
    90 : 'color',
    280 : 'wizard', 330 : 'id'
    },

'ATTDEF'    : {
    1 : 'text', 2 : 'tag', 3 : 'prompt', 7 : 'style',
    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
    11 : 'alignment_point.x', 21 : 'alignment_point.y', 31 : 'alignment_point.z', 
    40 : 'height', 41 : 'x_scale', 
    50 : 'rotation_angle', 51 : 'oblique_angle', 
    70 : 'flags', 71 : 'text_generation_flags', 
    72 : 'horizontal_justification',  74 : 'vertical_justification',    
    },


'ATTRIB'    : {
    1 : 'text', 2 : 'tag', 3 : 'prompt', 7 : 'style',
    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
    11 : 'alignment_point.x', 21 : 'alignment_point.y', 31 : 'alignment_point.z', 
    40 : 'height', 41 : 'x_scale', 
    50 : 'rotation_angle', 51 : 'oblique_angle', 
    70 : 'flags', 73 : 'length', 
    71 : 'text_generation_flags', 72 : 'horizontal_justification',  74 : 'vertical_justification',     
    },

'BLOCK'        : {
    1 : 'xref', 2 : 'name', 3 : 'also_name', 
    10 : 'base_point.x', 20 : 'base_point.y', 30 : 'base_point.z', 
    40 : 'size', 41 : 'x_scale', 
    50 : 'rotation_angle', 51 : 'oblique_angle',     
    70 : 'flags', 
    },

'CIRCLE'    : {
    10 : 'center.x', 20 : 'center.y', 30 : 'center.z', 
    40 : 'radius',
    39 : 'thickness',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'DIMENSION'    : {
    1 : 'text', 2 : 'name', 3 : 'style',
    10 : 'def_point.x', 20 : 'def_point.y', 30 : 'def_point.z', 
    11 : 'mid_point.x', 21 : 'mid_point.y', 31 : 'mid_point.z', 
    12 : 'vector.x', 22 : 'vector.y', 32 : 'vector.z', 
    13 : 'def_point2.x', 23 : 'def_point2.y', 33 : 'def_point2.z', 
    14 : 'vector2.x', 24 : 'vector2.y', 34 : 'vector2.z', 
    15 : 'vector3.x', 25 : 'vector3.y', 35 : 'vector3.z', 
    16 : 'vector4.x', 26 : 'vector4.y', 36 : 'vector4.z', 
    70 : 'dimtype',
    },

'ELLIPSE'    : {
    10 : 'center.x', 20 : 'center.y', 30 : 'center.z', 
    11 : 'end_point.x', 21 : 'end_point.y', 31 : 'end_point.z', 
    40 : 'ratio', 41 : 'start', 42 : 'end',
    39 : 'thickness',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'HATCH'        : {
    2 : 'pattern',
    10 : 'point.x', 20 : 'point.y', 30 : 'point.z', 
    41 : 'scale', 47 : 'pixelsize', 52 : 'angle',
    70 : 'fill', 71 : 'associativity', 75: 'style', 77 : 'double', 
    78 : 'numlines', 91 : 'numpaths', 98 : 'numseeds',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'IMAGE'        : {
    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
    11 : 'u_vector.x', 21 : 'u_vector.y', 31 : 'u_vector.z', 
    12 : 'v_vector.x', 22 : 'v_vector.y', 32 : 'v_vector.z', 
    13 : 'size.x', 23 : 'size.y', 33 : 'size.z', 
    14 : 'clip.x', 24 : 'clip.y', 34 : 'clip.z', 
    70 : 'display', 71 : 'cliptype', 
    90 : 'version',
    280 : 'clipstate', 281 : 'brightness', 282 : 'contrast', 283 : 'fade', 
    340 : 'image', 360 : 'reactor',
    },

'INSERT'    : {
    1 : 'attributes_follow', 2 : 'name',
    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
    41 : 'x_scale', 42 : 'y_scale', 43 : 'z_scale', 
    44 : 'column_spacing', 45 : 'row_spacing', 
    50 : 'rotation_angle', 66 : 'attributes_follow',
    70 : 'column_count', 71 : 'row_count', 
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'LEADER'    : {
    3 : 'style',
    10 : ['new_vertex(data)'], 20 : 'vertex.y', 30 : 'vertex.z', 
    40 : 'height', 41 : 'width',
    71 : 'arrowhead', 72 : 'pathtype', 73 : 'creation', 
    74 : 'hookdir', 75 : 'hookline', 76 : 'numverts', 77 : 'color',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    211 : 'horizon.x', 221 : 'horizon.y', 231 : 'horizon.z', 
    212 : 'offset_ins.x', 222 : 'offset_ins.y', 232 : 'offset_ins.z', 
    213 : 'offset_ann.x', 223 : 'offset_ann.y', 233 : 'offset_ann.z', 
    },

'LINE'        : {
    10 : 'start_point.x', 20 : 'start_point.y', 30 : 'start_point.z', 
    11 : 'end_point.x', 21 : 'end_point.y', 31 : 'end_point.z', 
    39 : 'thickness',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'LWPOLYLINE'    : {
    10 : ['new_vertex(data)'], 20 : 'vertex.y', 30 : 'vertex.z', 
    38 : 'elevation', 39 : 'thickness',
    40 : 'start_width', 41 : 'end_width', 42 : 'bulge', 43 : 'constant_width',
    70 : 'flags', 90 : 'numverts',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },
        
'MLINE'    : {
    10 : 'start_point.x', 20 : 'start_point.y', 30 : 'start_point.z', 
    11 : ['new_vertex(data)'], 21 : 'vertex.y', 31 : 'vertex.z', 
    12 : ['new_seg_dir(data)'], 22 : 'seg_dir.y', 32 : 'seg_dir.z', 
    13 : ['new_miter_dir(data)'], 23 : 'miter_dir.y', 33 : 'miter_dir.z', 
    39 : 'thickness',
    40 : 'scale', 41 : 'elem_param', 42 : 'fill_param',
    70 : 'justification', 71 : 'flags',
    72 : 'numverts', 73 : 'numelems', 74 : 'numparam', 75 : 'numfills',
    340 : 'id',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },
        
'MTEXT'        : {
    1 : 'text', 3: 'more_text', 7 : 'style',
    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
    11 : 'alignment_point.x', 21 : 'alignment_point.y', 31 : 'alignment_point.z', 
    40 : 'nominal_height', 41 : 'reference_width', 42: 'width', 43 : 'height', 44 : 'line_spacing',
    50 : 'rotation_angle', 
    71 : 'attachment_point', 72 : 'drawing_direction',  73 : 'spacing_style',    
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'POINT'        : {
    10 : 'point.x', 20 : 'point.y', 30 : 'point.z', 
    39 : 'thickness', 50 : 'orientation',
    },

'POLYLINE'    : {
    1 : 'verts_follow', 2 : 'name',
    10 : 'elevation.x', 20 : 'elevation.y', 30 : 'elevation.z', 
    39 : 'thickness',
    40 : 'start_width', 41 : 'end_width', 
    66 : 'verts_follow_flag',
    70 : 'flags', 71 : 'row_count', 72 : 'column_count', 
    73 : 'row_density', 74 : 'column_density', 75 : 'linetype',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'RAY'        : {
    10 : 'point.x', 20 : 'point.y', 30 : 'point.z', 
    11 : 'direction.x', 21 : 'direction.y', 31 : 'direction.z', 
    },

'RTEXT'        : {
    1 : 'text', 7 : 'style',
    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
    39 : 'thickness',
    40 : 'height', 
    50 : 'rotation_angle',
    70 : 'flags',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'SHAPE'        : {
    2 : 'name', 
    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
    39 : 'thickness',
    40 : 'size', 41 : 'x_scale', 
    50 : 'rotation_angle', 51 : 'oblique_angle',     
    39 : 'thickness',
    },

'SOLID'        : {
    10 : 'point0.x', 20 : 'point0.y', 30 : 'point0.z', 
    11 : 'point1.x', 21 : 'point1.y', 31 : 'point1.z', 
    12 : 'point2.x', 22 : 'point2.y', 32 : 'point2.z', 
    13 : 'point3.x', 23 : 'point3.y', 33 : 'point3.z', 
    39 : 'thickness',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'SPLINE'    : {
    10 : ['new_control_point(data)'], 20 : 'control_point.y', 30 : 'control_point.z', 
    11 : ['new_fit_point(data)'], 21 : 'fit_point.y', 31 : 'fit_point.z', 
    40 : ['new_knot_value(data)'], 
    12 : 'start_tangent.x', 22 : 'start_tangent.y', 32 : 'start_tangent.z', 
    13 : 'end_tangent.x', 23 : 'end_tangent.y', 33 : 'end_tangent.z', 
    39 : 'thickness',
    41 : 'weight', 42 : 'knot_tol', 43 : 'control_point_tol', 44 : 'fit_tol',
    70 : 'flag', 71 : 'degree', 
    72 : 'num_knots', 73 : 'num_control_points', 74 : 'num_fit_points',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'TEXT'        : {
    1 : 'text', 7 : 'style',
    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
    11 : 'alignment_point.x', 21 : 'alignment_point.y', 31 : 'alignment_point.z', 
    40 : 'height', 41 : 'x_scale', 
    50 : 'rotation_angle', 51 : 'oblique_angle', 
    71 : 'flags', 72 : 'horizontal_justification',  73 : 'vertical_justification',    
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'TOLERANCE'    : {
    3 : 'style',
    10 : 'insertion_point.x', 20 : 'insertion_point.y', 30 : 'insertion_point.z', 
    11 : 'direction.x', 21 : 'direction.y', 31 : 'direction.z', 
    },

'TRACE'        : {
    10 : 'point0.x', 20 : 'point0.y', 30 : 'point0.z', 
    11 : 'point1.x', 21 : 'point1.y', 31 : 'point1.z', 
    12 : 'point2.x', 22 : 'point2.y', 32 : 'point2.z', 
    13 : 'point3.x', 23 : 'point3.y', 33 : 'point3.z', 
    39 : 'thickness',
    210 : 'normal.x', 220 : 'normal.y', 230 : 'normal.z', 
    },

'VERTEX'    : {
    10 : 'location.x', 20 : 'location.y', 30 : 'location.z', 
    40 : 'start_width', 41 : 'end_width', 42 : 'bulge', 
    50 : 'tangent',
    70 : 'flags',
    71 : 'index1', 72 : 'index2', 73 : 'index3', 74 : 'index4', 
    },

'VIEWPORT'    : {
    10 : 'center.x', 20 : 'center.y', 30 : 'center.z', 
    12 : 'view_center.x', 22 : 'view_center.y', 32 : 'view_center.z', 
    13 : 'snap_base.x', 23 : 'snap_base.y', 33 : 'snap_base.z', 
    14 : 'snap_spacing.x', 24 : 'snap_spacing.y', 34 : 'snap_spacing.z', 
    15 : 'grid_spacing.x', 25 : 'grid_spacing.y', 35 : 'grid_spacing.z', 
    16 : 'view_direction.x', 26 : 'view_direction.y', 36 : 'view_direction.z', 
    40 : 'width', 41 : 'height',
    68 : 'status', 69 : 'id',
    },

'WIPEOUT'    : {
    10 : 'point.x', 20 : 'point.y', 30 : 'point.z', 
    11 : 'direction.x', 21 : 'direction.y', 31 : 'direction.z', 
    },

}


#
#    Flags
#

# Polyline flags
PL_CLOSED         = 0x01
PL_CURVE_FIT_VERTS    = 0x02
PL_SPLINE_FIT_VERTS    = 0x04
PL_3D_POLYLINE        = 0x08
PL_3D_POLYGON_MESH    = 0x10
PL_CLOSED_IN_N_DIR    = 0x20
PL_POLYFACE_MESH    = 0x40
PL_CONTINUOUS        = 0x80


# Vertex flags
VX_EXTRA_FLAG_CREATED        = 0x01
VX_CURVE_FIT_TANGENT_DEFINED    = 0x02
VX_SPLINE_VERTEX_CREATED    = 0x08
VX_SPLINE_FRAME_CONTROL_POINT    = 0x10
VX_3D_POLYLINE_VERTEX        = 0x20
VX_3D_POLYGON_MESH_VERTEX    = 0x40
VX_POLYFACE_MESH_VERTEX        = 0x80

# 3DFACE flags

F3D_EDGE0_INVISIBLE = 0x01
F3D_EDGE1_INVISIBLE = 0x02
F3D_EDGE2_INVISIBLE = 0x04
F3D_EDGE3_INVISIBLE = 0x08
