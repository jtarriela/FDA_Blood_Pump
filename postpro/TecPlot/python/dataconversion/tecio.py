import ctypes
import numpy as np
import sys

tecio = ctypes.cdll.LoadLibrary(r"C:\Program Files\Tecplot\Tecplot 360 EX Beta\bin\tecio.dll")

# Constants
VALUELOCATION_CELLCENTERED = 0
VALUELOCATION_NODECENTERED = 1

VARSTATUS_ACTIVE  = 0
VARSTATUS_PASSIVE = 1

ZONETYPE_ORDERED = 0
ZONETYPE_FELINESEG = 1
ZONETYPE_FETRIANGLE = 2
ZONETYPE_FEQUADRILATERAL = 3
ZONETYPE_FETETRAHEDRON = 4
ZONETYPE_FEBRICK = 5
ZONETYPE_FEPOLYGON = 6
ZONETYPE_FEPOLYHEDRON = 7

FILETYPE_GRIDANDSOLUTION = 0
FILETYPE_GRID = 1
FILETYPE_SOLUTION = 2

def open_file(
    file_name,
    dataset_title,
    var_names,
    use_double_precision=False,
    file_type=FILETYPE_GRIDANDSOLUTION):

    tecio.tecini142.restype=ctypes.c_int32
    tecio.tecini142.argtypes=(
            ctypes.c_char_p, #Title
            ctypes.c_char_p, #Variables
            ctypes.c_char_p, #FName
            ctypes.c_char_p, #ScratchDir
            ctypes.POINTER(ctypes.c_int32), # FileFormat
            ctypes.POINTER(ctypes.c_int32), # FileType
            ctypes.POINTER(ctypes.c_int32), #Debug
            ctypes.POINTER(ctypes.c_int32)) #IsDouble

    is_szl = True if file_name.endswith(".szplt") else False

    varnamelist = ",".join(var_names)
    scratch_dir = r"."
    fileformat = ctypes.c_int32(1 if is_szl else 0) # 0=PLT, 1=SZL
    filetype = ctypes.c_int32(file_type) # 0=Grid&Solution, 1=Grid, 2=Solution
    debug = ctypes.c_int32(0) # 0=No, 1=Yes
    isdouble = ctypes.c_int32(1 if use_double_precision else 0) # 0=float, 1=double
    ret = tecio.tecini142(
            ctypes.c_char_p(bytes(dataset_title, encoding="UTF-8")),
            ctypes.c_char_p(bytes(varnamelist, encoding="UTF-8")),
            ctypes.c_char_p(bytes(file_name, encoding="UTF-8")),
            ctypes.c_char_p(bytes(scratch_dir, encoding="UTF-8")),
            ctypes.byref(fileformat),
            ctypes.byref(filetype),
            ctypes.byref(debug),
            ctypes.byref(isdouble)
            )
    if ret != 0:
        raise Exception("open_file Error")
    return ret


def close_file():
    tecio.tecend142.restype=ctypes.c_int32
    #tecio.tecend142.argtypes=(,)

    ret = tecio.tecend142()
    if ret != 0:
        raise Exception("close_file Error")
    return ret

