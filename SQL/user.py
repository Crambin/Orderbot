class User:
    def __init__(self, db):
        self.db = db

    async def update_balance(self, *record):
        await self.db.process_sql("""INSERT INTO UserTbl(UserID, DisplayName, Balance) VALUES ($1, $2, $3)
                                     ON CONFLICT (UserID) DO UPDATE
                                     SET DisplayName = $2,
                                         Birthday = $3""",
                                  *record)

    async def update_birthday(self, *record):
        await self.db.process_sql("""INSERT INTO UserTbl(UserID, DisplayName, Birthday) VALUES ($1, $2, $3)
                                     ON CONFLICT (UserID) DO UPDATE
                                     SET DisplayName = $2,
                                         Birthday = $3""",
                                  *record)

    async def fetch_birthday(self, user_id):
        return await self.db.process_sql("SELECT Birthday FROM UserTbl WHERE UserID = $1", user_id)

    async def fetch_all_birthdays(self):
        return await self.db.process_sql("SELECT UserID, Birthday FROM UserTbl "
                                         "WHERE Birthday IS NOT NULL "
                                         "ORDER BY EXTRACT(MONTH FROM Birthday), "
                                         "         EXTRACT(DAY FROM Birthday)")

    async def delete_birthday(self, user_id):
        await self.db.process_sql("DELETE FROM UserTbl WHERE UserID = $1", user_id)
