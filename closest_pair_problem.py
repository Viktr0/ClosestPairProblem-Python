import numpy as np
import math

from data_structure import Points


class ClosestPair:
    """
    Algorithm for finding the closest pair of points.
    """

    def __init__(self, points_obj: Points):
        self.point_obj = points_obj

    def get_closest_pair(self):
        """
        Calculates and returns the closest pair of points.

        :return: the closest pair (tuple)
        """
        n = self.point_obj.size
        d = self.point_obj.dim
        indices = np.arange(0, self.point_obj.size, 1)

        # Calls Brute Force or Divide and Conquer algorithm based on the points and the complexity.
        if (d * n**2) < (n * math.log2(n)**d):
            print('BruteForce')
            return self.brute_force(indices)
        else:
            print('Divide and Conquer')
            sorted_indices = self.point_obj.sort_indices_by_coord(indices)
            return self.divide_and_conquer(sorted_indices)

    def divide_and_conquer(self, indices, dim=0, delta=float('inf')):
        """
        A recursive function that implements the Divide and Conquer algorithm.
        Recursively separates the space and projects points into lower dimensions.

        :param indices: indices of the points (list)
        :param dim: specifies the current dimension (int)
        :param delta: distance of the previous closest pair (float)
        :return: the closest pair (tuple)
        """
        if len(indices) <= 3:
            return self.brute_force(indices, dim, delta)

        # Divide step.
        midpoint, s1, s2 = self.divide_at_midpoint(indices, dim)
        cp1 = self.divide_and_conquer(s1, dim)
        cp2 = self.divide_and_conquer(s2, dim)
        cp = self.minimum_closest_pair(cp1, cp2)
        delta = cp[2]

        # Selecting points within delta of the hyperplane.
        slab_indices = []
        for i in indices:
            coordinate = self.point_obj.get_by_index(i)[dim]
            if midpoint - delta < coordinate < midpoint + delta:
                slab_indices.append(i)

        # Projecting and solving problem in reduced dimension.
        if dim < self.point_obj.dim - 2:
            sorted_slab_indices = self.point_obj.sort_indices_by_coord(slab_indices, dim + 1)
            cp3 = self.divide_and_conquer(sorted_slab_indices, dim + 1, delta)
        else:
            cp3 = self.linear_search(slab_indices, delta)

        # Selecting the pair with the smaller distance.
        closest_pair = self.minimum_closest_pair(cp, cp3)

        return closest_pair

    def brute_force(self, indices, dim=0, delta=float('inf')):
        """
        A naive algorithm for finding the closest pair of points.

        :param indices: indices of the points (list)
        :param dim: specifies the current dimension (int)
        :param delta: distance of the previous closest pair (float)
        :return: the closest pair (tuple)
        """
        n = len(indices)
        closest_pair = (-1, -1, float('inf'))
        if n >= 2:
            for i in range(n - 1):
                i_ind = indices[i]
                for j in range(i + 1, n):
                    j_ind = indices[j]
                    # Check if current distance is smaller than the smallest known distance in lower dimension.
                    lower_dim_dist = self.point_obj.get_distance(i_ind, j_ind, dim)
                    if lower_dim_dist < delta:
                        real_dist = self.point_obj.get_distance(i_ind, j_ind, 0)
                        if real_dist < delta:
                            delta = real_dist
                            closest_pair = (i_ind, j_ind, delta)

        return closest_pair

    def linear_search(self, indices, delta=float('inf')):
        """
        Optimised closest pair search on a 1D sorted array.

        :param indices: indices of the points (list)
        :param delta: distance of the previous closest pair (float)
        :return: the closest pair (tuple)
        """
        closest_pair = (-1, -1, float('inf'))
        n = len(indices)
        if n >= 2:
            for i in range(n - 1):
                i_ind = indices[i]
                for j in range(i + 1, min(i + 7, n)):
                    j_ind = indices[j]
                    # Calculate current distance and compare with the smallest.
                    dist = self.point_obj.get_distance(i_ind, j_ind, 0)
                    if dist < delta:
                        delta = dist
                        closest_pair = (i_ind, j_ind, delta)

        return closest_pair

    def divide_at_midpoint(self, indices, dim):
        """
        Separates the points in the space by a hyperplane that is perpendicular to the axis defined by dim.

        :param indices: list of indices (list)
        :param dim: which axis the hyperplane should be perpendicular to (integer)
        :return: value on the specified axis and the two separated set of points (tuple)
        """
        # Midpoint is calculated from the average of the specified coordinate values of the two border points.
        m = len(indices) // 2
        m1 = self.point_obj.get_by_index(indices[m - 1])[dim]
        m2 = self.point_obj.get_by_index(indices[m])[dim]

        midpoint = (m1 + m2) / 2
        s1 = indices[:m]
        s2 = indices[m:]

        return midpoint, s1, s2

    @staticmethod
    def minimum_closest_pair(closest_pair_1, closest_pair_2):
        """
        Returns the pair with the smaller distance.

        :param closest_pair_1: first pair (tuple)
        :param closest_pair_2: second pair (tuple)
        :return: the closer pair (tuple)
        """
        if closest_pair_1[2] < closest_pair_2[2]:
            return closest_pair_1
        else:
            return closest_pair_2
