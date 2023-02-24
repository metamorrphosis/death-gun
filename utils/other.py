import discord
from datetime import datetime, timedelta

async def auto_role(interaction, role_id):
    _role = interaction.guild.get_role(int(role_id))

    if _role in interaction.user.roles:
        await interaction.user.remove_roles(_role)
        await interaction.response.send_message(f'Успешно снял у вас роль {_role.mention}', ephemeral = True)
    else:
        await interaction.user.add_roles(_role)
        await interaction.response.send_message(f'Успешно выдал вам роль {_role.mention}', ephemeral = True)