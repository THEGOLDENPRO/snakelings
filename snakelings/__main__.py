from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

import time
import typer
import random
import shutil
import logging
from pathlib import Path
from rich.console import Console
from devgoldyutils import Colours
from rich.markdown import Markdown

from .exercise import Exercise
from .execution import test_exercise
from .logger import snakelings_logger
from .watchdog import watch_exercise_complete, watch_exercise_modify
from .exercises_handler import ExerciseHandler

__all__ = ()

EXERCISE_ERROR_MESSAGES = [
    "Oh no (anyways), an exception has been raised. Please look over the error message and retry.",
    "Oh oh, an exception occurred. Try and interpret the traceback below and try again. Don't forget to save.",
    "Looks like that one didn't execute successfully. Look at the traceback and try again."
]

app = typer.Typer(
    pretty_exceptions_enable = False,
    help = "🐍 A collection of small exercises to assist beginners at reading and writing Python code."
)

@app.command(help = "Start the exercises!")
def start(
    exercise_id: int = typer.Argument(0, help = "The ID of the exercise to start from."),
    path_to_exercises_folder: str = typer.Option("./exercises", "--exercises-path", help = "The path to the exercises folder you are using."),

    enter_to_continue: bool = typer.Option(
        True,
        "--ets/--no-ets",
        "--enter-to-continue/--no-enter-to-continue",
        is_flag = True,
        help = "ON by default, this enforces you to press enter before moving onto the next exercise."
    ),
    wait_to_continue: bool = typer.Option(
        False,
        "--wts",
        "--wait-to-continue",
        help = "Waits some time before moving onto the next exercise."
    ),
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
        raise typer.Exit(1)

    console = Console()

    handler = ExerciseHandler(exercises_path)

    no_exercises = True
    exercise_count = handler.get_exercises_amount()

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

        print(Colours.ORANGE.apply(f"🚧 Progress: {exercise.id} / {exercise_count}"))
        print(Colours.CLAY.apply(f"⚡ Complete the '{exercise.title}' exercise!"))

        watch_exercise_complete(exercise) # This will halt here until the exercise is marked complete

        snakelings_logger.info(f"Oh, you're done with the '{exercise.title}' exercise.")

        snakelings_logger.info("Now let's execute that code...")
        result, output = test_exercise(exercise)

        while result is False:
            snakelings_logger.error(random.choice(EXERCISE_ERROR_MESSAGES)           )

            print(f"\n{Colours.BOLD_RED.apply('[🟥 Error]')} \n{output}")
            print(Colours.ORANGE.apply(f"🚧 Progress: {exercise.id} / {exercise_count}"))

            watch_exercise_modify(exercise)

            result, output = test_exercise(exercise)

        print(f"\n{Colours.ORANGE.apply('[✨ Output]')} \n{output}")

        if enter_to_continue:
            snakelings_logger.info("Well done! ✨ Press enter to move onto the next question when you are ready!")
            input("\n [ENTER TO CONTINUE] ")

        elif wait_to_continue:
            snakelings_logger.info("Well done! ✨ Moving onto the next exercise in 3 seconds...")
            time.sleep(4) # TODO: Make this adjustable.

    if no_exercises:
        snakelings_logger.error(
            f"There was no exercises in that directory! DIR --> '{exercises_path.absolute()}'."
        )
        raise typer.Exit(1)

    snakelings_logger.info(
        Colours.GREEN.apply("🎊 Congrats, you have finished all the exercises we currently have to offer.") +
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
        raise typer.Exit(1)

    exercises_folder_path.mkdir(exist_ok = True)

    for path in library_exercises_path.iterdir():
        copy_exercise(path, exercises_folder_path)

    snakelings_logger.info(Colours.BLUE.apply("✨ Exercises copied!"))

@app.command(help = "Update exercises folder in the current working directory.")
def update(
    path_to_exercises_folder: str = typer.Argument("./exercises", help = "The path to dump the exercises."), 

    debug: bool = typer.Option(False, help = "Log more details.")
):
    did_update = False
    exercises_folder_path = Path(path_to_exercises_folder)

    if debug:
        snakelings_logger.setLevel(logging.DEBUG)

    library_exercises_path = Path(__file__).parent.joinpath("exercises")

    snakelings_logger.debug("Checking and copying exercises from snakelings module...")

    for exercise_path in library_exercises_path.iterdir():
        local_exercise = exercises_folder_path.joinpath(exercise_path.stem)

        if local_exercise.exists():
            continue

        snakelings_logger.debug(f"Copying exercise from '{exercise_path}'...")
        # shutil.copytree(exercise_path, local_exercise)
        copy_exercise(exercise_path, exercises_folder_path)
        did_update = True

    if not did_update:
        snakelings_logger.info(Colours.RED.apply("There are no new exercises."))
        raise typer.Exit()

    snakelings_logger.info(Colours.BLUE.apply("✨ New exercises added!"))


def copy_exercise(path_to_exercise: Path, exercise_folder_path: Path):
    exercise = Exercise(path_to_exercise, is_packed = True)

    for exercise_file_path in path_to_exercise.iterdir():

        if exercise_file_path.is_dir():
            continue

        destination_path = exercise_folder_path.joinpath(path_to_exercise.name)

        snakelings_logger.debug(
            f"Copying exercise file '{exercise_file_path}' --> '{destination_path}'..."
        )

        if not exercise_file_path.name == "main.py" and exercise_file_path.name not in exercise.extra_files:
            destination_path = destination_path.joinpath(".data")

        destination_path.mkdir(parents = True, exist_ok = True)

        shutil.copy(exercise_file_path, destination_path.joinpath(exercise_file_path.name))