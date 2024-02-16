# Copyright (C) 2024 OriginalFactor
# 
# This file is part of TelegramGPTBot.
# 
# TelegramGPTBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# TelegramGPTBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with TelegramGPTBot.  If not, see <http://www.gnu.org/licenses/>.

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