from ..template.table import TableOrigin
from pymongo.collection import Collection
from typing import Union

class Table(TableOrigin):
    async def _init(self, collection:Collection, *args, **kwargs)->None:
        self.tb = collection
    async def _new(self, data:dict[str,any], *args, **kwargs)->None:
        await self.tb.insert_one(data)
    async def _get(self, query:dict[str,any], target:Union[tuple[str],dict[str,bool]]={}, *args, **kwargs)->list:
        return list([_.values() for _ in self.tb.find(query,projection=target)])