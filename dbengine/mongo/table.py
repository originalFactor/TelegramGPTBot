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
from pymongo.collection import Collection
from typing import Union

class Table(TableOrigin):
    def _init(self, collection:Collection, *args, **kwargs):
        self.tb = collection
    async def _new(self, data:dict[str,any], *args, **kwargs):
        self.tb.insert_one(data)
    async def _get(self, query:dict[str,any], target:Union[tuple[str],dict[str,bool]]={}, *args, **kwargs)->list:
        return list([_.values() for _ in list(self.tb.find(query,projection=target))])
    async def _remove(self, query:dict[str,any], *args, **kwargs):
        self.tb.delete_many(query)