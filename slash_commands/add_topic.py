import discord
from discord import app_commands

from databases import data_util

@app_commands.command(name = "add_topic", description = "Add a topic to ask in a channel")
async def add_topic(interaction: discord.Interaction, topic: str, channel_mention: str):
    await interaction.response.defer(ephemeral=False)

    channel_has_topic = list(data_util.select_topics(topic_name=topic, guild_id=interaction.guild_id))

    if len(channel_has_topic) > 0:
        await interaction.followup.send(f"Already has {topic} in <#{channel_has_topic[0].channel_id}>")
        return    

    for channel in interaction.guild.channels:
        if str(channel.mention) == channel_mention:
            data_util.insert_topic(topic_name = topic, guild_id = interaction.guild_id, channel_id = channel.id)
            await interaction.followup.send(f"Added {topic} for {channel.mention}")
            return

    await interaction.followup.send("Invalid Channel!")

async def setup(bot, tree):
    for guild in bot.guilds:
        tree.add_command(add_topic, guild=discord.Object(id=guild.id))