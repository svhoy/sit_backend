from sit_ble_devices.domain.model import calibration
from sit_ble_devices.service_layer.utils.Calibration.genericCalibration import (
    DecaCalibration,
)
from sit_ble_devices.service_layer.utils.Calibration.psoCalibration import (
    PsoCalibration,
)


async def start_calibration(
    calibration_dom: calibration.Calibrations,
) -> list[float]:
    calibration_instance = None
    match calibration_dom.calibration_type:
        case "Antenna Calibration (ASP014)":
            calibration_instance = DecaCalibration(calibration_dom)
        case "Antenna Calibration (PSO)":
            calibration_instance = PsoCalibration(calibration_dom)
        case _:
            raise ValueError("Invalid calibration type")

    if calibration is not None:
        result = await calibration_instance.calibration_calc()
    else:
        result = -1
    return result
