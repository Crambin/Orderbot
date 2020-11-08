from .guild import Guild

import logging
import asyncpg

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.conn = None
        self.guild = Guild(self)

    @classmethod
    async def create(cls, database_url):
        self = cls()
        self.conn = await asyncpg.connect(database_url)
        await self.create_tables()

        logger.info("Successfully connected to SQL database.")
        return self

    async def create_tables(self):
        with open('SQL/tables.sql') as f:
            await self.process_sql(f.read())

    async def process_sql(self, sql, *parameters):
        records = []
        async with self.conn.transaction():
            async for record in self.conn.cursor(sql, *parameters):
                records.append(record)

        return records
