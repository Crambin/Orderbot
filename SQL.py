import logging
import psycopg2


logger = logging.getLogger(__name__)


class Database:
    def __init__(self, database_url):
        self.conn = psycopg2.connect(database_url, sslmode='require')
        self.create_tables()

        logger.info("Successfully connected to SQL database.")

    def create_tables(self):
        tables_sql = ("""
        CREATE TABLE IF NOT EXISTS GuildTbl(
                GuildID     BIGINT          NOT NULL    UNIQUE      PRIMARY KEY,
                Prefix      VARCHAR(15)     NOT NULL
                );""",)

        cur = self.conn.cursor()
        for table_sql in tables_sql:
            cur.execute(table_sql)

        cur.close()
        self.conn.commit()

    def process_sql(self, sql, parameters=()):
        cur = self.conn.cursor()
        cur.execute(sql, parameters)
        self.conn.commit()

        return cur

    # guilds
    def get_prefix(self, guild_id):
        cur = self.process_sql("SELECT Prefix FROM GuildTbl WHERE GuildID = (%s)", parameters=(guild_id,))
        try:
            return cur.fetchone()
        finally:
            cur.close()

    def insert_guild(self, *record):
        cur = self.process_sql("INSERT INTO GuildTbl(GuildID, Prefix) VALUES (%s, %s)", parameters=record)
        cur.close()

    def update_guild(self, guild_id, *record):
        cur = self.process_sql("UPDATE GuildTbl SET Prefix = (%s) WHERE GuildID = (%s)",
                               parameters=(*record, guild_id))
        cur.close()
