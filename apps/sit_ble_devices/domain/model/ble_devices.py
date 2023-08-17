from sit_ble_devices.store import Store
from sit_ble_devices.domain import events


class BleClients:
    def __init__(self) -> None:
        self.json_store = Store()
        self.events = []

    async def add_connection(self, id):
        device_list = self.json_store.get_value("device_list", [])
        connection_set = set(device_list)
        connection_set.add(id)
        self.json_store.set_value("device_list", list(connection_set))
        self.json_store.save()
        self.events.append(
            events.BleDeviceRegistered(
                device_list=list(connection_set), new_device=id
            )
        )

    async def remove_connection(self, id):
        device_list = []
        device_list.extend(self.json_store.get_value("device_list", []))
        if id in device_list:
            device_list.remove(id)
        self.json_store.set_value("device_list", device_list)
        device_list.save()
        self.events.append(
            events.BleDeviceUnregistered(device_list=device_list, device=id)
        )

    def get_device_list(self):
        return self.json_store.get_value("device_list", [])
