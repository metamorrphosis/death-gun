import os
import json
import aiohttp

_unb_api_token = os.getenv('UNB_API_TOKEN')

async def update_money(*, member, amount, reason = None):
    url = f'https://unbelievaboat.com/api/v1/guilds/{member.guild.id}/users/{member.id}'
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"{_unb_api_token}"
    }

    payload = {
        "bank": amount,
    }

    if reason:
        payload["reason"] = reason

    async with aiohttp.ClientSession(headers = headers) as session:
        async with session.patch(url, data = json.dumps(payload).encode('utf-8')) as resp:
            pass