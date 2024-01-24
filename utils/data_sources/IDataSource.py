from abc import ABC, abstractmethod


class IDataSource(ABC):
    @abstractmethod
    def get_list(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement get_list method")

    @abstractmethod
    def get_item(self, *args, **kwargs):
        pass

    @abstractmethod
    def insert_item(self, *args, **kwargs):
        pass

    @abstractmethod
    def update_item(self, *args, **kwargs):
        pass
