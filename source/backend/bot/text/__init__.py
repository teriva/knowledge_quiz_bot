from typing import Dict, Optional, Type

from bot.text.base import EnglishText, RussianText


class Languages:
    languages_by_name: Dict[str, Type[EnglishText]]
    languages_by_code: Dict[str, Type[EnglishText]]

    def __init__(self):
        self.languages_by_name = {}
        self.languages_by_code = {}

    def get_by_name(self, name: str) -> Type[EnglishText]:
        language = self.languages_by_name.get(name)
        if language is not None:
            return language
        return EnglishText

    def get_by_code(self, code: str) -> Type[EnglishText]:
        language = self.languages_by_code.get(code)
        if language is not None:
            return language
        return EnglishText

    def register(self, language: Type[EnglishText]):
        self.languages_by_name[language.language_name] = language
        self.languages_by_code[language.language_code] = language

    @property
    def all(self) -> list:
        return list(self.languages_by_code.values())


languages = Languages()

languages.register(EnglishText)
languages.register(RussianText)
