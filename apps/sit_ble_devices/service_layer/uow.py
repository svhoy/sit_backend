from __future__ import annotations
import abc
from sit_ble_devices.domain.model.ble_devices import BleClients
from sit_ble_devices.domain.model.ws_clients import WsClients


class AbstractUnitOfWork(abc.ABC):
    wsConnection: WsClients
    bleDevices: BleClients

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    def collect_new_events(self):
        while self.wsConnection.events:
            yield self.wsConnection.events.pop(0)
        while self.bleDevices.events:
            yield self.bleDevices.events.pop(0)

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    async def __aenter__(self) -> AbstractUnitOfWork:
        self.wsConnection = WsClients()
        self.bleDevices = BleClients()
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)

    async def commit(self):
        await self._commit()

    async def _commit(self):
        pass

    async def rollback(self):
        pass
