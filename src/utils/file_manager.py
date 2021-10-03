import json
import typing
from pathlib import Path
from abc import ABC


class FileManager(ABC):
    """Class with static methods for manipulating .json files."""

    # path to .json file to manipulate.
    PATH: Path = Path("./users_languages.json")

    @staticmethod
    def load_data() -> typing.Dict[str, str]:
        """Loads data from a .json file. Create the file if it doesn't
        exist.

        :return `dict`: A dict containing the file data. An empty
        dict if the file doesn't exist.
        """
        data = {}

        if FileManager.PATH.is_file():
            with open(FileManager.PATH, "r") as f:
                data = json.load(f)
        else:
            FileManager._create_empty_file()

        return data

    @staticmethod
    def write_data(data: typing.Dict[str, str], indent: int = 4) -> None:
        """Write data from a dict to the .json file."""
        with open(FileManager.PATH, "w+") as file:
            json.dump(data, file, indent=indent)

    @staticmethod
    def _create_empty_file() -> None:
        """Creates an empty .json file."""
        FileManager.write_data(data={})
