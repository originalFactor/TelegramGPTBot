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