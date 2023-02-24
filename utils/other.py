import discord
from datetime import datetime, timedelta

async def auto_role(interaction, role_id):
    if role in member.roles:
        await member.remove_roles(role)
        return f'Успешно снял у вас роль {role.mention}'
    else:
        await member.add_roles(role)
        return f'Успешно выдал вам роль {role.mention}'