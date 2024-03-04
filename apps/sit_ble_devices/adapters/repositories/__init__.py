import abc


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    async def add(self, domain_model):
        raise NotImplementedError

    async def update(self, domain_model):
        raise NotImplementedError

    async def list(self):
        raise NotImplementedError

    async def get_by_id(self, domain_id):
        raise NotImplementedError
