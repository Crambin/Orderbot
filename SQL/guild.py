class Guild:
    def __init__(self, db):
        self.db = db

    async def insert(self, *record):
        await self.db.process_sql("INSERT INTO GuildTbl(GuildID, Prefix) VALUES ($1, $2)", *record)

    async def update(self, guild_id, *record):
        await self.db.process_sql("UPDATE GuildTbl SET Prefix = ($1) WHERE GuildID = ($2)",
                                  *record, guild_id)

    async def get_prefixes(self):
        cur = await self.db.process_sql("SELECT GuildID, Prefix FROM GuildTbl")
        guild_prefixes = dict(map(tuple, cur))
        return guild_prefixes
