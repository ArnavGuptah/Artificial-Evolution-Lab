from sklearn.feature_selection import mutual_info_classif
import numpy as np

#ranking the useful biological features to 
# ... select best features to be used as qubits 

class MutualInformationSelector:

    def __init__(self):

        self.scores = None

    def rank(self, X, y, feature_names):

        """
        Rank features using Mutual Information.

        X : list of feature vectors
        y : labels
        feature_names : list of feature names

        Returns
        -------
        list of (feature, score)
        """

        X = np.asarray(X)

        y = np.asarray(y)

        self.scores = mutual_info_classif(

            X,
            y,
            random_state=42

        )

        ranking = list(zip(feature_names, self.scores))

        ranking.sort(key=lambda x: x[1], reverse=True)

        return ranking

    def select_top_k(self, ranking, k):

        """
        Return the top-k ranked features.
        ranking : list of (feature_name, score)
        k : int

        Returns
        list
        """

        return ranking[:k]