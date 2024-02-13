from ..template.database import DatabaseOrigin
from pymongo import MongoClient
from .table import Table

class Database(DatabaseOrigin):
    async def _init(self, name:str, host:str='mongodb://127.0.0.1:27017', *args, **kwargs)->None:
        self.client = MongoClient(host)
        self.db = self.client[name]
    async def _create(self, name:str, *args, **kwargs)->None:
        self.tables[name] = Table(self.db[name])
    