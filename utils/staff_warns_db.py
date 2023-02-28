import os
import asyncio
from datetime import datetime, timedelta

import discord
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()


class StaffWarnsDB:
    def __init__(self):
        self.cluster = AsyncIOMotorClient(os.getenv("MONGODB_LINK"))
        self.warns = self.cluster["warns"]["staff_warns"]
    
    async def insert_warn(self, *, _id, author, member, reason):
        if await self.warns.find_one({"_id": _id}) is None:
            new_warn = {}
            new_warn["_id"] = _id
            new_warn["author"] = author.id
            new_warn["member"] = member.id
            new_warn["reason"] = reason
            await self.warns.insert_one(new_warn)
            return True
        else:
            return False

    async def remove_warn(self, *, _id):
        if await self.warns.find_one({"_id": _id}) is not None:
            await self.warns.delete_one({"_id":_id})
            return True
        else:
            return False

    async def get_warns(self, *, member):
        result = []
        async for i in self.warns.find():
            if i["member"] == member.id:
                result.append(i)
        
        return result