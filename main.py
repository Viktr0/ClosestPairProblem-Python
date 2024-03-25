from closest_pair_problem import ClosestPair
from file_operator import FileOperator


def closest_pair_problem(input_file, output_file):
    """
    Calculates and writes the closest pair of multidimensional points.

    :param input_file: Path of the tsv file that contains the points.
    :param output_file: Path of the output file contains the line numbers and the coordinates of the two closest points.
    """
    fo = FileOperator(input_file, output_file)
    points = fo.read_points()

    cp = ClosestPair(points)
    index1, index2, distance = cp.get_closest_pair()

    if index1 < index2:
        pair1 = (index1, points.get_by_index(index1))
        pair2 = (index2, points.get_by_index(index2))
    else:
        pair2 = (index1, points.get_by_index(index1))
        pair1 = (index2, points.get_by_index(index2))

    fo.write_closest_pair(pair1, pair2)


if __name__ == '__main__':
    input_path = 'venv\\Data\\sample_input_100_100.tsv'
    output_path = 'venv\\Data\\results.txt'

    closest_pair_problem(input_path, output_path)
