from __future__ import annotations

import abc

from asgiref.sync import sync_to_async
from django.db import transaction

from sit_ble_devices.adapters.repositories.calibration import (
    CalibrationRepository,
)
from sit_ble_devices.adapters.repositories.devices import UwbDeviceRepository
from sit_ble_devices.adapters.repositories.distances import (
    DistanceMeasurementRepository,
)
from sit_ble_devices.domain.model.ble_devices import BleClients
from sit_ble_devices.domain.model.ws_clients import WsClients


class AbstractUnitOfWork(abc.ABC):
    ws_connection: WsClients
    ble_devices: BleClients
    uwb_device_repo: UwbDeviceRepository
    distance_measurement: DistanceMeasurementRepository
    calibration_repo: CalibrationRepository

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    def collect_new_events(self):
        while self.ws_connection.events:
            yield self.ws_connection.events.pop(0)
        while self.ble_devices.events:
            yield self.ble_devices.events.pop(0)

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    async def __aenter__(self) -> AbstractUnitOfWork:
        self.ws_connection = WsClients()
        self.ble_devices = BleClients()
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)

    async def commit(self):
        await self._commit()

    async def _commit(self):
        pass

    async def rollback(self):
        pass


class DistanceUnitOfWork(AbstractUnitOfWork):
    async def __aenter__(self) -> AbstractUnitOfWork:
        self.distance_measurement = DistanceMeasurementRepository()
        sync_to_async(transaction.set_autocommit)(False)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        sync_to_async(transaction.set_autocommit)(True)

    async def commit(self):
        sync_to_async(transaction.commit)

    async def rollback(self):
        sync_to_async(transaction.rollback)

    def collect_distance_events(self):
        try:
            for measurement in self.distance_measurement.seen:
                while measurement.events:
                    yield measurement.events.pop(0)
        except AttributeError:
            print("Error while collecting Distance Events")


class CalibrationUnitOfWork(AbstractUnitOfWork):
    async def __aenter__(self) -> AbstractUnitOfWork:
        self.calibration_repo = CalibrationRepository()
        sync_to_async(transaction.set_autocommit)(False)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        sync_to_async(transaction.set_autocommit)(True)

    async def commit(self):
        sync_to_async(transaction.commit)

    async def rollback(self):
        sync_to_async(transaction.rollback)

    def collect_calibration_events(self):
        try:
            for calibration in self.calibration_repo.seen:
                while calibration.events:
                    yield calibration.events.pop(0)
        except AttributeError:
            print("Error while collecting Calibration Events")


class UwbDeviceUnitOfWork(AbstractUnitOfWork):
    async def __aenter__(self) -> AbstractUnitOfWork:
        self.uwb_device_repo = UwbDeviceRepository()
        sync_to_async(transaction.set_autocommit)(False)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        sync_to_async(transaction.set_autocommit)(True)

    async def commit(self):
        sync_to_async(transaction.commit)

    async def rollback(self):
        sync_to_async(transaction.rollback)

    def collect_uwb_device_events(self):
        try:
            for device in self.uwb_device_repo.seen:
                while device.events:
                    yield device.events.pop(0)
        except AttributeError:
            print("Error while collecting UWB Device Events")
