import asyncio

import asyncpg

from bot import config


class DB:
    def __init__(self):
        self.connection = None

    async def connect(self):
        self.connection = await asyncpg.connect(user=config.POSTGRES_USER,
                                                password=config.POSTGRES_PASSWORD,
                                                host=config.POSTGRES_HOST,
                                                port=config.POSTGRES_PORT,
                                                database=config.POSTGRES_DB)

# SELECT ===============================================================================================================
    async def user_exists(self, tg: str) -> bool:
        result = await self.connection.fetchrow('SELECT tg FROM users WHERE tg = $1', tg)
        return False if result is None else True

    async def user_is_registered(self, tg: str) -> bool:
        result = await self.connection.fetchrow('SELECT class FROM users WHERE tg = $1', tg)
        return False if dict(result)['class'] is None else True

    async def get_users(self) -> list:
        result = await self.connection.fetch('SELECT tg FROM users')
        return [dict(i)['tg'] for i in list(result)]

    async def get_class(self, tg: str) -> str:
        result = await self.connection.fetchrow('SELECT class FROM users WHERE tg = $1', tg)
        return dict(result)['class']

    async def get_building(self, tg: str) -> str:
        result = await self.connection.fetchrow('SELECT building FROM users WHERE tg = $1', tg)
        return dict(result)['building']

    async def count_users(self) -> int:
        result = await self.connection.fetchval('SELECT COUNT(tg) FROM users')
        return result

# INSERT ===============================================================================================================
    async def new_user(self, tg: str, username: str):
        await self.connection.execute('INSERT INTO users (tg, username) VALUES ($1, $2)', tg, username)

# UPDATE ===============================================================================================================
    async def edit_group(self, tg: str, group: str) -> None:
        await self.connection.execute('UPDATE users set class = $1 WHERE tg = $2', group, tg)

    async def edit_building(self, tg: str, building: str) -> None:
        await self.connection.execute('UPDATE users set building = $1 WHERE tg = $2', building, tg)


# db = DB()
#
#
# async def main():
#     await db.connect()
#     print(await db.edit_class('886971306', '1а'))
#
# asyncio.run(main())
