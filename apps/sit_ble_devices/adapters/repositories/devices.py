from typing import List

from sit_ble_devices.domain import events
from sit_ble_devices.domain.model import uwbdevice
from sit_ble_devices.models import AntDelay as django_delay_model
from sit_ble_devices.models import UwbDevice as django_model

from . import AbstractRepository


class UwbDeviceRepository(AbstractRepository):
    async def add(self, domain_model: uwbdevice.UwbDevice):
        django_model.from_domain(domain_model)
        domain_model.events.append(
            events.AddedUwbDevice(
                device_name=domain_model.device_name,
                device_id=domain_model.device_id,
            )
        )

    async def get_by_id(self, domain_id: str) -> uwbdevice.UwbDevice:
        model = await django_model.objects.aget(device_id=domain_id)
        return await model.to_domain()

    async def list(self) -> list[uwbdevice.UwbDevice]:
        return [d.to_domain() for d in django_model.objects.all()]

    async def add_ant_dly(
        self,
        device_domain_model: uwbdevice.UwbDevice,
        ant_dly: uwbdevice.AntDelay,
    ):
        ant_dly.ant_delay_id = await django_delay_model.from_domain(ant_dly)
        device_domain_model.append_ant_delay(ant_dly)
        return device_domain_model

    def get_ant_dly_by_device(self, device_id) -> List[uwbdevice.AntDelay]:
        return [
            d.to_domain()
            for d in django_delay_model.objects.filter(
                device__device_id=device_id
            )
        ]
