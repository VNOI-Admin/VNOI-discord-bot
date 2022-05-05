import discord
from discord import app_commands

from databases import data_util

@app_commands.command(description="Set the default channel to ask a question")
async def set_default_channel(interaction: discord.Interaction, channel_mention: str):
    await interaction.response.defer()

    if interaction.user.guild_permissions.administrator is False:
        await interaction.followup.send("You need administrator permission to use that command!")

    guild_list = list(data_util.select_guilds(guild_id=interaction.guild_id))
    channel_id = channel_mention[2:-1]

    if len(guild_list) == 0:
        data_util.insert_guild(guild_id=interaction.guild_id, default_channel_id=channel_id)
        await interaction.followup.send(f"The default ask channel set to {channel_mention}")
    elif len(guild_list) == 1:
        guild_id = guild_list[0].guild_id
        data_util.update_guild_information(guild_id, channel_id)
        await interaction.followup.send(f"Updated default ask channel to {channel_mention}")
    elif len(guild_list) > 1:
        print("Something went wrong!")
        await interaction.followup.send("Code bugged, panic!")

async def setup(bot, tree):
    for guild in bot.guilds:
        tree.add_command(set_default_channel, guild=discord.Object(id=guild.id))
