import discord
from discord import app_commands

@app_commands.command(description="Format for question command")
async def format(interaction: discord.Interaction):
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

async def setup(bot, tree):
    for guild in bot.guilds:
        tree.add_command(format, guild=discord.Object(id=guild.id))
