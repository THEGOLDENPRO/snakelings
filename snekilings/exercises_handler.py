from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, Optional

from pathlib import Path

from .exercise import Exercise

__all__ = (
    "ExerciseHandler", 
)

class ExerciseHandler():
    def __init__(self, path_to_exercises_folder: Path) -> None:
        self._path = path_to_exercises_folder

    def get_single_exercise(self, exercise_id: int) -> Optional[Exercise]:
        exercise = None

        for exercise_path in self._path.iterdir():
            id = int(exercise_path.split("_")[0]) # TODO: Handle the exception here.

            if exercise_id == id:
                exercise = Exercise(exercise_path)
                break

        return exercise

    def get_exercises(self) -> Iterable[Exercise]:

        for path in self._path.iterdir():

            if self.__is_exercise(path):
                yield Exercise(path)

    def get_exercises_amount(self) -> int:
        exercises = 0

        for path in self._path.iterdir():

            if self.__is_exercise(path):
                exercises += 1

        return exercises

    def __is_exercise(self, path: Path) -> bool:
        if path.is_dir() and path.name[0].isnumeric():
            return True
        
        return False