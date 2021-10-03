import typing
from googletrans.constants import LANGCODES, LANGUAGES

from .file_manager import FileManager


class LanguageStorage:

    _data: typing.Dict[str, str]

    def __init__(self) -> None:
        self._data = FileManager.load_data()

        # indicates if there has been any change in the default languages.
        self.changed = False

    def set_user_language(self, user_id: str, language: str) -> None:
        language = self.get_language(language.lower())

        self._data[user_id] = language
        self.changed = True

    def get_user_language(self, user_id: str) -> str:
        if not self.contains_user(user_id):
            self.set_user_language(user_id, "portuguese")

        return self._data[user_id]

    def get_language(self, language: str) -> str:
        if language in LANGUAGES:
            language = LANGUAGES[language]
        elif language not in LANGCODES:
            language = None
        return language

    def contains_user(self, user_id: str) -> bool:
        return user_id in self._data

    def save(self) -> None:
        if self.changed:
            FileManager.write_data(self.data)
            self.changed = False

    @property
    def data(self):
        return self._data.copy()

    def __del__(self) -> None:
        self.save()
