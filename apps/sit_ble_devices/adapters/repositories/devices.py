from sit_ble_devices.domain import events
from sit_ble_devices.domain.model import uwbdevice
from sit_ble_devices.models import AntDelay as django_delay_model
from sit_ble_devices.models import UwbDevice as django_model

from . import AbstractRepository


class UwbDeviceRepository(AbstractRepository):
    async def add(self, uwb_device_domain: uwbdevice.UwbDevice):
        django_model.from_domain(uwb_device_domain)
        uwb_device_domain.events.append(
            events.AddedUwbDevice(
                device_name=uwb_device_domain.device_name,
                device_id=uwb_device_domain.device_id,
            )
        )

    async def add_ant_dly(
        self, uwb_device_dom: uwbdevice.UwbDevice, ant_dly: uwbdevice.AntDelay
    ):
        ant_dly.ant_delay_id = await django_delay_model.from_domain(ant_dly)
        uwb_device_dom.append_ant_delay(ant_dly)
        return uwb_device_dom

    async def get_by_id(self, device_id: str) -> uwbdevice.UwbDevice:
        model = await django_model.objects.aget(device_id=device_id)
        return await model.to_domain()

    def get_ant_dly_by_device(self, device_id) -> list[uwbdevice.AntDelay]:
        return [
            d.to_domain()
            for d in django_delay_model.objects.filter(
                device__device_id=device_id
            )
        ]

    def list(self) -> list[uwbdevice.UwbDevice]:
        return [d.to_domain() for d in django_model.objects.all()]
