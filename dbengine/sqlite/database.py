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

from sqlite3 import connect, Connection, Cursor
from .table import Table
from ..template.database import DatabaseOrigin

# 数据库类
class Database(DatabaseOrigin):
    # 初始化
    def _init(self, name:str='./database.db', threadId:int=0, *args, **kwargs):
        self.connection:Connection = connect(name)
        self.cursors:dict[int,Cursor] = {}
        for tableName in list((self.getCursor(threadId)).execute('SELECT name FROM sqlite_master WHERE type="table"')):
            self.tables[tableName] = Table(self, tableName)
    # [SQL独有] 获取cursor 
    def getCursor(self, threadId:int=0, *args, **kwargs)->Cursor:
        if threadId not in self.cursors.keys():
            self.cursors[threadId] = self.connection.cursor()
        return self.cursors[threadId]
    async def _create(self, name:str, create:list[tuple[str]], threadId:int=0, *args, **kwargs):
        self.getCursor(threadId).execute(f'CREATE TABLE {name} ({",".join([_+" "+" ".join(create[_]) for _ in create.keys()])})')
        self.connection.commit()
    async def _remove(self, name:str, threadId:int=0, *args, **kwargs):
        if name in self.tables.keys():
            self.getCursor(threadId).execute(
                f"DROP TABLE {name}"
            )
            del self.tables[name]