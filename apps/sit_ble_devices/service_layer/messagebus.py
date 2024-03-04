import logging

from sit_ble_devices.domain import commands, events

logger = logging.getLogger("service_layer.messagebus")


class MessageBus:
    def __init__(
        self,
        uow,
        duow,
        cuow,
        uduow,
        *args,
        **kwargs,
    ):
        self.uow = uow
        self.duow = duow
        self.cuow = cuow
        self.uduow = uduow
        self.event_handlers = kwargs.get("event_handlers", {})
        self.command_handlers = kwargs.get("command_handlers", {})
        self.queue = []

    async def handle(self, message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                await self.handle_event(message)
            elif isinstance(message, commands.Command):
                logger.debug(f"Message Queue: {message}")
                await self.handle_command(message)
            else:
                raise ValueError(f"{message} was not an Event or Command")

    async def handle_event(self, event):
        handlers = self.event_handlers[type(event)]
        for handler in handlers:
            try:
                await handler(event)
                self.queue.extend(self.uow.collect_new_events())
                self.queue.extend(self.duow.collect_new_events())
                self.queue.extend(self.cuow.collect_new_events())
                self.queue.extend(self.uduow.collect_new_events())
            except Exception:  # pylint: disable=broad-exception-caught
                logger.error(f"Exception handling event: {event}")
                continue

    async def handle_command(self, command):
        handler = self.command_handlers[type(command)]
        try:
            await handler(command)
            self.queue.extend(self.uow.collect_new_events())
            self.queue.extend(self.duow.collect_new_events())
            self.queue.extend(self.cuow.collect_new_events())
            self.queue.extend(self.uduow.collect_new_events())

        except Exception:  # pylint: disable=broad-exception-caught
            logger.error(f"Exception handling command: {command}")
