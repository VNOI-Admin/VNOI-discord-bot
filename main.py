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

    async def load_slash_commands(self, module):
        await __import__(module, fromlist=[None]).setup(self, self._connection._command_tree)

    async def on_ready(self):
        if not self.is_running:
            self.is_running = True
            for available_slash_command in ["ask", "format", "search", "set_default_channel", "default_channel", "topics", "move_topic"]:
                await self.load_slash_commands(f"slash_commands.{available_slash_command}")

        print('Ready')
        print('Connected guilds:')

        for guild in self.guilds:
            await self._connection._command_tree.sync(guild=discord.Object(id=guild.id))
            print(f"[+] {guild.name}")

bot = VNOIBot()

bot.run(config.token)
