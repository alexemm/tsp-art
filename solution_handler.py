from argparse import ArgumentParser
from operator import itemgetter
from os import listdir, makedirs
from typing import List, Optional, Tuple

from connector import create_tsp_art
from image_tools import load_image, image_to_array
from tsp_solving import read_tsp_file


def get_size_of_image(nodes: List[Tuple[int, int]]):
    return max(nodes, key=itemgetter(0))[0], max(nodes, key=itemgetter(1))[1]


def create_tsp_art_from_partial_solutions(tsp_file: str, im_file: Optional[str], darkness: bool = False) -> None:
    nodes = read_tsp_file(tsp_file)
    if im_file is not None:
        im_arr = image_to_array(load_image(im_file))
        size = im_arr.T.shape
    else:
        im_arr = None
        size = get_size_of_image(nodes)
    output_dir: str = f"{'/'.join(tsp_file.split('/')[:-1])}/nonoptimal_solutions/"
    try:
        makedirs(output_dir)
    except FileExistsError:
        pass
    for i, sol in enumerate(get_solution_files_of_tsp('.')):
        print(f"Solution {i}")
        create_tsp_art(nodes, read_solution_file(sol), size, im_arr, darkness).save(output_dir + f'{i}' + '.jpg')


def get_solution_files_of_tsp(directory) -> List[str]:
    return [file for file in listdir(directory) if file.split(".")[-1] == 'sol']


def read_solution_file(file_name: str, skiph: int = 1) -> List[int]:
    with open(file_name) as f:
        return [int(entry) for line in f.read().splitlines()[skiph:] for entry in line.split(" ") if entry != '']


def define_arguments():
    parser = ArgumentParser()
    parser.add_argument("tsp_file", help="TSP file with .tsp ending")
    parser.add_argument("-im", "--image", help="Image for modified line thickness")
    parser.add_argument("--non_optimal", help="Look for non-optimal solution", action="store_true")
    parser.add_argument("--darkness", help="Option for drawing white lines on black background", action="store_true")
    return parser


def main(parsed_arguments):
    create_tsp_art_from_partial_solutions(parsed_arguments.tsp_file, parsed_arguments.image, parsed_arguments.darkness)


if __name__ == "__main__":
    main(define_arguments().parse_args())
