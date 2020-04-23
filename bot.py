import os
import re
import json
import logging
import traceback
import asyncio
import discord
from discord.ext import commands
import constants
import SQL

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, command_prefix=Bot.get_prefix, case_insensitive=True, **kwargs)
        self.db = SQL.Database(os.getenv('DATABASE_URL'))
        self.mention_pattern = None

    async def get_prefix(self, message):
        mention = re.match(rf"<@!{self.user.id}>\s*", message.content)
        if mention:
            return mention.group()

        prefix = self.db.get_prefix(message.guild.id)
        if not prefix:
            prefix = constants.default_prefix
            self.db.insert_guild(message.guild.id, prefix)

        return prefix[0]

    async def on_ready(self):
        logger.info(f"discord.py version: {discord.__version__}")
        logger.info(f"Successfully logged in as {self.user}   ID: {self.user.id}")

    async def on_message(self, message):
        if not self.is_ready():
            return

        await self.process_commands(message)

    async def on_error(self, event, *args):
        msg = f"{event} event error exception!\n{traceback.format_exc()}"
        logger.critical(msg)
        await self.log_error(msg)

    async def log_error(self, message):
        if not self.is_ready() or self.is_closed():
            return

        error_log_channel = self.get_channel(constants.error_log_channel_id)

        num_messages = 1 + len(message) // 1981
        split_messages = (message[i:i + 1980] for i in range(0, len(message), 1980))
        for count, message in enumerate(split_messages, 1):
            await error_log_channel.send(f"```Num {count}/{num_messages}:\n{message}```")

    async def update_presence(self):
        await self.wait_until_ready()
        while not self.is_closed():
            num_guilds = len(self.guilds)
            num_users = sum(len(guild.members) for guild in self.guilds)
            stats_message = f"{num_guilds} servers and {num_users} users"

            status = os.getenv("STATUS")
            if status is None:
                status = 'online'

            await self.change_presence(status=status,
                                       activity=discord.Activity(type=discord.ActivityType.watching,
                                                                 name=stats_message))
            logger.info(f"Updated presence: {num_guilds} servers and {num_users} users")
            await asyncio.sleep(60 * 15)  # 15 minutes
