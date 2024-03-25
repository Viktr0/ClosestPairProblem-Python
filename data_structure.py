import numpy as np


class Points:
    """
    Data structure for storing multidimensional points.
    """

    def __init__(self, data, size, dimension):
        self.data = data
        self.size = size
        self.dim = dimension

    def get_distance(self, index_1, index_2, level=0):
        """
        Calculates the Euclidean distance between two points in the specified dimension.

        :param index_1: index of the first point (integer)
        :param index_2: index of the second point (integer)
        :param level: specifies how many dimensions lower (integer)
        :return: distance (float)
        """
        p1 = np.array(self.get_by_index(index_1, level))
        p2 = np.array(self.get_by_index(index_2, level))

        return np.linalg.norm(p1 - p2)

    def get_by_index(self, index, level=0):
        """
        Return a numpy array of the point with the specified index.
        It can be in a lower dimension based on the level.

        :param index: the index of the point (integer)
        :param level: specifies how many dimensions lower (integer)
        :return: point (numpy.array)
        """
        return self.data[index * self.dim + level: (index + 1) * self.dim]

    def sort_indices_by_coord(self, indices, coordinate=0):
        """
        Sorts the points with the specified index based on the specified coordinate.

        :param indices: indices of the points that should be sorted (list)
        :param coordinate: the coordinate that the sorting is based on (integer)
        :return: sorted indices (list)
        """
        n = len(indices)
        if n == 0:
            return []

        # Creating index and the specified coordinate pairs then sorting them by the values of the coordinates.
        tuples = []
        for i in range(0, n):
            i_ind = indices[i]
            tuples.append((i_ind, self.get_by_index(i_ind)[coordinate]))
        sorted_tuples = sorted(tuples, key=lambda t: t[1])

        # Getting the sorted indices.
        sorted_indices = []
        for i in range(0, n):
            sorted_indices.append(sorted_tuples[i][0])

        return sorted_indices
