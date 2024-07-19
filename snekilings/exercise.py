from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import toml
from dataclasses import dataclass, field

__all__ = (
    "Exercise",
)

@dataclass
class Exercise:
    id: int = field(init = False)
    title: str = field(init = False)
    readme: str = field(init = False)
    completed: bool = field(init = False)
    use_pytest: bool = field(init = False)
    execute_first: bool = field(init = False)

    path: Path

    def __post_init__(self):
        exercise_folder_name = self.path.stem

        code_file = self.path.joinpath("main.py").open("r")
        readme_file = self.path.joinpath("readme.md").open("r")
        config_file = self.path.joinpath("config.toml").open("r")

        self.id = int(exercise_folder_name.split("_")[0]) # TODO: Handle the exception here.

        config_data = toml.load(config_file)
        config_title = config_data.get("title")
        config_code_data = config_data.get("code", {})

        self.title = config_title if config_title is not None else " ".join(exercise_folder_name.split("_")[1:])

        self.readme = readme_file.read().format(
            id = self.id, 
            title = self.title, 
            code_path = str(self.path.joinpath("main.py"))
        )

        done_comment_line = code_file.readline()

        self.completed = False if "# I'M NOT DONE YET" in done_comment_line else True

        self.use_pytest = config_code_data.get("use_pytest", False)

        self.execute_first = config_code_data.get("execute_first", False)

        config_file.close()
        readme_file.close()
        code_file.close()