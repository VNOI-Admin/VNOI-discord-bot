from unittest import async_case
import discord
from discord import app_commands

from databases import data_util

@app_commands.command(description="List of all topic")
async def topics(interactions: discord.Interaction):
    await interactions.response.defer()

    embed = ""
    list_of_topic = data_util.select_topics(guild_id=interactions.guild_id)
    for topic in list_of_topic:
        embed += f"{topic.topic_name} in <#{topic.channel_id}>\n"

    if len(embed) == 0:
        embed = "There was no topic added, try using \move_topic"

    await interactions.followup.send(embed)

async def setup(bot, tree):
    for guild in bot.guilds:
        tree.add_command(topics, guild=discord.Object(id=guild.id))
