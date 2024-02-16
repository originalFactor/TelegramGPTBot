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

from .origin import T, D

class TableOrigin(T):
    def _init(self, *args, **kwargs):
        pass
    def __init__(self, *args, **kwargs):
        self._init(*args, **kwargs)
    async def _new(self, *args, **kwargs):
        pass
    async def new(self, data:dict[str,any], *args, **kwargs):
        await self._new(data=data,*args,**kwargs)
    async def _get(self, *args, **kwargs)->list:
        return []
    async def get(self, query:dict[str,any], *args, **kwargs)->list:
        return await self._get(query, *args, **kwargs)
    async def _remove(self, *args, **kwargs):
        pass
    async def remove(self, query:dict[str,any], *args, **kwargs):
        await self._remove(query, *args, **kwargs)