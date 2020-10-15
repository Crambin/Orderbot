import logging
import asyncpg

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.conn = None

    @classmethod
    async def create(cls, database_url):
        self = cls()
        self.conn = await asyncpg.connect(database_url)
        await self.create_tables()

        logger.info("Successfully connected to SQL database.")
        return self

    async def create_tables(self):
        tables_sql = ("""
        CREATE TABLE IF NOT EXISTS GuildTbl(
                GuildID     BIGINT          NOT NULL    UNIQUE      PRIMARY KEY,
                Prefix      VARCHAR(15)     NOT NULL
                );""",)

        for sql in tables_sql:
            await self.process_sql(sql)

    async def process_sql(self, sql, *parameters):
        records = []
        async with self.conn.transaction():
            async for record in self.conn.cursor(sql, *parameters):
                records.append(record)

        return records

    # guilds
    async def insert_guild(self, *record):
        await self.process_sql("INSERT INTO GuildTbl(GuildID, Prefix) VALUES ($1, $2)", *record)

    async def update_guild(self, guild_id, *record):
        await self.process_sql("UPDATE GuildTbl SET Prefix = ($1) WHERE GuildID = ($2)",
                               *record, guild_id)

    async def get_guild_prefixes(self):
        cur = await self.process_sql("SELECT GuildID, Prefix FROM GuildTbl")
        guild_prefixes = dict(map(tuple, cur))
        return guild_prefixes
