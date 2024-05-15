import numpy as np
import pytest


@pytest.fixture
def define_edm_measured_tof():
    matrix = np.array(
        [
            [0, 5.41074147e-07, 5.41380451e-07],
            [5.40959700e-07, 0, 5.41353090e-07],
            [5.41254993e-07, 5.41397468e-07, 0],
        ]
    )
    return matrix


@pytest.fixture
def define_edm_real_tof():
    matrix = np.array(
        [
            [0.0, 2.6406182e-08, 2.6406182e-08],
            [2.6406182e-08, 0.0, 2.6406182e-08],
            [2.6406182e-08, 2.6406182e-08, 0.0],
        ]
    )
    print(type(matrix))
    return matrix


@pytest.fixture
def define_delay_array():
    return np.array(
        [
            514.4747e-9,
            514.5911e-9,
            515.0413e-9,
        ]
    )


@pytest.fixture
def define_measurement_list():
    pass
