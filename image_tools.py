import numpy as np
from PIL import Image, ImageDraw
from concorde.tsp import TSPSolver


def load_image(file: str):
    im = Image.open(file).convert('L')
    return im


def image_to_array(img):
    return np.asarray(img)


def array_to_image(arr):
    return Image.fromarray(np.uint8(arr))


def image_to_tsp_nodes(img):
    arr = image_to_array(img)
    points = np.argwhere(arr == 0)
    return points


def get_header(f, name, dim):
    lines = ["NAME: %s\n" % name, "TYPE: TSP\n", "DIMENSION: %i\n" % dim, "EDGE_WEIGHT_TYPE: EUC_2D\n",
             "NODE_COORD_SECTION\n"]
    return lines


def parse_to_tsp_file(input_folder, name):
    img = load_image(input_folder + name)
    nodes = image_to_tsp_nodes(img)
    with open(input_folder + name.split('.')[0] + ".tsp", 'w') as f:
        lines = get_header(f, name, len(nodes))
        lines += ["%i %i %i\n" % (i, point[0], point[1]) for i, point in enumerate(nodes)]
        f.writelines(lines)
    return img, nodes


def solve_tsp(input_folder, output_folder, name):
    solver = TSPSolver.from_tspfile(input_folder + name)
    solution = solver.solve()
    with open(output_folder + name.split('.')[0] +'.txt', 'w') as f:
        f.write(str(solution.tour))
    return solution


def image_to_tsp_routed():
    input_folder = 'input/'
    output_folder = 'output/'
    name = 'beeg.jpg'
    img, nodes = parse_to_tsp_file(input_folder, name)
    solution = solve_tsp(input_folder, output_folder, name.split('.')[0] + '.tsp').tour
    solution += solution[0]
    draw = ImageDraw.Draw(img)
    for i, node in enumerate(solution[:-1]):
        node1 = nodes[node]
        node2 = nodes[solution[i+1]]
        draw.line((node1[0], node1[1], node2[0], node2[1]), fill=128)
    img.save(output_folder + name.split('.')[0] + '.jpg')



#def draw_tsp_route()


image_to_tsp_routed()

# input_folder = 'images/input/'
# output_folder = 'images/output/'
# name = 'adam2battleroyale.png'
# k = 3072
# iterations = 10000
# im_arr = image_to_array(load_image(input_folder + name))
# output_img = array_to_image(im_arr)
# output_img = array_to_image(tractor_beam(im_arr, k=k, iterations=iterations))
# output_img.save(output_folder+name)