def teczne(
    zone_name,
    zone_type,
    imax,
    jmax,
    kmax,
    solution_time = 0,
    strand = 0,
    parent_zone = 0,
    num_face_connections = 0,
    face_neighbor_mode = 0,
    total_num_face_nodes = 0,
    num_connected_boundary_faces = int(0),
    total_num_boundary_connections = int(0),
    var_sharing = None,
    passive_vars = None,
    value_locations = None):

    tecio.teczne142.restype=ctypes.c_int32
    tecio.teczne142.argtypes=(
            ctypes.c_char_p, # ZoneTitle
            ctypes.POINTER(ctypes.c_int32), # ZoneType
            ctypes.POINTER(ctypes.c_int32), # IMax
            ctypes.POINTER(ctypes.c_int32), # JMax
            ctypes.POINTER(ctypes.c_int32), # KMax
            ctypes.POINTER(ctypes.c_int32), # ICellMax
            ctypes.POINTER(ctypes.c_int32), # JCellMax
            ctypes.POINTER(ctypes.c_int32), # KCellMax
            ctypes.POINTER(ctypes.c_double), # SolutionTime
            ctypes.POINTER(ctypes.c_int32), # StrandID
            ctypes.POINTER(ctypes.c_int32), # ParentZone
            ctypes.POINTER(ctypes.c_int32), # IsBlock
            ctypes.POINTER(ctypes.c_int32), # NumFaceConnections
            ctypes.POINTER(ctypes.c_int32), # FaceNeighborMode
            ctypes.POINTER(ctypes.c_int32), # TotalNumFaceNodes
            ctypes.POINTER(ctypes.c_int32), # NumConnectedBoundaryFaces
            ctypes.POINTER(ctypes.c_int32), # TotalNumBoundaryConnections
            ctypes.POINTER(ctypes.c_int32), # PassiveVarList
            ctypes.POINTER(ctypes.c_int32), # ValueLocation
            ctypes.POINTER(ctypes.c_int32), # ShareVarFromZone
            ctypes.POINTER(ctypes.c_int32)) # ShareConnectivityFromZone

    zone_type = ctypes.c_int32(zone_type)
    imax = ctypes.c_int32(imax)
    jmax = ctypes.c_int32(jmax)
    kmax = ctypes.c_int32(kmax)
    parent_zone = ctypes.c_int32(parent_zone)
    ignored = ctypes.c_int32(0)
    block_format = ctypes.c_int32(1)
    num_face_connections = ctypes.c_int32(num_face_connections)
    face_neighbor_mode = ctypes.c_int32(face_neighbor_mode)
    total_num_face_nodes = ctypes.c_int32(total_num_face_nodes)
    num_connected_boundary_faces = ctypes.c_int32(num_connected_boundary_faces)
    total_num_boundary_connections = ctypes.c_int32(total_num_boundary_connections)

    passive_var_list = None
    if passive_vars:
        passive_var_list = (ctypes.c_int32*len(passive_vars))(*passive_vars)
    var_share_list = None
    if var_sharing:
        var_share_list = (ctypes.c_int32*len(var_sharing))(*var_sharing)
    value_location_list = None
    if value_locations:
        value_location_list = (ctypes.c_int32*len(value_locations))(*value_locations)

    ret = tecio.teczne142(
            ctypes.c_char_p(bytes(zone_name, encoding="UTF-8")),
            ctypes.byref(zone_type),
            ctypes.byref(imax),
            ctypes.byref(jmax),
            ctypes.byref(kmax),
            ctypes.byref(ignored),
            ctypes.byref(ignored),
            ctypes.byref(ignored),
            ctypes.byref(ctypes.c_double(solution_time)),
            ctypes.byref(ctypes.c_int32(strand)),
            ctypes.byref(parent_zone),
            ctypes.byref(block_format),
            ctypes.byref(num_face_connections),
            ctypes.byref(face_neighbor_mode),
            ctypes.byref(total_num_face_nodes), # only applies to poly data
            ctypes.byref(num_connected_boundary_faces), # only applies to poly data
            ctypes.byref(total_num_boundary_connections), # only applies to poly data
            passive_var_list,
            value_location_list,
            var_share_list,
            ctypes.byref(ctypes.c_int32(0))) #ShareConnectivityFromZone
    return ret

def create_ordered_zone(
    zone_name,
    shape,
    solution_time=0,
    strand=0,
    var_sharing=None,
    passive_vars=None,
    value_locations=None):

    zone_type = ZONETYPE_ORDERED
    imax,jmax,kmax = shape

    ret = teczne(
            zone_name = zone_name,
            zone_type = zone_type,
            imax=shape[0],
            jmax=shape[1],
            kmax=shape[2],
            solution_time = solution_time,
            strand = strand,
            var_sharing = var_sharing,
            passive_vars = passive_vars,
            value_locations = value_locations)
    if ret != 0:
        raise Exception("create_ordered_zone Error")
    return ret

def create_poly_zone(
    zone_name,
    zone_type,
    num_nodes,
    num_elements,
    num_faces,
    total_num_face_nodes,
    num_connected_boundary_faces=0,
    total_num_boundary_connections=0,
    solution_time=0,
    strand=0,
    var_sharing=None,
    passive_vars=None,
    value_locations=None):

    assert(zone_type == ZONETYPE_FEPOLYGON or zone_type == ZONETYPE_FEPOLYHEDRON)
    ret = teczne(
            zone_name = zone_name,
            zone_type = zone_type,
            imax = num_nodes,
            jmax = num_elements,
            kmax = num_faces,
            solution_time = solution_time,
            strand = strand,
            total_num_face_nodes = total_num_face_nodes,
            num_connected_boundary_faces = num_connected_boundary_faces,
            total_num_boundary_connections = total_num_boundary_connections,
            var_sharing = var_sharing,
            passive_vars = passive_vars,
            value_locations = value_locations)
    if ret != 0:
        raise Exception("create_poly_zone Error")
    return ret

