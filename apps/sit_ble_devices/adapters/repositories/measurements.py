import logging
from venv import logger

from asgiref.sync import sync_to_async
from sit_ble_devices.domain import events
from sit_ble_devices.domain.model import distances
from sit_ble_devices.models import CalibrationMeasurements as django_model

from . import AbstractRepository

logger = logging.getLogger("sit.adapters.repositories.distances")


class CalibrationMeasurementRepository(AbstractRepository):
    async def add(self, domain_model: distances.CalibrationMeasurements):
        await self.update(domain_model)
        await super().add(domain_model)
        domain_model.events.append(
            events.CalibrationMeasurementSaved(
                devices=[
                    domain_model.device_a,
                    domain_model.device_b,
                    domain_model.device_c,
                ],
                measurement=domain_model.measurement,
                sequence=domain_model.sequence,
            )
        )

    async def update(self, domain_model: distances.CalibrationMeasurements):
        await django_model.update_from_domain(measurement=domain_model)

    async def update_calibration_id(
        self,
        calibration_id: int,
        new_calibration_id: int,
    ):
        """
        Update the calibration ID for distance measurements.

        Args:
            calibration_id (int): The current calibration ID.
            new_calibration_id (int): The new calibration ID.

        Returns:
            None
        """

        distance_measurements = await sync_to_async(
            django_model.objects.filter
        )(calibrations=calibration_id)

        through_objects = []

        async for distance in distance_measurements:
            through_object = await sync_to_async(
                django_model.calibrations.through
            )(
                calibrationmeasurements_id=distance.id,
                calibration_id=new_calibration_id,
            )
            through_objects.append(through_object)

        test = await sync_to_async(
            django_model.calibrations.through.objects.bulk_create
        )(through_objects)
        logger.debug(
            f"Updated calibration_id for {len(through_objects)} calibration measurements: {len(test)}"
        )

    async def get_by_calibration_id(self, calibration_id):
        distance_list = []
        distance_list_buf = [
            d
            async for d in django_model.objects.filter(
                calibrations=calibration_id
            )
        ]

        for d in distance_list_buf:
            domain = await sync_to_async(d.to_domain)()
            distance_list.append(domain)

        return distance_list

    async def list(self):
        return [await d.to_domain() async for d in django_model.objects.all()]
