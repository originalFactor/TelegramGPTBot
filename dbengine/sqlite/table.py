from ..template.table import TableOrigin
from ..template.database import DatabaseOrigin
from typing import Union

# 数据表
class Table(TableOrigin):
    # 初始化
    async def _init(self, db:DatabaseOrigin, name:str, *args, **kwargs):
        self.db:DatabaseOrigin = db
        self.name:str = name
    # 新行
    async def _new(self, data:dict[str,any], threadId:int=0, *args, **kwargs):
        (await self.db.getCursor(threadId)).execute(f'INSERT INTO {self.name} ({",".join(data.keys())}) VALUES ({",".join(["?" for _ in data.values()])})',tuple(data.values()))
        self.db.connection.commit()
    # 获取数据
    async def _get(self, query:Union[dict[str,any],str]="", target:Union[tuple[str],str]="*", threadId:int=0, *args, **kwargs)->list[list[str]]:
        return list([
            [0]+_
            for _ in
            list((await self.db.getCursor(threadId)).execute(
                f'''SELECT {
                    target 
                    if type(target)==str else 
                    ",".join(target)
                } FROM {self.name} {
                    "WHERE "+(
                        query 
                        if type(query)==str else 
                        " AND ".join([
                            f"{_}={query[_]}"
                            for _ in query.keys()
                        ])
                    ) if query else ""
                }'''
            ))
        ])
    async def _remove(self, query:dict[str,any], threadId:int=0, *args, **kwargs):
        self.db.getCursor(threadId).execute(
            f"DELETE FROM {self.name}"
            f"{'WHERE '+' AND '.join([f'{_}=?' for _ in query.keys()]) if query else ''}",
            tuple(query.values())
        )