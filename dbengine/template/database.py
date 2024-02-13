from origin import D, T

# Database父类
class DatabaseOrigin(D):
    # 此处写自定义init
    async def _init(self, *args, **kwargs)->None:
        pass
    # 标准init
    async def __init__(self, *args, **kwargs)->None:
        self.tables:dict[str,T] = {}
        await self._init(*args, **kwargs)
    #自定义create
    async def _create(self, name:str, create:dict[str,tuple[str]], *args, **kwargs)->None:
        pass
    # 标准get
    async def get(self, name:str, create:dict[str,tuple[str]]={}, *args, **kwargs)->T:
        if name not in self.tables:
            await self._create(name=name, create=create, *args, **kwargs)
        return self.tables[name]