def tecpolyface(num_faces, face_node_counts, face_nodes, face_left_elems, face_right_elems):
    tecio.tecpolyface142.restype=ctypes.c_int32
    tecio.tecpolyface142.argtypes=(
            ctypes.POINTER(ctypes.c_int32), # NumFaces
            ctypes.POINTER(ctypes.c_int32), # FaceNodeCounts array
            ctypes.POINTER(ctypes.c_int32), # FaceNodes array
            ctypes.POINTER(ctypes.c_int32), # Face Left Elems array
            ctypes.POINTER(ctypes.c_int32)) # Face Right Elems array

    face_node_count_array = None
    if face_node_counts:
        face_node_counts = np.asarray(face_node_counts,dtype=np.int32)
        face_node_count_array = ctypes.cast(face_node_counts.ctypes.data, ctypes.POINTER(ctypes.c_int32))

    face_nodes = np.asarray(face_nodes,dtype=np.int32)
    face_left_elems = np.asarray(face_left_elems,dtype=np.int32)
    face_right_elems = np.asarray(face_right_elems,dtype=np.int32)
    ret = tecio.tecpolyface142(
            ctypes.byref(ctypes.c_int32(num_faces)),
            face_node_count_array, #ctypes.cast(face_node_counts.ctypes.data, ctypes.POINTER(ctypes.c_int32)),
            ctypes.cast(face_nodes.ctypes.data, ctypes.POINTER(ctypes.c_int32)),
            ctypes.cast(face_left_elems.ctypes.data, ctypes.POINTER(ctypes.c_int32)),
            ctypes.cast(face_right_elems.ctypes.data, ctypes.POINTER(ctypes.c_int32)))
    if ret != 0:
        raise Exception("tecpolyface Error")

def __zone_write_double_values(values):
    values = np.asarray(values.ravel(),dtype=np.float64)
    tecio.tecdat142.restype=ctypes.c_int32
    tecio.tecdat142.argtypes=(
            ctypes.POINTER(ctypes.c_int32), # NumPts
            ctypes.POINTER(ctypes.c_double), #values
            ctypes.POINTER(ctypes.c_int32)) #isdouble 

    isdouble = ctypes.c_int32(1)
    ret = tecio.tecdat142(
            ctypes.byref(ctypes.c_int32(len(values))),
            ctypes.cast(values.ctypes.data, ctypes.POINTER(ctypes.c_double)),
            ctypes.byref(isdouble))
    if ret != 0:
        raise Exception("zone_write_double_values Error")

def __zone_write_float_values(values):
    values = np.asarray(values.ravel(),dtype=np.float32)
    tecio.tecdat142.restype=ctypes.c_int32
    tecio.tecdat142.argtypes=(
            ctypes.POINTER(ctypes.c_int32), # NumPts
            ctypes.POINTER(ctypes.c_float), #values
            ctypes.POINTER(ctypes.c_int32)) #isdouble 

    isdouble = ctypes.c_int32(0)
    ret = tecio.tecdat142(
            ctypes.byref(ctypes.c_int32(values.size)),
            ctypes.cast(values.ctypes.data, ctypes.POINTER(ctypes.c_float)),
            ctypes.byref(isdouble))
    if ret != 0:
        raise Exception("zone_write_float_values Error")

def zone_write_values(values):
    values = np.asarray(values)
    if values.dtype == np.float64:
        return __zone_write_double_values(values)
    else:
        return __zone_write_float_values(values)

def test_ordered(file_name, use_double):
    open_file(file_name, "Title", ['x','y','c'], use_double)
    value_locations = [
        VALUELOCATION_NODECENTERED, # 'x'
        VALUELOCATION_NODECENTERED, # 'y'
        VALUELOCATION_CELLCENTERED] # 'c'
    # Use default values for non-positional arguments (like strand, solution_time, etc)
    create_ordered_zone("Zone", (3,3,1), value_locations=value_locations)
    zone_write_values([1,2,3,1,2,3,1,2,3]) #xvals
    zone_write_values([1,1,1,2,2,2,3,3,3]) #yvals
    # 3x3 zone has 4 elements
    zone_write_values([1,2,3,4]) #cvals
    close_file()
    
