from argparse import ArgumentParser
from collections import OrderedDict
from typing import Optional

import numpy as np
from PIL import ImageDraw, ImageFont

from image_tools import image_to_array, load_image, array_to_image


def get_probability_matrix(arr):
    return (255. - arr) / (255. - arr).sum()


def determine_datapoint_from_int(i, prev_shape):
    x = int(i % prev_shape[1])
    y = int(i / prev_shape[1])
    return x, y


def choose_k_points(prob_arr_2d, k, prev_shape):
    chosen_data_values = np.random.choice(range(prob_arr_2d.size), size=k, p=prob_arr_2d.flatten(), replace=False)
    chosen_data_points = [determine_datapoint_from_int(i, prev_shape) for i in chosen_data_values]
    return chosen_data_points, chosen_data_values


def create_dotted_array(chosen_points, shape):
    dotted_arr = np.zeros(shape) + 255
    for point in chosen_points:
        dotted_arr[point[1], point[0]] = 0
    return dotted_arr


def find_closest_point(p, w):
    distance_to_w = lambda x_1, y_1: np.sqrt((x_1 - w[0]) ** 2 + (y_1 - w[1]) ** 2)
    min_distance = distance_to_w(p[0][0], p[0][1])
    closest_point = 0
    for i, point in enumerate(p):
        if min_distance == 0:
            break
        curr_distance = distance_to_w(point[0], point[1])
        if curr_distance < min_distance:
            closest_point = i
            min_distance = curr_distance
    return closest_point


def tractor_beam(arr, k, iterations: Optional[int] = None, intermediate_steps: Optional[int] = None):
    iterations = iterations or 10000
    intermediate_result_steps = intermediate_steps or (iterations + 1)
    prob_matr = get_probability_matrix(arr)
    prev_shape = prob_matr.shape
    prob_matr = prob_matr.flatten()
    p, values = choose_k_points(prob_matr, k, prev_shape)
    n = np.zeros(len(p))
    intermediates = OrderedDict() if intermediate_steps is not None else None
    for iteration in range(iterations):
        # 1. Select tractor beam point
        w = choose_k_points(prob_matr, 1, prev_shape)[0][0]
        # 2. Find closest point to tractor beam point
        i = find_closest_point(p, w)
        # 3. Increment counter for point
        n[i] += 1
        # 4. Adjust point
        p[i] = int(round(1. / (n[i] + 1.) * w[0] + n[i] / float(n[i] + 1.) * p[i][0])), \
               int(round(1. / (n[i] + 1.) * w[1] + n[i] / float(n[i] + 1.) * p[i][1]))
        # Print iterations
        if iteration % 100 == 0 or iterations / 2 == iteration:
            print(iteration)
        # Store side steps for visualization later
        if iteration % intermediate_result_steps == 0 and intermediate_steps is not None:
            intermediates[iteration] = p.copy()
    intermediates[iterations] = p
    return p, intermediates


def write_tsp_file(output_file, nodes):
    with open(output_file, 'w') as f:
        name: str = output_file.split('/')[-1].split('.')[0]
        lines = get_header(name, len(nodes))
        lines += ["%i %i %i\n" % (i, point[0], point[1]) for i, point in enumerate(nodes)]
        f.writelines(lines)


def get_header(name, dim):
    lines = ["NAME: %s\n" % name, "TYPE: TSP\n", "DIMENSION: %i\n" % dim, "EDGE_WEIGHT_TYPE: EUC_2D\n",
             "NODE_COORD_SECTION\n"]
    return lines


def define_arguments() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("input_file", help="File input")
    parser.add_argument("k", help="Number of dots in image", type=int)
    parser.add_argument("out_dir", help="Output directory")
    parser.add_argument("-it", "--iterations", help="Number of iterations to clean image. Default is 10000", type=int)
    parser.add_argument("-st", "--steps", help="Number of intermediate steps which will be printed in to an image",
                        type=int)
    # parser.add_argument("--seed", help="Random seed")
    return parser


def add_iteration_text_to_corner(im, text):
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 20)
    draw.text((0, 0), text, 0, font=font)
    return im


def create_timelapse_gif(out_name, intermediate_steps, shape):
    im = array_to_image(create_dotted_array(intermediate_steps[0], shape))
    im_arr = [add_iteration_text_to_corner(array_to_image(create_dotted_array(st, shape)), "Iteration: " + str(it)) for
              it, st in intermediate_steps.items()]
    im.save(out_name, save_all=True, append_images=im_arr, loop=0, duration=200)


def stippling(im_arr: np.ndarray, k: int, filename: str, out_dir: str, iterations: Optional[int], steps: Optional[int]):
    nodes, intermediate_nodes = tractor_beam(im_arr, k, iterations, steps)
    # Save picture
    array_to_image(create_dotted_array(nodes, im_arr.shape)).save(out_dir + str(k) + filename)
    # Save tsp-file
    write_tsp_file(out_dir + filename.split('.')[0] + str(k) + '.tsp', nodes)
    # Show all the intermediate steps
    if steps is not None:
        create_timelapse_gif(out_dir + filename.split('.')[0] + '.gif', intermediate_nodes, im_arr.shape)


def main(parsed_arguments):
    args = parsed_arguments
    filename = args.input_file.split('/')[-1]
    im_arr = image_to_array(load_image(args.input_file))
    stippling(im_arr, args.k, filename, args.out_dir, args.iterations, args.steps)


if __name__ == '__main__':
    main(define_arguments().parse_args())