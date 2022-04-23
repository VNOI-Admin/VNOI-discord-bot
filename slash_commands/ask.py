import discord
from discord import app_commands
from discord.ext import commands
from utils import judge_api

import config

from databases import data_util

PLATFORM_LIST = ['Codeforces', 'Atcoder', 'VNOJ']
PLATFORM_LIST.sort()

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

async def setup(bot, tree):
    for guild in bot.guilds:
        tree.add_command(ask, guild = discord.Object(id = guild.id))