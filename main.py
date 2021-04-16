from dot_connector.connector import create_tsp_art
from dot_connector.solution_handler import get_size_of_image
from image_tools import image_to_array, load_image
from stippler import define_arguments, main as stippling_main
from tsp_solving import main as solving_main
#from dot_connector.connector import create_tsp_art


"""
def solve_tsp_problem_and_create_art(input_folder, output_folder, name, nodes, size, k):
    solution = solve_tsp(input_folder, name.split('.')[0] + f'_{k}' + '.tsp').tour.tolist()
    # solution.append(solution[0])
    im = create_tsp_art(nodes, solution, size)
    im.save(output_folder + name.split('.')[0] + f'_{k}' + '.jpg')


def image_to_tsp_routed():
    input_folder = 'input/'
    output_folder = 'output/'
    name = 'pepe_cut_smol.jpg'
    k = 4096
    iterations = 200000
    im_arr = image_to_array(load_image(input_folder + name))
    # output_img = array_to_image(im_arr)
    output_img = create_dotted_array(tractor_beam(im_arr, k=k, iterations=iterations)[0], im_arr.shape)
    array_to_image(output_img).save(output_folder + f"dotted_{k}_{iterations}_" + name)
    img, nodes = parse_to_tsp_file(input_folder, name.split('.')[0] + '.jpg', array_to_tsp_nodes(output_img), k)
    solve_tsp_problem_and_create_art(input_folder, output_folder, name, nodes, img.size, k)
"""


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
    output_directory: str = parsed_args.out_dir + filename_no_postfix + "_" + str(k) + '/'  # for all output
    solution = solving_main(output_directory + filename_no_postfix + '_' + str(k) + '.tsp')
    if parsed_args.thickness:
        im_arr = image_to_array(load_image(parsed_args.input_file))
        shape = im_arr.T.shape
    else:
        im_arr = None
        shape = get_size_of_image(nodes)
    print(shape)
    create_tsp_art(nodes, solution, shape, im_arr).save(output_directory + filename_no_postfix + "_" + str(k) + ".png")


def deleto():
    # importing image object from PIL
    import math
    from PIL import Image, ImageDraw

    w, h = 220, 190
    shape = [(40, 40), (w - 10, h - 10)]

    # creating new Image object
    img = Image.new("RGB", (w, h))

    # create line image
    img1 = ImageDraw.Draw(img)
    img1.line(shape, width=4)
    img.save("test.png")


if __name__ == "__main__":
    #deleto()
    main(define_arguments_main().parse_args())
    # solve_tsp_problem_and_create_art('input/', 'output/', 'baba.jpg', read_tsp_file('input/baba_40000.tsp'), (251,356), 40000)
    # image_to_tsp_routed()
# create_tsp_art_from_partial_solutions("input/jesus_close_4096.tsp", (169, 210))
