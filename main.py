import os

import discord
from discord.ext import commands
from discord import app_commands

import config


class VNOIBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="?", intents=discord.Intents.all())
        self.is_running = False

        if not self._connection._command_tree:
            self._connection._command_tree = app_commands.CommandTree(self)

    async def on_ready(self):
        if not self.is_running:
            self.is_running = True

            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    await bot.load_extension(f'cogs.{filename[:-3]}')

        await self.tree.sync(guild=discord.Object(id=701626107417460766))

        print('Ready')
        print('Connected guilds:')

        for guild in self.guilds:
            await self._connection._command_tree.sync(guild=discord.Object(id=guild.id))
            print(f"[+] {guild.name}")


bot = VNOIBot()

bot.run(config.token)
