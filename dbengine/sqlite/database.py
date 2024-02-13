from sqlite3 import connect, Connection, Cursor
from .table import Table
from ..template.database import DatabaseOrigin

# 数据库类
class Database(DatabaseOrigin):
    # 初始化
    async def _init(self, name:str='./database.db', threadId:int=0, *args, **kwargs)->None:
        self.connection:Connection = connect(name)
        self.cursors:dict[int,Cursor] = {}
        for tableName in list(self.getCursor(threadId).execute('SELECT name FROM sqlite_master WHERE type="table"')):
            self.tables[tableName] = Table(self, tableName)
    # [SQL独有] 获取cursor 
    async def getCursor(self, threadId:int=0, *args, **kwargs)->Cursor:
        if threadId not in self.cursors.keys():
            self.cursors[threadId] = self.connection.cursor()
        return self.cursors[threadId]
    async def _create(self, name:str, create:list[tuple[str]], threadId:int=0, *args, **kwargs)->Table:
        self.getCursor(threadId).execute(f'CREATE TABLE {name} ({','.join([_+' '+' '.join(create[_]) for _ in create.keys()])})')
        await self.connection.commit()