def test_polygon(file_name, use_double):
    open_file(file_name, "Title", ['x','y','c'], use_double)

    # Create two triangle polygon cells
    num_nodes = 4
    num_elements = 2
    num_faces = 5
    total_num_face_nodes = 2 * num_faces
    
    value_locations = [
        VALUELOCATION_NODECENTERED, # 'x'
        VALUELOCATION_NODECENTERED, # 'y'
        VALUELOCATION_CELLCENTERED] # 'c'

    create_poly_zone(
        "Zone", #zone_name
        ZONETYPE_FEPOLYGON,
        num_nodes,
        num_elements,
        num_faces,
        total_num_face_nodes,
        value_locations=value_locations) # value_locations
    
    zone_pts = [
        0,0,    # cell 1
        1,0,    # cell 1 & 2
        0.5,1,  # cell 1 & 2
        1.5,0.5]# cell 2

    x_pts = zone_pts[0::2]
    y_pts = zone_pts[1::2]
    zone_write_values(x_pts)
    zone_write_values(y_pts)
    zone_write_values([1,2]) # 'c' has two cell centered values

    face_nodes = [
        2,1, # Face 1
        1,3, # Face 2
        3,2, # Face 3
        3,4, # Face 4
        4,2, # Face 5
    ]
    assert(len(face_nodes) == total_num_face_nodes)

    left_elems = [0,0,2,0,0]
    right_elems = [1,1,1,2,2]
    # Negative values in the element arrays indicate a connection to an element in another zone
    tecpolyface(num_faces, None, face_nodes, left_elems, right_elems)
    close_file()

def test_polyhedron(file_name, use_double):
    open_file(file_name, "Title", ['x','y','z','c'], use_double)

    # Create a brick-like polyhedral zone 
    num_nodes = 8
    num_elements = 1
    num_faces = 6
    total_num_face_nodes = 24 # 6 faces with 4 nodes per face
    face_node_counts = [4] * 6 # 6 faces with 4 nodes per face
    assert(len(face_node_counts) == num_faces)
    
    value_locations = [
        VALUELOCATION_NODECENTERED, # 'x'
        VALUELOCATION_NODECENTERED, # 'y'
        VALUELOCATION_NODECENTERED, # 'z'
        VALUELOCATION_CELLCENTERED] # 'c'

    create_poly_zone(
        "Zone", #zone_name
        ZONETYPE_FEPOLYHEDRON,
        num_nodes,
        num_elements,
        num_faces,
        total_num_face_nodes,
        value_locations=value_locations) # value_locations
    
    rect_pts = [
        0,3,0, # XYZ
        3,3,0, # XYZ
        3,1,0, # XYZ
        0,1,0, # XYZ
        0,3,1, # XYZ
        3,3,1, # XYZ
        3,1,1, # XYZ
        0,1,1] # XYZ
    x_pts = rect_pts[0::3]
    y_pts = rect_pts[1::3]
    z_pts = rect_pts[2::3]
    zone_write_values(x_pts)
    zone_write_values(y_pts)
    zone_write_values(z_pts)
    zone_write_values([3]) # 'c' has only one cell centered value

    face_nodes = [
        1,2,3,4, # Face 1
        1,4,8,5, # Face 2
        5,8,7,6, # Face 3
        2,6,7,3, # Face 4
        6,2,1,5, # Face 5
        3,7,8,4, # Face 6
    ]
    assert(len(face_nodes) == total_num_face_nodes)

    left_elems = [0] * num_faces
    right_elems = [1] * num_faces
    # Negative values in the element arrays indicate a connection to an element in another zone
    tecpolyface(num_faces, face_node_counts, face_nodes, left_elems, right_elems)
        
    close_file()

def test_gridandsolution(grid_file, solution_file):
    open_file(grid_file, "Title", ['x','y'], file_type = FILETYPE_GRID)
    value_locations = [
        VALUELOCATION_NODECENTERED, # 'x'
        VALUELOCATION_NODECENTERED] # 'y'
    create_ordered_zone("Zone", (3,3,1), strand=1, value_locations=value_locations)
    zone_write_values([1,2,3,1,2,3,1,2,3]) #xvals
    zone_write_values([1,1,1,2,2,2,3,3,3]) #yvals
    close_file()

    for t in [1,2,3]:
        open_file("t={}_{}".format(t, solution_file), "Title", ['c'], file_type=FILETYPE_SOLUTION)
        value_locations = [VALUELOCATION_CELLCENTERED] # 'c'
        create_ordered_zone("Zone", (3,3,1), solution_time=t, strand=1, value_locations=value_locations)
        zone_write_values([t*1,t*2,t*3,t*4]) #cvals
        close_file()

if "--testgridandsolution" in sys.argv:
    test_gridandsolution("grid.plt", "solution.plt")
    test_gridandsolution("grid.szplt", "solution.szplt")

if "--testpolygon" in sys.argv:
    test_polygon("test_polygon.plt", False)

if "--testpolyhedron" in sys.argv:
    test_polyhedron("test_polyhedron.plt", False)

if "--testordered" in sys.argv:
    test_ordered("test_ordered_double.plt", True)
    test_ordered("test_ordered_float.plt", False)
    test_ordered("test_ordered_double.szplt", True)
    test_ordered("test_ordered_float.szplt", False)
