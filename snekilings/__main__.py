from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    ...

import typer
import shutil
import logging
from pathlib import Path
from rich.console import Console
from devgoldyutils import Colours
from rich.markdown import Markdown
import random

from .logger import snakelings_logger
from .execution import test_exercise
from .watchdog import watch_exercise_complete, watch_exercise_modify
from .exercises_handler import ExerciseHandler

__all__ = ()

app = typer.Typer(
    pretty_exceptions_enable = False, 
    help = "🐍 A collection of small exercises to assist beginners at reading and writing Python code."
)

@app.command(help = "Start the exercises!")
def start(
    exercise_id: int = typer.Argument(0, help = "The ID of the exercise to start from."), 
    path_to_exercises_folder: str = typer.Option("./exercises", "--exercises-path", help = "The path to the exercises folder you are using."),

    debug: bool = typer.Option(False, help = "Log more details.")
):
    exercises_path = Path(path_to_exercises_folder)

    if debug:
        snakelings_logger.setLevel(logging.DEBUG)

    snakelings_logger.debug(f"Exercises Path -> '{exercises_path.absolute()}'")

    if not exercises_path.exists():
        snakelings_logger.error(
            f"The exercises folder ({exercises_path.absolute()}) was not found! Create it with 'snakelings init'."
        )
        return False

    console = Console()

    handler = ExerciseHandler(exercises_path)

    no_exercises = True

    for exercise in sorted(handler.get_exercises(), key = lambda x: x.id):
        no_exercises = False

        if exercise.completed:
            result, _ = test_exercise(exercise)

            if result is True:
                continue

        if exercise_id >= exercise.id and not exercise.id == exercise_id:
            continue

        console.clear()

        markdown = Markdown(exercise.readme)
        console.print(markdown)

        if exercise.execute_first:
            _, output = test_exercise(exercise)

            print(f"\n{Colours.RED.apply('[🛑 Problem]')} \n{output}")

        print(Colours.CLAY.apply(f"⚡ Complete the '{exercise.title}' exercise!"))

        watch_exercise_complete(exercise) # This will halt here until the exercise is marked complete

        snakelings_logger.info(f"Oh, you're done with the '{exercise.title}' exercise.")

        snakelings_logger.info("Now let's execute that code...")
        result, output = test_exercise(exercise)

        while result is False:
            error_messages = [
                "Oh no (anyways), an exception has been raised. Please look over the error message and retry.",
                "Oh oh, an exception occurred. Try and interpret the traceback above and try again. Don't forget to save."
            ]

            snakelings_logger.error(
                random.choice(error_messages)           
            )

            print(f"\n{Colours.BOLD_RED.apply('[🟥 Error]')} \n{output}")

            watch_exercise_modify(exercise)

            result, output = test_exercise(exercise)

        print(f"\n{Colours.ORANGE.apply('[✨ Output]')} \n{output}")

    if no_exercises:
        snakelings_logger.error(
            f"There was no exercises in that directory! DIR --> '{exercises_path.absolute()}'."
        )
        return False

    snakelings_logger.info(
        "🎊 Congrats, you have finished all the exercises we currently have to offer." \
        "\nCome back for more exercises later as snakelings grows 🪴 more or run the " \
        "'snakelings update' command to check if there are any new exercises."
    )


@app.command(help = "Create exercises folder in the current working directory.")
def init(
    path_to_exercises_folder: str = typer.Argument("./exercises", help = "The path to dump the exercises."), 

    debug: bool = typer.Option(False, help = "Log more details.")
):
    exercises_folder_path = Path(path_to_exercises_folder)

    if debug:
        snakelings_logger.setLevel(logging.DEBUG)

    library_exercises_path = Path(__file__).parent.joinpath("exercises")

    snakelings_logger.debug("Copying exercises from snakelings module...")

    if exercises_folder_path.exists() and next(exercises_folder_path.iterdir(), None) is not None:
        snakelings_logger.error(
            f"The exercises folder ({exercises_folder_path.absolute()}) is not empty!" \
            "\nIf you would like to update your exercises use 'snakelings update' instead."
        )
        return False

    shutil.copytree(library_exercises_path, exercises_folder_path, dirs_exist_ok = True)

    snakelings_logger.info(Colours.BLUE.apply("✨ Exercises copied!"))