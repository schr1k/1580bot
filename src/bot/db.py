import asyncpg

from src.config import Config

config = Config()


class DB:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            database=config.POSTGRES_DB,
            min_size=5,
            max_size=100,
        )

    # SELECT ===============================================================================================================
    async def user_exists(self, tg: str) -> bool:
        """
        Check if user exists
        :param tg: User telegram id
        :return: :class:`bool`: True if user exists else False
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT tg
            FROM users
            WHERE tg = $1
            """
            result = await connection.fetchval(query, tg)
            return False if result is None else True

    async def staff_exists(self, tg: str) -> bool:
        """
        Check if user is staff
        :param tg: User telegram id
        :return: :class:`bool`: True if user is staff else False
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT tg
            FROM staff
            WHERE tg = $1
            """
            result = await connection.fetchval(query, tg)
            return False if result is None else True

    async def user_is_registered(self, tg: str) -> bool:
        """
        Check if user is registered
        :param tg: User telegram id
        :return: :class:`bool`: True if user is registered else False
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT class
            FROM users
            WHERE tg = $1
            """
            result = await connection.fetchval(query, tg)
            return False if result is None else True

    async def get_all_users(self) -> list[str]:
        """
        Get all users
        :return: :class:`list` containing all users telegram ids
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT tg
            FROM users
            """
            result = await connection.fetch(query)
            return [dict(i)['tg'] for i in list(result)]

    async def get_users_by_building(self, building: str) -> list[str]:
        """
        Get all users in provided building
        :param building: Building id (1, 2, 3, 4)
        :return: :class:`list` containing users telegram ids in provided building
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT tg
            FROM users
            WHERE building = $1
            """
            result = await connection.fetch(query, building)
            return [dict(i)['tg'] for i in list(result)]

    async def get_group(self, tg: str) -> str:
        """
        Get class name of user with given telegram id
        :param tg: User telegram id
        :return: :class:`str`: user's class name (11с1)
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT class
            FROM users
            WHERE tg = $1
            """
            result = await connection.fetchrow(query, tg)
            return dict(result)['class']

    async def get_building(self, tg: str) -> str:
        """
        Get building id of user with given telegram id
        :param tg: User telegram id
        :return: :class:`str`: user's building id (1, 2, 3, 4)
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT building
            FROM users
            WHERE tg = $1
            """
            result = await connection.fetchrow(query, tg)
            return dict(result)['building']

    async def get_teacher(self, tg: str) -> str:
        """
        Get teacher's surname for user with given telegram id
        :param tg: User telegram id
        :return: :class:`str`: user's teacher name (11с1)
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT teacher
            FROM users
            WHERE tg = $1
            """
            result = await connection.fetchrow(query, tg)
            return dict(result)['teacher']

    async def count_users(self) -> int:
        """
        Get users amount
        :return: :class:`int`: total amount of users
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT COUNT(tg)
            FROM users
            """
            result = await connection.fetchval(query)
            return result

    async def count_registered_users(self) -> int:
        """
        Get amount of registered users
        :return: :class:`int`: amount of registered users
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT COUNT(tg)
            FROM users
            WHERE class <> ''
            """
            result = await connection.fetchval(query)
            return result

    async def count_staff(self) -> int:
        """
        Get staff amount
        :return: :class:`int`: total amount of staff
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT COUNT(tg)
            FROM staff
            """
            result = await connection.fetchval(query)
            return result

    async def get_role(self, tg: str) -> str:
        """
        Get user's role
        :return: :class:`str`: user's role
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT role
            FROM staff
            WHERE tg = $1
            """
            result = await connection.fetchrow(query, tg)
            return dict(result)['role']

    async def get_username_by_tg(self, tg: str) -> str:
        """
        Get user's username by telegram id
        :param tg: Telegram id
        :return: :class:`str`: user's username
        """
        async with self.pool.acquire() as connection:
            query = """
            SELECT username
            FROM users
            WHERE tg = $1
            """
            result = await connection.fetchrow(query, tg)
            return dict(result)['username']

    # INSERT ===============================================================================================================
    async def new_user(self, tg: str, username: str) -> None:
        """
        Create new user
        :param tg: Telegram id
        :param username: Telegram username
        """
        async with self.pool.acquire() as connection:
            query = """
            INSERT INTO users (tg, username)
            VALUES ($1, $2)
            """
            await connection.execute(query, tg, username)

    async def new_staff(self, tg: str, role: str, username: str) -> None:
        """
        Promote user to given role
        :param tg: Telegram id
        :param username: Telegram username
        :param role: Role to give
        """
        async with self.pool.acquire() as connection:
            query = """
            INSERT INTO staff (tg, role, username)
            VALUES ($1, $2, $3)
            """
            await connection.execute(query, tg, role, username)

    # UPDATE ===============================================================================================================
    async def edit_group(self, tg: str, group: str) -> None:
        """
        Change user's class to given value
        :param tg: Telegram id
        :param group: Class
        """
        async with self.pool.acquire() as connection:
            query = """
            UPDATE users
            SET class = $1
            WHERE tg = $2
            """
            await connection.execute(query, group, tg)

    async def edit_building(self, tg: str, building: str) -> None:
        """
        Change user's building to given value
        :param tg: Telegram id
        :param building: Building
        """
        async with self.pool.acquire() as connection:
            query = """
            UPDATE users
            SET building = $1
            WHERE tg = $2
            """
            await connection.execute(query, building, tg)

    async def edit_teacher(self, tg: str, teacher: str) -> None:
        """
        Change user's teacher to given value
        :param tg: Telegram id
        :param teacher: Teacher
        """
        async with self.pool.acquire() as connection:
            query = """
            UPDATE users
            SET teacher = $1
            WHERE tg = $2
            """
            await connection.execute(query, teacher, tg)

    async def edit_role(self, tg: str, role: str, username: str) -> None:
        """
        Change user's role to given value (and update username)
        :param tg: Telegram id
        :param role: Role to give
        :param username: Telegram username
        """
        async with self.pool.acquire() as connection:
            query = """
            UPDATE staff
            SET role = $1, username = $2
            WHERE tg = $3
            """
            await connection.execute(query, role, username, tg)
