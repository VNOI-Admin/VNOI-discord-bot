import discord
from discord import app_commands

from databases import data_util

@app_commands.command(name="search", description="Find a similar problem")
async def search(interaction: discord.Interaction, query: str):
    await interaction.response.defer(ephemeral=True)

    matched_questions = data_util.related_questions(query)
    for questions in matched_questions:
        questions.query = query

    embed = ""
    for question in matched_questions:
        embed += f"<#{question.thread_id}>\n"
    await interaction.followup.send(embed)

async def setup(bot, tree):
    for guild in bot.guilds:
        tree.add_command(search, guild=discord.Object(id=guild.id))
