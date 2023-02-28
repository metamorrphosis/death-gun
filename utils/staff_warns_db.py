import os
import asyncio
from datetime import datetime, timedelta

import discord
from motor.motor_asyncio import AsyncIOMotorClient


class StaffWarnsDB:
    def __init__(self):
        self.cluster = AsyncIOMotorClient(os.getenv("MONGODB_LINK"))
        self.warns = self.cluster["warns"]["staff_warns"]
    
    async def insert_warn(self, *, author, member, reason):
        _id = await self.warns.find_one({"_id": 0})["count"]
        await self.warns.update_one({"_id": 0}, {"$inc": {"count": 1}})
        new_warn = {}
        new_warn["_id"] = _id
        new_warn["author"] = author.id
        new_warn["member"] = member.id
        new_warn["time"] = int(datetime.timestamp(datetime.now()))
        new_warn["reason"] = reason
        await self.warns.insert_one(new_warn)
        return _id

    async def remove_warn(self, *, _id):
        if await self.warns.find_one({"_id": _id}) is not None:
            await self.warns.delete_one({"_id":_id})
            return True
        else:
            return False

    async def get_warns(self, *, member):
        result = []
        async for i in self.warns.find():
            if i["_id"] == 0:
                continue
            
            if i["member"] == member.id:
                result.append(i)
        
        return result