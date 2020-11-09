class User:
    def __init__(self, db):
        self.db = db

    async def update_birthday(self, *record):
        await self.db.process_sql("""INSERT INTO UserTbl(UserID, DisplayName, Birthday) VALUES ($1, $2, $3)
                                     ON CONFLICT (UserID) DO UPDATE
                                     SET DisplayName = $2,
                                         Birthday = $3""",
                                  *record)

    async def update_balance(self, *record):
        await self.db.process_sql("""INSERT INTO UserTbl(UserID, DisplayName, Balance) VALUES ($1, $2, $3)
                                     ON CONFLICT (UserID) DO UPDATE
                                     SET DisplayName = $2,
                                         Birthday = $3""",
                                  *record)
