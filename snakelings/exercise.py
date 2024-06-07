from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

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

    path: Path

    def __post_init__(self):
        exercise_folder_name = self.path.stem

        code_file = self.path.joinpath("main.py").open("r")
        readme_file = self.path.joinpath("readme.md").open("r")

        self.id = int(exercise_folder_name.split("_")[0]) # TODO: Handle the exception here.
        self.title = " ".join(exercise_folder_name.split("_")[1:]) # TODO: If title key exists in the config.toml prioritize that.
        self.readme = readme_file.read()

        done_comment_line = code_file.readline()

        self.completed = False if "# I'M NOT DONE YET" in done_comment_line else True

        readme_file.close()
        code_file.close()