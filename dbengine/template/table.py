from .origin import T, D

class TableOrigin(T):
    def _init(self, *args, **kwargs):
        pass
    def __init__(self, *args, **kwargs):
        self._init(*args, **kwargs)
    async def _new(self, *args, **kwargs):
        pass
    async def new(self, data:dict[str,any], *args, **kwargs):
        await self._new(data=data,*args,**kwargs)
    async def _get(self, *args, **kwargs)->list:
        return []
    async def get(self, query:dict[str,any], *args, **kwargs)->list:
        return await self._get(query, *args, **kwargs)
    async def _remove(self, *args, **kwargs):
        pass
    async def remove(self, query:dict[str,any], *args, **kwargs):
        await self._remove(query, *args, **kwargs)