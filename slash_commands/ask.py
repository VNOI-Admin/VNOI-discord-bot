import discord
from discord import app_commands
from discord.ext import commands

import config

PLATFORM_LIST = ['Codeforces', 'Codechef', 'Hackerearth', 'Atcoder', 'Topcoder', 'Hackerrank', 'Leetcode', 'DMOJ', 'VNOJ', 'Project Euler', 'USACO', 'SPOJ']
PLATFORM_LIST.sort()

@app_commands.command(name = "ask", description = "Tạo thread để hỏi bài")
async def ask(interaction: discord.Interaction, platform: str, problem_id: str):
    ask_channel = interaction.client.get_channel(config.ask_channel)
    new_thread = await ask_channel.create_thread(name = f'{platform} - {problem_id}', type = discord.ChannelType.public_thread, auto_archive_duration = 60 * 24)
    
    await new_thread.send(f'Thread của bạn đã được tạo, {interaction.user.mention}')
    await interaction.response.send_message(f"Thread của bạn đã được tạo ở {ask_channel.mention}", ephemeral = True)

@ask.autocomplete("platform")
async def platform_autocomplete(interaction: discord.Interaction, current: str):
    hint = [platform for platform in PLATFORM_LIST if current.lower() in platform.lower()]
    
    return [
        app_commands.Choice(name = platform, value = platform)
        for platform in hint
    ]

async def setup(bot, tree):
    tree.add_command(ask, guild = discord.Object(id = 701626107417460766))