import discord
from discord import app_commands

from databases import data_util

@app_commands.command(description="Default channel to ask a question")
async def default_channel(interaction: discord.Interaction):
    await interaction.response.defer()

    guild_information = list(data_util.select_guilds(guild_id=interaction.guild_id))
    if len(guild_information) == 0:
        await interaction.followup.send("This server does not have a default channel")
    elif len(guild_information) == 1:
        current_guild = guild_information[0]
        await interaction.followup.send(f"Default ask channel: <#{current_guild.default_channel_id}>")
    elif len(guild_information) == 2:
        print("Something went wrong!")
        await interaction.followup.send("Code bugged, panic!")
    
async def setup(bot, tree):
    for guild in bot.guilds:
        tree.add_command(default_channel, guild=discord.Object(id=guild.id))
