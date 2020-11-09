import os
import re
import asyncio
import logging
import traceback
from datetime import datetime

import discord
from discord.ext import commands
import SQL
import constants


logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, command_prefix=Bot.get_prefix, **kwargs)
        self.start_time = datetime.now()
        self.guild_prefixes = None
        self.db = None

    async def on_connect(self):
        self.db = await SQL.Database.create(os.getenv('DATABASE_URL'))
        self.guild_prefixes = await self.db.guild.get_prefixes()
        logger.info("Loaded guild prefixes into memory")

    def get_cog(self, name):
        # this is really hacky and is probably a sin, could break something
        return super().get_cog(name.capitalize())

    async def get_prefix(self, message):
        mention = re.match(rf"<@!{self.user.id}>\s*", message.content)
        if mention:
            return mention.group()

        if not message.guild:
            return constants.default_prefix

        prefix = self.guild_prefixes.get(message.guild.id, None)
        if prefix is None:
            prefix = constants.default_prefix
            self.guild_prefixes[message.guild.id] = prefix
            await self.db.guild.insert(message.guild.id, prefix)

        return prefix

    async def on_ready(self):
        logger.info(f"discord.py version: {discord.__version__}")
        logger.info(f"Successfully logged in as {self.user}   ID: {self.user.id}")

    async def on_guild_join(self, _guild):
        await self.update_presence()

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
        num_guilds = len(self.guilds)
        num_users = sum(guild.member_count for guild in self.guilds)
        stats_message = f"{num_guilds} servers and {num_users} users"

        # status automatically set to online if env does not exist
        status = os.getenv("STATUS") or 'online'
        await self.change_presence(status=status,
                                   activity=discord.Activity(name=stats_message,
                                                             type=discord.ActivityType.watching))

        logger.info(f"Updated presence: {num_guilds} servers and {num_users} users")

    async def scheduled_presence_update(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await self.update_presence()
            await asyncio.sleep(60 * 60)  # 60 minutes
