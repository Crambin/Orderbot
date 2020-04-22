import logging
import traceback
import discord
from discord.ext import commands
import constants

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    error_log_channel_id = 690650346665803777

    def __init__(self, prefix, *args, **kwargs):
        super().__init__(*args, command_prefix=prefix, **kwargs)

    async def on_ready(self):
        logger.info(f"Successfully logged in as {self.user.name} ID:{self.user.id}\t"
                    f"d.py version: {discord.__version__}")

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
