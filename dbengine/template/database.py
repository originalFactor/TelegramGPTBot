from .origin import D, T

# Database父类
class DatabaseOrigin(D):
    # 此处写自定义init
    def _init(self, *args, **kwargs):
        pass
    # 标准init
    def __init__(self, name:str, *args, **kwargs):
        self.tables:dict[str,T] = {}
        self._init(name, *args, **kwargs)
    #自定义create
    async def _create(self, name:str, create:dict[str,tuple[str]], *args, **kwargs):
        pass
    # 标准get
    async def get(self, name:str, create:dict[str,tuple[str]]={}, *args, **kwargs)->T:
        if name not in self.tables:
            await self._create(name=name, create=create, *args, **kwargs)
        return self.tables[name]
    async def _remove(self, *args, **kwargs):
        pass
    async def remove(self, name:str, *args, **kwargs):
        await self._remove(name, *args, **kwargs)
    async def exists(self, name:str):
        return name in self.tables.keys()