from sit_ble_devices.store import Store
from sit_ble_devices.domain import events


class WsClients:
    def __init__(self) -> None:
        self.json_store = Store()
        self.events = []

    async def add_connection(self, id):
        websocket_connections = self.json_store.get_value(
            "websocket_connection", []
        )
        connection_set = set(websocket_connections)
        connection_set.add(id)
        self.json_store.set_value("websocket_connection", list(connection_set))
        self.json_store.save()
        self.events.append(
            events.WsClientRegisterd(clients=list(connection_set))
        )

    async def remove_connections(self):
        connection_list = []
        connection_list.extend(
            self.json_store.get_value("websocket_connection", [])
        )
        connection_list.clear()
        self.json_store.set_value("websocket_connection", connection_list)
        self.json_store.save()
        self.events.append(events.WsClientUnregisterd(room_id="sit_1"))
