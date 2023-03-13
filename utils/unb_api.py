import os
import aiohttp

_unb_api_token = os.getenv('UNB_API_TOKEN')


async def add_money(user, amount, _reason = None):
    url = f'https://unbelievaboat.com/api/v1/guilds/{user.guild.id}/users/{user.id}'
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"{_unb_api_token}"
    }

    payload = {
        "bank": amount,
    }

    if reason:
        payload["reason"] = _reason

    async with aiohttp.ClientSession(headers=headers) as session:
        await session.post(url, data = payload)