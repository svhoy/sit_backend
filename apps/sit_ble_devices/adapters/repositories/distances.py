from . import AbstractRepository
from sit_ble_devices.domain import events
from sit_ble_devices.models import DistanceMeasurement as django_model
from sit_ble_devices.domain.model import distances


class DistanceMeasurementRepository(AbstractRepository):
    async def add(self, measurement: distances.DistanceMeasurement):
        await django_model.from_domain(measurement=measurement)
        self.seen.add(measurement)
        measurement.events.append(
            events.MeasurementSaved(
                initiator=None,
                sequence=measurement.sequence,
                distance=measurement.distance,
                nlos=measurement.nlos,
                rssi=measurement.rssi,
                fpi=measurement.fpi,
                e_distance=measurement.edistance,
            )
        )

    def get_by_test(self, test):
        return django_model.objects.filter(test=test)

    def list(self):
        return [d.to_domain() for d in django_model.objects.all()]
