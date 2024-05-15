import numpy as np
import pytest


@pytest.fixture
def define_edm_measured():
    return np.array(
        [
            [0, 162.1613, 162.2531],
            [162.1270, 0, 162.2449],
            [162.2155, 162.2582, 0],
        ]
    )


@pytest.fixture
def define_edm_real():
    return np.array(
        [
            [0, 7.914, 7.914],
            [7.914, 0, 7.914],
            [7.914, 7.914, 0],
        ]
    )


@pytest.fixture
def define_device_list():
    return ["device1", "device2", "device3"]


@pytest.fixture
def define_measurement_list():
    return [
        0,
        162.1613,
        162.2531,
        162.1270,
        0,
        162.2449,
        162.2155,
        162.2582,
        0,
    ]
