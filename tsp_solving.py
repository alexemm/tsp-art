from typing import List, Tuple, Iterable, AnyStr
from argparse import ArgumentParser

from concorde.tsp import TSPSolver


def read_tsp_file(file: str, skiph: int = 5) -> List[Tuple[int, int]]:
    with open(file) as f:
        return [(int(line.split(" ")[1]), int(line.split(" ")[2])) for line in f.read().splitlines()[skiph:]]


def solve_tsp(file: str):
    solver = TSPSolver.from_tspfile(file)
    solution = solver.solve()
    return solution


def parse_tsp_file_name():
    parser = ArgumentParser()
    parser.add_argument("tsp_file", help="Location to tsp file to solve")
    return parser


def write_solution_file(solution: Iterable[AnyStr], file: str):
    with open(file, 'w') as f:
        f.writelines([str(len(solution)) + '\n'] + [str(x) + '\n' for x in solution])


def main(tsp_file: str):
    solution = solve_tsp(tsp_file)
    solution_file_name = '.'.join(tsp_file.split('.')[:-1]) + '.sol'
    write_solution_file(solution.tour, solution_file_name)
    return solution.tour


if __name__ == "__main__":
    main(parse_tsp_file_name().parse_args().tsp_file)
