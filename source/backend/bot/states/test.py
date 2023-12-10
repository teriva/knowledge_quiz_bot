from typing import Optional

from bot.states.base import BaseCustomState


class TestState(BaseCustomState):
    def __init__(self, state: Optional[str] = None, group_name: Optional[str] = None) -> None:
        print('341231423')
        super().__init__(state, group_name)