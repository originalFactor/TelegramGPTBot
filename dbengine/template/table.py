from .origin import T, D

class TableOrigin(T):
    async def _init(self, *args, **kwargs)->None:
        pass
    async def __init__(self, *args, **kwargs) -> None:
        await self._init(*args, **kwargs)
    async def _new(self, *args, **kwargs) -> None:
        pass
    async def new(self, data:dict[str,any], *args, **kwargs)->None:
        await self._new(data=data,*args,**kwargs)
    async def _get(self, *args, **kwargs)->list:
        return []
    async def get(self, query:dict[str,any], *args, **kwargs)->list:
        return await self._get(query=query, *args, **kwargs)