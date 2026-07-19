import numpy as np


class FeatureMap:

    def __init__(self):

        pass

    def angle_encoding(self, features):

        """
        Convert classical features
        into rotation angles.

        Parameters
        ----------
        features : list or numpy array

        Returns
        -------
        numpy.ndarray
        """

        features = np.asarray(
            features,
            dtype=float
        )

        return features