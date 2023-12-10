import dataclasses
import json
from collections import defaultdict
from typing import Optional

from redis import Redis

from bot.settings import Settings


from dataclasses import dataclass

from bot.text import EnglishText


def factory(data):
    return dict(x for x in data if x[1] is not None)

@dataclass
class Form:
    mother_full_name: str = ''
    mother_run: str = ''
    mother_nationality: str = ''
    mother_address: str = ''
    mother_comuna: str = ''


@dataclass
class UserData:
    id: int
    language_code: str = EnglishText.language_code
    questions_count: int = 10
    questions: list = dataclasses.field(default_factory=dict)
    current_question: int = 0
    correct_answers: int = 0

    @classmethod
    def from_json(cls, data: str):
        data = json.loads(data)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> 'UserData':
        user_data = UserData(**data)
        return user_data

    def to_json(self) -> str:
        data = self.to_dict()
        return json.dumps(data)

    def to_dict(self) -> dict:
        data = dataclasses.asdict(self, dict_factory=factory)
        return data


class DataStorage:
    _storage: Redis

    def __init__(self, settings: Settings):
        from redis.asyncio.client import Redis
        self._storage = Redis(host=settings.redis.host, port=settings.redis.port)

    async def get_user_data_key(self, user_id: int):
        return f'user:{user_id}:data'

    async def get_user_data(self, user_id: int) -> UserData:
        print('==== = == = = =====resis ping', await self._storage.ping())
        user_raw_data: Optional[str] = await self._storage.get(await self.get_user_data_key(user_id))
        print('=====', user_raw_data)
        if not user_raw_data or user_raw_data is None:
            return UserData(
                id=user_id
            )
        else:
            return UserData.from_json(user_raw_data)

    async def set_user_data(self, user_data: UserData):
        print(f'===== SET USER DATA ====== {user_data}')
        await self._storage.set(await self.get_user_data_key(user_data.id), user_data.to_json())


