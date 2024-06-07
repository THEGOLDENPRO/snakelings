from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    ...

import typer
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown

from .logger import snakelings_logger
from .exercises_handler import ExerciseHandler

__all__ = ()

app = typer.Typer(
    pretty_exceptions_enable = False, 
    help = "🐍 A collection of small exercises to assist beginners at reading and writing Python code."
)

@app.command(help = "Start the exercises!")
def start(
    exercise_id: Optional[int] = typer.Argument(None, help = "The ID of the exercise to start from."), 
    path_to_exercises_folder: str = typer.Option(".", "--exercises-path", help = "The path to the exercises folder you are using.")
):
    exercises_path = Path(path_to_exercises_folder)
    snakelings_logger.debug(f"Exercises Path -> '{exercises_path.absolute()}'")

    console = Console()
    handler = ExerciseHandler(exercises_path)

    for exercise in handler.get_exercises():

        if exercise.completed:
            continue

        markdown = Markdown(exercise.readme)
        console.print(markdown)

        # TODO: Add watchdog stuff here I guess.

@app.command(help = "...")
def test():
    ...