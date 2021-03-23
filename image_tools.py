from typing import List

import numpy as np
from PIL import Image, ImageDraw
from concorde.tsp import TSPSolver
from dotter.stippler import tractor_beam
from os import listdir


def load_image(file: str):
    im = Image.open(file).convert('L')
    return im


def image_to_array(img):
    return np.asarray(img)


def array_to_image(arr):
    return Image.fromarray(np.uint8(arr))


def array_to_tsp_nodes(arr):
    #arr = image_to_array(img)
    points = np.argwhere(arr == 0)
    return points


def get_header(f, name, dim):
    lines = ["NAME: %s\n" % name, "TYPE: TSP\n", "DIMENSION: %i\n" % dim, "EDGE_WEIGHT_TYPE: EUC_2D\n",
             "NODE_COORD_SECTION\n"]
    return lines


def parse_to_tsp_file(input_folder, name, nodes):
    print(nodes)
    img = load_image(input_folder + name)
    #nodes = image_to_tsp_nodes(img)
    with open(input_folder + name.split('.')[0] + ".tsp", 'w') as f:
        lines = get_header(f, name, len(nodes))
        lines += ["%i %i %i\n" % (i, point[0], point[1]) for i, point in enumerate(nodes)]
        f.writelines(lines)
    return img, nodes


def solve_tsp(input_folder, name):
    solver = TSPSolver.from_tspfile(input_folder + name)
    solution = solver.solve()
    #with open(output_folder + name.split('.')[0] +'.txt', 'w') as f:
    #    f.write(str(solution.tour))
    return solution


def read_solution_file(file_name: str) -> List[int]:
    pass


def get_solution_files_of_tsp(directory) -> List[str]:
    return [file for file in listdir(directory) if file.split(".")[-1] == '.sol']


def create_tsp_art(nodes, solution_tour, size) -> Image:
    im = Image.new('RGB', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)
    for i, node in enumerate(solution_tour[:-1]):
        node1 = nodes[node]
        node2 = nodes[solution_tour[i + 1]]
        draw.line((node1[1], node1[0], node2[1], node2[0]), fill=128)
    return im


def create_tsp_art_from_partial_solutions() -> None:
    for i, sol in enumerate(get_solution_files_of_tsp('')):
        pass


def image_to_tsp_routed():
    input_folder = 'input/'
    output_folder = 'output/'
    name = 'jesus_close.jpg'
    k = 4096
    iterations = 10000
    im_arr = image_to_array(load_image(input_folder + name))
    # output_img = array_to_image(im_arr)
    output_img = tractor_beam(im_arr, k=k, iterations=iterations)
    array_to_image(output_img).save(output_folder + "dotted_" + name)
    img, nodes = parse_to_tsp_file(input_folder, name, array_to_tsp_nodes(output_img))
    solution = solve_tsp(input_folder, name.split('.')[0] + '.tsp').tour.tolist()
    solution.append(solution[0])
    im = create_tsp_art(img.size)
    im.save(output_folder + name.split('.')[0] + '.jpg')


image_to_tsp_routed()
