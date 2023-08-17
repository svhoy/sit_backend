import abc


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    async def add(self, record):
        await self._add(record)
        self.seen.add(record)

    async def get_by_id(self, id):
        record = await self._get_by_id(id)
        return record

    @abc.abstractmethod
    async def _add(self, record):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_by_id(self, batchref):
        raise NotImplementedError
