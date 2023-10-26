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

    async def staff_exists(self, tg: str) -> bool:
        result = await self.connection.fetchrow('SELECT tg FROM staff WHERE tg = $1', tg)
        return False if result is None else True

    async def user_is_registered(self, tg: str) -> bool:
        result = await self.connection.fetchrow('SELECT class FROM users WHERE tg = $1', tg)
        return False if dict(result)['class'] is None else True

    async def get_all_users(self) -> list:
        result = await self.connection.fetch('SELECT tg FROM users')
        return [dict(i)['tg'] for i in list(result)]

    async def get_users_by_building(self, building: str) -> list:
        result = await self.connection.fetch('SELECT tg FROM users WHERE building = $1', building)
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

    async def count_registered_users(self) -> int:
        result = await self.connection.fetchval("SELECT COUNT(tg) FROM users WHERE class <> ''")
        return result

    async def count_staff(self) -> int:
        result = await self.connection.fetchval('SELECT COUNT(tg) FROM staff')
        return result

    async def get_role(self, tg: str) -> str:
        result = await self.connection.fetchrow('SELECT role FROM staff WHERE tg = $1', tg)
        return dict(result)['role']

    async def get_username_by_tg(self, tg: str) -> str:
        result = await self.connection.fetchrow('SELECT username FROM users WHERE tg = $1', tg)
        return dict(result)['username']

# INSERT ===============================================================================================================
    async def new_user(self, tg: str, username: str):
        await self.connection.execute('INSERT INTO users (tg, username) VALUES ($1, $2)', tg, username)

    async def new_staff(self, tg: str, role: str, username: str):
        await self.connection.execute('INSERT INTO staff (tg, role, username) VALUES ($1, $2, $3)', tg, role, username)

# UPDATE ===============================================================================================================
    async def edit_group(self, tg: str, group: str) -> None:
        await self.connection.execute('UPDATE users set class = $1 WHERE tg = $2', group, tg)

    async def edit_building(self, tg: str, building: str) -> None:
        await self.connection.execute('UPDATE users set building = $1 WHERE tg = $2', building, tg)

    async def edit_role(self, tg: str, role: str, username: str) -> None:
        await self.connection.execute('UPDATE staff set role = $1, username = $2 WHERE tg = $3', role, username, tg)


# db = DB()
#
#
# async def main():
#     await db.connect()
#     print(await db.new_staff('1200522770', 'admin', 'matvey'))
#
# asyncio.run(main())
