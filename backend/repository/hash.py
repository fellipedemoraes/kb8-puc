from .entities import Repository


class HashRepository(Repository):
    def __init__(self):
        self.data = {}

    def store(self, id, data: dict):
        self.data[id] = data

    def retrieve(self, id: str):
        return self.data[id]
