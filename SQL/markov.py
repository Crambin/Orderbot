import json


class Markov:
    def __init__(self, db):
        self.db = db

    async def insert(self, name, pairs):
        pairs = json.dumps(pairs)
        await self.db.process_sql("""INSERT INTO MarkovTbl(Name, WordPairs) VALUES ($1, $2)
                                     ON CONFLICT (Name) DO UPDATE
                                     SET Name = $1,
                                         WordPairs = $2""",
                                  name, pairs)

    async def fetch(self, name):
        cur = await self.db.process_sql("SELECT WordPairs FROM MarkovTbl WHERE Name = ($1)", name)
        if cur:
            return json.loads(dict(cur[0])['wordpairs'])
        return None

    async def get_tags(self):
        cur = await self.db.process_sql("SELECT Name FROM MarkovTbl")
        return (item['name'] for item in cur)
