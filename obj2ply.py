import sys
from typing import List, TextIO, Tuple


def parse(lines:List[str]) -> Tuple[List[Tuple[float]], List[Tuple[int]], List[Tuple[int]]]:
    vertices: List[Tuple[float]] = []
    colors: List[Tuple[int]] = []
    faces: List[Tuple[int]] = []
    for line in lines:
        parts = line.split()
        if len(parts) == 0:
            continue
        if parts[0] == 'v':
            vertices.append(tuple(float(coord) for coord in parts[1:4]))
            colors.append(tuple(int(255*chan) for chan in map(float, parts[4:7])))
        if parts[0] == 'f':
            faces.append(tuple(int(vert)-1 for vert in parts[1:4]))
    return vertices, colors, faces


def validate(vertices:List[Tuple[float]], colors:List[Tuple[int]], faces:List[Tuple[int]]) -> None:
    # print("vertices:", type(vertices), len(vertices), type(vertices[0]), len(vertices[0]), type(vertices[0][0]))
    # print("colors:", type(colors), len(colors), type(colors[0]), len(colors[0]), type(colors[0][0]))
    # print("faces:", type(faces), len(faces), type(faces[0]), len(faces[0]), type(faces[0][0]))
    # TODO: validate
    pass

def optimize(vertices:List[Tuple[float]], colors:List[Tuple[int]], faces:List[Tuple[int]]) -> Tuple[List[Tuple[float]], List[Tuple[int]], List[Tuple[int]]]:
    # vertex_count_before = len(vertices)
    # color_count_before = len(colors)
    # face_count_before = len(faces)
    vertex_replacements = {}
    unique_vertices = {}
    for i, vertex in enumerate(vertices):
        if str(vertex) not in unique_vertices:
            unique_vertices[str(vertex)] = i
        else:
            vertex_replacements[i] = unique_vertices[str(vertex)]
    vertices = [vertices[i] for i in range(len(vertices)) if i not in vertex_replacements]
    colors = [colors[i] for i in range(len(colors)) if i not in vertex_replacements]
    for i, face in enumerate(faces):
        faces[i] = tuple(vertex_replacements[vertex] if vertex in vertex_replacements else vertex for vertex in face)

    faces = list(set(faces))
    
    all_indices = set()
    for face in faces:
        for index in face:
            all_indices.add(index)
    all_indices = list(sorted(all_indices))

    index_lookup = {}
    for face in faces:
        for index in face:
            if index not in index_lookup:
                index_lookup[index] = all_indices.index(index)

    vertices = [vertices[i] for i in all_indices]
    colors = [colors[i] for i in all_indices]
    faces = [tuple(index_lookup[index] for index in face) for face in faces]
    
    # vertex_count_after = len(vertices)
    # color_count_after = len(colors)
    # face_count_after = len(faces)
    # print(f'optimized {vertex_count_before} vertices to {vertex_count_after} vertices')
    # print(f'optimized {color_count_before} colors to {color_count_after} colors')
    # print(f'optimized {face_count_before} faces to {face_count_after} faces')
    return vertices, colors, faces


def to_ply(vertices:List[Tuple[float]], colors:List[Tuple[int]], faces:List[Tuple[int]], f:TextIO=sys.stdout) -> None:
    print('ply', file=f)
    print('format ascii 1.0', file=f)
    print(f'element vertex {len(vertices)}', file=f)
    print('property float x', file=f)
    print('property float y', file=f)
    print('property float z', file=f)
    print('property uchar red', file=f)
    print('property uchar green', file=f)
    print('property uchar blue', file=f)
    print(f'element face {len(faces)}', file=f)
    print('property list uchar int vertex_indices', file=f)
    print('end_header', file=f)

    for vertex, color in zip(vertices, colors):
        print(f'{vertex[0]} {vertex[1]} {vertex[2]} {color[0]} {color[1]} {color[2]}', file=f)

    for face in faces:
        print(f'3 {face[0]} {face[2]} {face[1]}', file=f)


def convert(input_file:str, output_file:str=None) -> None:
    with open(input_file, 'r') as f:
        lines = f.readlines()
    vertices, colors, faces = parse(lines)
    validate(vertices, colors, faces)
    vertices, colors, faces = optimize(vertices, colors, faces)
    if output_file is None:
        to_ply(vertices, colors, faces)
    else:
        with open(output_file, 'w') as f:
            to_ply(vertices, colors, faces, f)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <obj file> <ply file>')
        print(f'    output to stdout: {sys.argv[0]} <obj file>')
        print(f'    output to file:   {sys.argv[0]} <obj file> <ply file>')
        sys.exit(1)
    convert(*sys.argv[1:])