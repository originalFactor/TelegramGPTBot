from ..template.database import DatabaseOrigin
from pymongo import MongoClient
from .table import Table

class Database(DatabaseOrigin):
    def _init(self, name:str, host:str='mongodb://127.0.0.1:27017', *args, **kwargs):
        self.client = MongoClient(host)
        self.db = self.client[name]
    async def _create(self, name:str, *args, **kwargs):
        self.tables[name] = Table(self.db[name])
    async def _remove(self, name:str, *args, **kwargs):
        if name in self.tables.keys():
            self.tables[name].tb.drop()
            del self.tables[name]