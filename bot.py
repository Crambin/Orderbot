import re
import json
import logging
import traceback
import discord
from discord.ext import commands
import constants

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, command_prefix=Bot.get_prefix, **kwargs)
        self.mention_pattern = None

    async def get_prefix(self, message):
        mention = self.mention_pattern.match(message.content)
        if mention:
            return mention.group()

        try:
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)
        except FileNotFoundError:
            prefixes = {}

        if f"{message.guild.id}" not in prefixes:
            prefixes[f"{message.guild.id}"] = '!'
            with open('prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)

        return prefixes[f"{message.guild.id}"]

    async def on_ready(self):
        logger.info(f"Successfully logged in as {self.user.name} ID:{self.user.id}\t"
                    f"d.py version: {discord.__version__}")

        self.mention_pattern = re.compile(rf"<@!{self.user.id}>\s*")

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

        error_log_channel = self.get_channel(constants.dev_log_channel)

        num_messages = 1 + len(message) // 1981
        split_messages = (message[i:i + 1980] for i in range(0, len(message), 1980))
        for count, message in enumerate(split_messages, 1):
            await error_log_channel.send(f"```Num {count}/{num_messages}:\n{message}```")
