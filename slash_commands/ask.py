import discord
from discord import app_commands
from discord.ext import commands
from utils import judge_api

import config

from databases import data_util

PLATFORM_LIST = ['Codeforces', 'Atcoder', 'VNOJ']
PLATFORM_LIST.sort()

@app_commands.command(name = "add_topic", description = "Add a topic to ask in a channel")
async def add_topic(interaction: discord.Interaction, topic: str, channel_mention: str):
    await interaction.response.defer(ephemeral = False)

    channel_has_topic = data_util.select_topics(topic_name = topic)

    if len(channel_has_topic) > 0:
        await interaction.followup.send(f"Already has {topic} in <#{channel_has_topic[0].channel_id}>")
        return    

    for channel in interaction.guild.channels:
        if str(channel.mention) == channel_mention:
            data_util.insert_topic(topic_name = topic, guild_id = interaction.guild_id, channel_id = channel.id)
            await interaction.followup.send(f"Added {topic} for {channel.mention}")
            return

    await interaction.followup.send("Invalid Channel!")

@app_commands.command(name="ask", description="Create a thread to get help on a problem")
async def ask(interaction: discord.Interaction, platform: str, problem_id: str):
    ask_channel = interaction.client.get_channel(config.ask_channel)

    problem_name = problem_id

    await interaction.response.defer(ephemeral=True)

    if platform in PLATFORM_LIST:
        problem_name = await judge_api.fetch_problem_name(platform.lower(), problem_id)
        if not problem_name:
            await interaction.followup.send("Invalid problem ID, please find more info about problem ID format with `/format` command", ephemeral=True)
            return

    new_thread = await ask_channel.create_thread(name=f'{platform} - {problem_name}', type=discord.ChannelType.public_thread, auto_archive_duration=60 * 24)

    data_util.insert_thread(thread_id=new_thread.id, judge=platform,
                     problem_name=problem_name, problem_id=problem_id)
    await new_thread.send(f'Your thread has been created, {interaction.user.mention}')
    await interaction.followup.send(f"Your thread has been created in {ask_channel.mention}", ephemeral=True)

@ask.autocomplete("platform")
async def platform_autocomplete(interaction: discord.Interaction, current: str):
    hint = [platform for platform in PLATFORM_LIST if current.lower()
            in platform.lower()]

    return [
        app_commands.Choice(name=platform, value=platform)
        for platform in hint
    ]

@app_commands.command(name = "format", description = "Format for question command")
async def format(interaction: discord.Interaction):
    used_channel = interaction.client.get_channel(config.ask_channel)

    await interaction.response.defer(ephemeral=True, thinking=False)

    embed = """```With Codeforces problems, problem id is contest id with problem index,
for example: https://codeforces.com/problemset/problem/1666/L the problem id is 1666L.
With Atcoder and VNOJ problems, problem id is the last part of the url, for example:
https://oj.vnoi.info/problem/bedao_r05_factory problem id is bedao_r05_factory.
With problems does not belong to all these judge, please give a valid platform/topic.
Some examples commands:
/ask platform: codeforces problem_id: 1666L
/ask platform: atcoder problem_id: keyence2021_d
/ask platform: VNOJ problem_id: bedao_r05_factory
/ask platform: HSG problem_id: paint```"""    
    await interaction.followup.send(embed)

@app_commands.command(name = "search", description = "Find a similar problem")
async def search(interaction: discord.Interaction, query: str):
    await interaction.response.defer(ephemeral=True)

    matched_questions = data_util.related_questions(query)
    for questions in matched_questions:
        questions.query = query   
        """Will be used for searching algorithm""" 

    embed = ""
    for question in matched_questions:
        embed += f"<#{question.thread_id}>\n"
    await interaction.followup.send(embed)

async def setup(bot, tree):
    tree.add_command(ask, guild = discord.Object(id = config.guild_id))
    tree.add_command(format, guild = discord.Object(id = config.guild_id))
    tree.add_command(search, guild = discord.Object(id = config.guild_id))
    tree.add_command(add_topic, guild = discord.Object(id = config.guild_id))