from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..exercise import Exercise

import time
from watchdog.observers import Observer
from devgoldyutils import LoggerAdapter, Colours

from ..logger import snakelings_logger
from .event_handlers import ExerciseEventHandler, LoggingEventHandler

__all__ = (
    "watch_exercise_complete",
)

watchdog_logger = LoggerAdapter(snakelings_logger, prefix = Colours.GREY.apply("🐶 Watch Dog"))

def watch_exercise_complete(exercise: Exercise) -> None:
    """Halts until the exercise is completed successfully otherwise it NEVER returns."""
    observer = Observer()

    exercise_event_handler = ExerciseEventHandler()
    observer.schedule(exercise_event_handler, str(exercise.path.absolute()), recursive = True)

    observer.schedule(LoggingEventHandler(logger = watchdog_logger), str(exercise.path.absolute()), recursive = True)

    observer.start()

    try:
        while True:
            time.sleep(1)

            if exercise_event_handler.completed:
                snakelings_logger.info(f"The exercise '{exercise.title}' has been complete!")
                return

    finally:
        observer.stop()
        observer.join()