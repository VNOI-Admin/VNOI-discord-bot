import os
import dotenv

import discord
from discord.ext import commands
from discord import app_commands

import config

dotenv.load_dotenv()

class VNOIBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = "?", intents = discord.Intents.all())
        self.is_running = False

        if not self._connection._command_tree: self._connection._command_tree = app_commands.CommandTree(self)

    async def load_slash_commands(self, module):
        await __import__(module, fromlist = [None]).setup(self, self._connection._command_tree)

    async def on_ready(self):
        if not self.is_running:
            self.is_running = True
            await self.load_slash_commands("slash_commands.ask")

        await self._connection._command_tree.sync(guild = discord.Object(id = 701626107417460766))    

        print('Ready')
        print('Connected guilds:')
        for i in self.guilds:
            print(f"[+] {i.name}")

bot = VNOIBot()

bot.run(config.token)