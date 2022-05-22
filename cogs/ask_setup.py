import discord
from discord.ext import commands
from discord import app_commands

from utils import judge_utils

from databases import data_util


class AskSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Set the default channel to ask a question")
    @app_commands.default_permissions(administrator=True)
    async def set_default_channel(self, interaction: discord.Interaction, channel_mention: str):
        await interaction.response.defer()

        guild_list = list(data_util.select_guilds(
            guild_id=interaction.guild_id))
        channel_id = channel_mention[2:-1]

        if len(guild_list) == 0:
            data_util.insert_guild(
                guild_id=interaction.guild_id, default_channel_id=channel_id)
            await interaction.followup.send(f"The default ask channel set to {channel_mention}")
        elif len(guild_list) == 1:
            guild_id = guild_list[0].guild_id
            data_util.update_guild_information(guild_id, channel_id)
            await interaction.followup.send(f"Updated default ask channel to {channel_mention}")
        elif len(guild_list) > 1:
            print("Something went wrong!")
            await interaction.followup.send("Code bugged, panic!")

    @app_commands.command(description="Default channel to ask a question")
    async def default_channel(self, interaction: discord.Interaction):
        await interaction.response.defer()

        guild_information = list(
            data_util.select_guilds(guild_id=interaction.guild_id))
        if len(guild_information) == 0:
            await interaction.followup.send("This server does not have a default channel")

        elif len(guild_information) == 1:
            current_guild = guild_information[0]
            await interaction.followup.send(f"Default ask channel: <#{current_guild.default_channel_id}>")

        elif len(guild_information) == 2:
            print("Something went wrong!")
            await interaction.followup.send("Code bugged, panic!")

    @app_commands.command(description="Move a topic to ask in a channel")
    @app_commands.default_permissions(administrator=True)
    async def move_topic(self, interaction: discord.Interaction, topic: str, channel_mention: str):
        await interaction.response.defer(ephemeral=False)

        channel_has_topic = list(data_util.select_topics(
            topic_name=topic, guild_id=interaction.guild_id))

        for channel in interaction.guild.channels:
            if str(channel.mention) == channel_mention:

                if len(channel_has_topic) == 0:
                    await interaction.followup.send(f"Added {topic} for {channel.mention}")
                    data_util.insert_topic(
                        topic_name=topic, guild_id=interaction.guild_id, channel_id=channel.id)

                elif len(channel_has_topic) == 1:
                    channel_id = channel_mention[2:-1]
                    data_util.update_topic_information(
                        topic_name=topic, guild_id=interaction.guild_id, channel_id=int(channel_id))
                    await interaction.followup.send(f"Moved {topic} from <#{channel_has_topic[0].channel_id}> to {channel.mention}")

                elif len(channel_has_topic) > 1:
                    print("Something went wrong!")
                    await interaction.followup.send("Code bugged, panic!")

                return

        await interaction.followup.send("Invalid Channel!")

    @app_commands.command(description="List of all topics")
    async def topics(self, interactions: discord.Interaction):
        await interactions.response.defer()

        embed = ""
        list_of_topic = data_util.select_topics(guild_id=interactions.guild_id)
        for topic in list_of_topic:
            embed += f"{topic.topic_name} in <#{topic.channel_id}>\n"

        if len(embed) == 0:
            embed = "There was no topic added, try using /move_topic"

        await interactions.followup.send(embed)


async def setup(bot):
    await bot.add_cog(AskSetup(bot), guild=discord.Object(id=701626107417460766))
