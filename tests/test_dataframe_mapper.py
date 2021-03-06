import pytest

from pandas import DataFrame
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

from sklearn_pandas import (
    DataFrameMapper,
    PassthroughTransformer,
    cross_val_score,
)


@pytest.fixture
def iris_dataframe():
    iris = load_iris()
    return DataFrame(
        data={
            iris.feature_names[0]: iris.data[:, 0],
            iris.feature_names[1]: iris.data[:, 1],
            iris.feature_names[2]: iris.data[:, 2],
            iris.feature_names[3]: iris.data[:, 3],
            "species": np.array([iris.target_names[e] for e in iris.target])
        }
    )


@pytest.fixture
def cars_dataframe():
    return pd.read_csv("tests/test_data/cars.csv.gz")


def test_with_iris_dataframe(iris_dataframe):
    pipeline = Pipeline([
        ("preprocess", DataFrameMapper([
            ("petal length (cm)", PassthroughTransformer()),
            ("petal width (cm)", PassthroughTransformer()),
            ("sepal length (cm)", PassthroughTransformer()),
            ("sepal width (cm)", PassthroughTransformer()),
        ])),
        ("classify", SVC(kernel='linear'))
    ])
    data = iris_dataframe.drop("species", axis=1)
    labels = iris_dataframe["species"]
    scores = cross_val_score(pipeline, data, labels)
    assert scores.mean() > 0.96
    assert (scores.std() * 2) < 0.04


def test_with_car_dataframe(cars_dataframe):
    pipeline = Pipeline([
        ("preprocess", DataFrameMapper([
            ("description", CountVectorizer()),
        ])),
        ("classify", SVC(kernel='linear'))
    ])
    data = cars_dataframe.drop("model", axis=1)
    labels = cars_dataframe["model"]
    scores = cross_val_score(pipeline, data, labels)
    assert scores.mean() > 0.30
