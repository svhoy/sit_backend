from sit_ble_devices.domain import events
from sit_ble_devices.domain.model import distances
from sit_ble_devices.models import DistanceMeasurement as django_model

from . import AbstractRepository


class DistanceMeasurementRepository(AbstractRepository):
    async def add(self, domain_model: distances.DistanceMeasurement):
        await django_model.from_domain(measurement=domain_model)
        self.seen.add(domain_model)
        domain_model.events.append(
            events.MeasurementSaved(
                initiator=None,
                sequence=domain_model.sequence,
                distance=domain_model.distance,
                nlos=domain_model.nlos_final,
                rssi=domain_model.rssi_final,
                fpi=domain_model.fpi_final,
                e_distance=domain_model.edistance,
            )
        )

    async def get_by_test(self, test):
        return [d.to_domain() for d in django_model.objects.filter(test=test)]

    async def get_by_calibration_id(self, calibration_id):
        return [
            d.to_domain()
            for d in django_model.objects.filter(
                calibration__id=calibration_id
            )
        ]

    async def list(self):
        return [d.to_domain() for d in django_model.objects.all()]
