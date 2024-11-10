import abc


class Repository(abc.ABC):
    @abc.abstractmethod
    def store(self, id, data):
        pass

    @abc.abstractmethod
    def retrieve(self, id):
        pass
