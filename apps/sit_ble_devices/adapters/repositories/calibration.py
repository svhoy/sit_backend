import logging
from typing import List

from asgiref.sync import sync_to_async
from sit_ble_devices.domain import events
from sit_ble_devices.domain.model import calibration
from sit_ble_devices.models import Calibration as django_model
from sit_ble_devices.models import (
    CalibrationsDistances as django_cali_dist_model,
)

from . import AbstractRepository

logger = logging.getLogger("sit.adapters.repositories.calibration")


class CalibrationRepository(AbstractRepository):
    async def add(self, domain_model: calibration.Calibrations):
        domain_model.calibration_id = await django_model.from_domain(
            calibration_dom=domain_model
        )
        self.seen.add(domain_model)
        domain_model.events.append(
            events.CalibrationCreated(
                calibration_id=domain_model.calibration_id,
            )
        )
        return domain_model.calibration_id

    async def list(self):
        return [d.to_domain() for d in django_model.objects.all()]

    async def get_by_id(self, domain_id: int) -> calibration.Calibrations:
        model = await django_model.objects.aget(id=domain_id)
        domain_model = await model.to_domain()
        distance_list_buf = [
            d
            async for d in django_cali_dist_model.objects.filter(
                calibration_mod__pk=domain_id
            )
        ]

        for d in distance_list_buf:
            cali_distance = await sync_to_async(d.to_domain)()
            await domain_model.append_cali_distances(cali_distance)

        return domain_model

    async def add_cali_distances(
        self,
        calibration_domain: calibration.Calibrations,
        cali_distances_domains: List[calibration.CalibrationDistance],
        copie=False,
    ):
        for cali_distance_domain in cali_distances_domains:
            cali_distance_domain.id = await django_cali_dist_model.from_domain(
                cali_distance_dom=cali_distance_domain
            )
            await calibration_domain.append_cali_distances(
                cali_distance_domain
            )
        self.seen.add(calibration_domain)
        if copie is False:
            calibration_domain.events.append(
                events.CalibrationInitFinished(
                    calibration_id=calibration_domain.calibration_id,
                    calibration_type=calibration_domain.calibration_type,
                    measurement_type=calibration_domain.measurement_type,
                    devices=calibration_domain.devices,
                )
            )
