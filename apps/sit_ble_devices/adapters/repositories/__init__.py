import abc


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()
