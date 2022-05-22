import discord
from discord.ext import commands
from discord import app_commands

from utils import judge_utils

from databases import data_util

PLATFORM_LIST = ['Codeforces', 'Atcoder', 'VNOJ', 'Codechef']
PLATFORM_LIST.sort()


class AskCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ask", description="Create a thread to get help on a problem")
    @app_commands.describe(
        topic="What you want to ask about.",
        problem="What your problem is."
    )
    async def ask(self, interaction: discord.Interaction, topic: str, problem: str):
        await interaction.response.defer(ephemeral=True)

        guild_information = list(
            data_util.select_guilds(guild_id=interaction.guild_id))
        topic_information = list(data_util.select_topics(
            topic_name=topic, guild_id=interaction.guild_id))

        if len(topic_information) == 0:
            if len(guild_information) == 0:
                await interaction.followup.send("There is no default channel and no channel has this topic")
                return

            if len(guild_information) == 1:
                ask_channel_id = guild_information[0].default_channel_id
                ask_channel = interaction.guild.get_channel(ask_channel_id)

            if len(guild_information) > 1:
                print("Something went wrong!")
                await interaction.followup.send("Code bugged, panic!")
                return

        if len(topic_information) == 1:
            ask_channel_id = topic_information[0].channel_id
            ask_channel = interaction.guild.get_channel(ask_channel_id)

        if len(topic_information) > 2:
            print("Something went wrong!")
            await interaction.followup.send("Code bugged, panic!")
            return

        problem_name = problem

        if topic in PLATFORM_LIST:
            problem_name = await judge_utils.fetch_problem_name(topic.lower(), problem)
            if not problem_name:
                await interaction.followup.send("Invalid problem ID, please find more info about problem ID format with `/format` command", ephemeral=True)
                return

        new_thread = await ask_channel.create_thread(name=f'{topic} - {problem_name}', type=discord.ChannelType.public_thread, auto_archive_duration=60 * 24)

        data_util.insert_thread(thread_id=new_thread.id, judge=topic,
                                problem_name=problem_name, problem=problem)
        await new_thread.send(f'Your thread has been created, {interaction.user.mention}')
        await interaction.followup.send(f"Your thread has been created in {ask_channel.mention}", ephemeral=True)

    @ask.autocomplete("topic")
    async def topic_autocomplete(self, interaction: discord.Interaction, current: str):
        hint = []
        topic_list = data_util.select_topics(guild_id=interaction.guild_id)

        topic_list = [topic.topic_name for topic in topic_list] + PLATFORM_LIST

        for topic in topic_list:
            if current in topic:
                hint.append(topic)

        return [
            app_commands.Choice(name=topic, value=topic)
            for topic in hint
        ]

    @app_commands.command(description="Format for question command")
    async def format(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=False)

        embed = discord.Embed(
            title="",
            description="""**[+]** With Codeforces problems, `problem` is contest id with problem index, for example: 
for `https://codeforces.com/problemset/problem/1666/L`, `problem` is 1666L.

**[+]** With Atcoder and VNOJ problems, `problem` is the last part of the url, for example:
for `https://oj.vnoi.info/problem/bedao_r05_factory`, `problem` is bedao_r05_factory.

**[+]** With problems does not belong to all these judge, please give a valid topic.

**[+]** Some examples commands:
`/ask topic: codeforces, problem: 1666L`
`/ask topic: atcoder, problem: keyence2021_d`
`/ask topic: VNOJ, problem: bedao_r05_factory`
`/ask topic: HSG, problem: paint`""",
            color=0xffcccb
        )
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="search", description="Find a similar problem")
    @app_commands.describe(
        topic="The topic of what you want to search for. This can be anything but if you want more accurate results, do specify the correct topic.",
        query="What you want to search for."
    )
    async def search(self, interaction: discord.Interaction, topic: str, query: str):
        problem_name = None

        if topic in [platform.lower() for platform in PLATFORM_LIST]:
            problem_name = await judge_utils.fetch_problem_name(topic.lower(), query)

        await interaction.response.defer(ephemeral=True)

        matched_questions = data_util.related_questions(query, problem_name)
        for questions in matched_questions:
            questions.query = query

        embed = ""
        for question in matched_questions:
            embed += f"<#{question.thread_id}>\n"
        await interaction.followup.send(embed)

    @search.autocomplete("topic")
    async def topic_autocomplete(self, interaction: discord.Interaction, current: str):
        hint = []

        for topic in PLATFORM_LIST:
            if current in topic:
                hint.append(topic)

        return [
            app_commands.Choice(name=topic, value=topic)
            for topic in hint
        ]


async def setup(bot):
    await bot.add_cog(AskCommands(bot), guild=discord.Object(id=701626107417460766))
