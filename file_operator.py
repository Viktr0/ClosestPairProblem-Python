import csv

from data_structure import Points


class FileOperator:
    """
    Reads in multidimensional points from tsv file and writes the closest pairs to txt file.
    """

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def read_points(self):
        """
        Reads multidimensional points from tsv file and creates a Points object.

        :return: points object (Points)
        """
        points = []
        with open(self.input_path, 'r') as file:
            tsv_reader = csv.reader(file, delimiter='\t')
            row_counter = 0
            for row in tsv_reader:
                row_counter += 1
                for coord in row:
                    points.append(float(coord))
            dimension = len(points) // row_counter

        return Points(points, row_counter, dimension)

    def write_closest_pair(self, pair1, pair2):
        """
        Writes the closest pair to the output file in the desired representation.

        :param pair1: the index and the coordinates of the first element in the pair (tuple)
        :param pair2: the index and the coordinates of the second element in the pair (tuple)
        :return -
        """
        dim = len(pair1[1])
        output = f'{pair1[0] + 1}:{round(pair1[1][0], 1)}'
        for i in range(1, dim):
            output += f'\t{round(pair1[1][i], 1)}'
        output += f'\n{pair2[0] + 1}:{round(pair2[1][0], 1)}'
        for i in range(1, dim):
            output += f'\t{round(pair2[1][i], 1)}'

        with open(self.output_path, "w") as file:
            file.write(output)
