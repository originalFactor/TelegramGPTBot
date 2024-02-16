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