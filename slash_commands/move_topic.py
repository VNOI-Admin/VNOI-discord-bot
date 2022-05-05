import discord
from discord import Interaction, app_commands

from databases import data_util

@app_commands.command(description="Move a topic to ask in a channel")
async def move_topic(interaction: discord.Interaction, topic: str, channel_mention: str):
    await interaction.response.defer(ephemeral=False)

    channel_has_topic = list(data_util.select_topics(topic_name=topic, guild_id=interaction.guild_id))

    for channel in interaction.guild.channels:
        if str(channel.mention) == channel_mention:

            if len(channel_has_topic) == 0:
                await interaction.followup.send(f"Added {topic} for {channel.mention}")
                data_util.insert_topic(topic_name=topic, guild_id=interaction.guild_id, channel_id=channel.id)

            elif len(channel_has_topic) == 1:
                channel_id = channel_mention[2:-1]
                data_util.update_topic_information(topic_name=topic, guild_id=interaction.guild_id, channel_id=int(channel_id))
                await interaction.followup.send(f"Moved {topic} from <#{channel_has_topic[0].chancnel_id}> to {channel.mention}")

            elif len(channel_has_topic) > 1:
                print("Something went wrong!")
                await interaction.followup.send("Code bugged, panic!")

            return

    await interaction.followup.send("Invalid Channel!")

async def setup(bot, tree):
    for guild in bot.guilds:
        tree.add_command(move_topic, guild=discord.Object(id=guild.id))
