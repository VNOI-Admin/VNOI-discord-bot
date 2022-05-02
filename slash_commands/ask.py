import discord
from discord import app_commands

from utils import judge_api

import config

from databases import data_util

PLATFORM_LIST = ['Codeforces', 'Atcoder', 'VNOJ']
PLATFORM_LIST.sort()

@app_commands.command(name="ask", description="Create a thread to get help on a problem")
async def ask(interaction: discord.Interaction, platform: str, problem_id: str):
    await interaction.response.defer(ephemeral=True)

    guild_information = list(data_util.select_guilds(guild_id=interaction.guild_id))
    topic_information = list(data_util.select_topics(topic_name=platform, guild_id=interaction.guild_id))
    
    if len(topic_information) == 0:
        if len(guild_information) == 0:
            await interaction.followup.send("There is no default channel and no channel has this topic")
            return
        
        elif len(guild_information) == 1:
            ask_channel_id = guild_information[0].default_channel_id
            ask_channel = interaction.guild.get_channel(ask_channel_id)
        
        elif len(guild_information) > 1:
            print("Something went wrong!")
            await interaction.followup.send("Code bugged, panic!")
            return
    
    elif len(topic_information) == 1:
        ask_channel_id = topic_information[0].channel_id
        ask_channel = interaction.guild.get_channel(ask_channel_id)
    
    elif len(topic_information) > 2:
        print("Something went wrong!")
        await interaction.followup.send("Code bugged, panic!")
        return
    
    problem_name = problem_id

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
    TOPIC_LIST = data_util.select_topics()
    hint = []

    for topic in TOPIC_LIST:
        topic_name = topic.topic_name
        if current in topic_name:
            hint.append(topic_name)    

    return [
        app_commands.Choice(name=platform, value=platform)
        for platform in hint
    ]

async def setup(bot, tree):
    for guild in bot.guilds:
        tree.add_command(ask, guild=discord.Object(id=guild.id))