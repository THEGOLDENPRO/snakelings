from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict, List

    class PytestScriptData(TypedDict):
        module: str
        fail_hint: str

import toml
from pathlib import Path
from devgoldyutils import LoggerAdapter
from dataclasses import dataclass, field

from .logger import snakelings_logger

__all__ = (
    "Exercise",
)

logger = LoggerAdapter(snakelings_logger, prefix = "Exercise")

@dataclass
class Exercise:
    id: int = field(init = False)
    title: str = field(init = False)
    readme: str = field(init = False)
    completed: bool = field(init = False)
    execute_first: bool = field(init = False)
    extra_files: List[str] = field(init = False)

    config_data: dict = field(init = False, repr = False)

    path: Path
    is_packed: bool = field(default = False)

    def __post_init__(self):
        exercise_folder_name = self.path.stem

        code_file = self.path.joinpath("main.py").open("r")

        data_dir = () if self.is_packed else (".data",)

        readme_file = self.path.joinpath(*data_dir, "readme.md").open("r")
        config_file = self.path.joinpath(*data_dir, "config.toml").open("r")

        self.id = int(exercise_folder_name.split("_")[0]) # TODO: Handle the exception here.

        self.config_data = toml.load(config_file)
        config_title = self.config_data.get("title")
        config_code_data = self.config_data.get("code", {})
        config_misc_data = self.config_data.get("misc", {})

        self.title = config_title if config_title is not None else (" ".join(exercise_folder_name.split("_")[1:]).title())

        self.readme = readme_file.read().format(
            id = self.id, 
            title = self.title, 
            code_path = str(self.path.joinpath("main.py"))
        )

        done_comment_line = code_file.readline()
        self.completed = False if "# I'M NOT DONE YET" in done_comment_line else True

        self.execute_first = config_code_data.get("execute_first", False)

        self.extra_files = config_misc_data.get("extra_files_to_include", [])

        config_file.close()
        readme_file.close()
        code_file.close()

    def get_pytest_scripts(self) -> List[Path]:
        config_pytest_data = self.config_data.get("pytest", {})

        if config_pytest_data == {}:
            return []

        test_scripts: List[PytestScriptData] = config_pytest_data["test_scripts"]

        test_script_paths = []

        for test_script in test_scripts:
            module_string_path = test_script["module"]

            module_path = Path(module_string_path)

            data_directory = self.path.joinpath(".data")
            module_path = data_directory.joinpath(module_path)

            if module_path.exists():
                test_script_paths.append(module_path)

            else:
                logger.warning(
                    "The pytest script you entered in config "\
                        f"('{module_path}') ""does not exist so it will be ignored!"
                )

        return test_script_paths