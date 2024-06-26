import inspect

from sit_ble_devices.service_layer import uow

from apps.sit_ble_devices.service_layer import messagebus
from apps.sit_ble_devices.service_layer.handlers import (
    command_handler,
    event_handler,
)


def bootstrap(
    uow: uow.AbstractUnitOfWork,
    duow: uow.DistanceUnitOfWork,
    cuow: uow.CalibrationUnitOfWork,
    uduow: uow.UwbDeviceUnitOfWork,
    cmuow: uow.CalibrationMeasurementUnitOfWork,
):
    dependencies = {
        "uow": uow,
        "duow": duow,
        "cuow": cuow,
        "uduow": uduow,
        "cmuow": cmuow,
    }

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in event_handler.EVENT_HANDLER.items()
    }

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in command_handler.COMMAND_HANDLER.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        duow=duow,
        cuow=cuow,
        uduow=uduow,
        cmuow=cmuow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(
        message, **deps
    )  # pylint: disable=unnecessary-lambda
