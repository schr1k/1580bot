import asyncpg
import asyncio

import config


class DB:
    def __init__(self):
        self.connection = None

    async def connect(self):
        self.connection = await asyncpg.connect(user=config.POSTGRES_USER,
                                                password=config.POSTGRES_PASSWORD,
                                                host=config.POSTGRES_HOST,
                                                port=config.POSTGRES_PORT,
                                                database=config.POSTGRES_DB)

    async def user_exists(self, tg):
        result = await self.connection.fetchrow('SELECT tg FROM users WHERE tg = $1', tg)
        return False if result is None else True

    async def new_user(self, tg, username):
        await self.connection.execute('INSERT INTO users (tg, username) VALUES ($1, $2)', tg, username)


# db = DB()
#
#
# async def main():
#     await db.connect()
#     print(await db.new_user('123', 'abc'))
#
# asyncio.run(main())
