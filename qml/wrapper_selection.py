from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SequentialFeatureSelector


class WrapperSelector:

    def __init__(

        self,

        estimator=None,

        n_features=8

    ):

        self.estimator = (

            estimator

            if estimator is not None

            else RandomForestClassifier(

                random_state=42

            )

        )

        self.n_features = n_features

    def select(

        self,

        X,

        y,

        feature_names

    ):

        selector = SequentialFeatureSelector(

            self.estimator,

            n_features_to_select=self.n_features,

            direction="forward",

            scoring="accuracy",

            cv=5

        )

        selector.fit(X, y)

        mask = selector.get_support()

        selected = [

            feature

            for feature, keep

            in zip(feature_names, mask)

            if keep

        ]

        return selected