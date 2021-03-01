from abc import ABC, abstractmethod


class Generator(ABC):
    @abstractmethod
    def apply(self, world):
        pass
