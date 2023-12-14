from sit_ble_devices.domain import events
from sit_ble_devices.domain.model import calibration
from sit_ble_devices.models import Calibration as django_model
from sit_ble_devices.models import (
    CalibrationsDistances as django_cali_dist_model,
)

from . import AbstractRepository


class CalibrationRepository(AbstractRepository):
    async def add(self, calibration_domain: calibration.Calibrations):
        calibration_domain.calibration_id = await django_model.from_domain(
            calibration_dom=calibration_domain
        )
        self.seen.add(calibration_domain)
        calibration_domain.events.append(
            events.CalibrationCreated(
                calibration_id=calibration_domain.calibration_id,
            )
        )

    async def add_cali_distances(
        self,
        calibration_domain: calibration.Calibrations,
        cali_distances_domains: list[calibration.CalibrationDistance],
    ):
        for cali_distance_domain in cali_distances_domains:
            cali_distance_domain.id = await django_cali_dist_model.from_domain(
                cali_distance_dom=cali_distance_domain
            )
            calibration_domain.append_cali_distances(cali_distance_domain)
        self.seen.add(calibration_domain)
        print(f"Calibration Devices: {calibration_domain.devices}")
        calibration_domain.events.append(
            events.CalibrationInitFinished(
                calibration_id=calibration_domain.calibration_id,
                calibration_type=calibration_domain.calibration_type,
                devices=calibration_domain.devices,
            )
        )

    async def get_by_id(self, cali_id) -> calibration.Calibrations:
        model = await django_model.objects.aget(id=cali_id)
        print(f"Calibration Model: {model}")
        return await model.to_domain()

    def list(self):
        return [d.to_domain() for d in django_model.objects.all()]
