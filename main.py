from connector import create_tsp_art
from image_tools import image_to_array, load_image
from solution_handler import get_size_of_image
from stippler import define_arguments, main as stippling_main
from tsp_solving import main as solving_main


def define_arguments_main():
    parser = define_arguments()
    parser.add_argument("--thickness", action="store_true",
                        help="Use modified algorithm for using edge thickness if specified")

    return parser


def main(parsed_args):
    nodes = stippling_main(parsed_args)
    filename = parsed_args.input_file.split('/')[-1]
    filename_no_postfix = filename.split('.')[0]
    k = parsed_args.k
    darkness: bool = parsed_args.darkness
    output_directory: str = parsed_args.out_dir + filename_no_postfix + "_" + str(k) + '/'  # for all output
    solution = solving_main(output_directory + filename_no_postfix + '_' + str(k) + '.tsp')
    if parsed_args.thickness:
        im_arr = image_to_array(load_image(parsed_args.input_file))
        shape = im_arr.T.shape
    else:
        im_arr = None
        shape = get_size_of_image(nodes)
    create_tsp_art(nodes, solution, shape, im_arr, darkness).save(
        output_directory + filename_no_postfix + "_" + str(k) + ".png")


if __name__ == "__main__":
    main(define_arguments_main().parse_args())
