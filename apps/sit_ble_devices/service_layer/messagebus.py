from shutil import ExecError
from sit_ble_devices.domain import commands, events


class MessageBus:
    def __init__(self, uow, duow, event_handlers, command_handlers):
        self.uow = uow
        self.duow = duow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    async def handle(self, message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                await self.handle_event(message)
            elif isinstance(message, commands.Command):
                print(message)
                await self.handle_command(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    async def handle_event(self, event):
        handlers = self.event_handlers[type(event)]
        for handler in handlers:
            try:
                await handler(event)
                self.queue.extend(self.uow.collect_new_events())
                self.queue.extend(self.duow.collect_distance_events())
            except Exception:
                print("Exception handling command %s", event)
                continue

    async def handle_command(self, command):
        handler = self.command_handlers[type(command)]
        try:
            await handler(command)
            self.queue.extend(self.uow.collect_new_events())
            self.queue.extend(self.duow.collect_distance_events())
        except Exception:
            print("Exception handling command %s", command)
            raise
