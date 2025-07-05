from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def save(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError
