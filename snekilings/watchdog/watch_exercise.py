from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from watchdog.events import FileSystemEvent

import time
from pathlib import Path
from watchdog.observers import Observer
from devgoldyutils import LoggerAdapter, Colours

from ..exercise import Exercise
from ..logger import snakelings_logger
from .event_handlers import LoggingEventHandler, ModifiedEventHandler

__all__ = (
    "watch_exercise_complete", 
    "watch_exercise_modify"
)

logger = LoggerAdapter(snakelings_logger, prefix = Colours.GREY.apply("🐶 Watch Dog"))
logging_event_handler_logger = LoggerAdapter(logger, prefix = "Logging")

def watch_exercise_complete(exercise: Exercise) -> None:
    """Halts until the exercise is marked completed successfully otherwise it NEVER returns."""
    event = watch_exercise_modify(exercise)

    while True:
        completed = Exercise(Path(event.src_path)).completed

        if completed:
            snakelings_logger.debug(f"The exercise '{exercise.title}' was marked completed.")
            return

        event = watch_exercise_modify(exercise)

def watch_exercise_modify(exercise: Exercise) -> FileSystemEvent:
    observer = Observer()

    event_handler = ModifiedEventHandler()
    observer.schedule(event_handler, str(exercise.path.absolute()), recursive = True)
    observer.schedule(LoggingEventHandler(logger = logging_event_handler_logger), str(exercise.path.absolute()), recursive = True)

    observer.start()

    try:
        while True:
            time.sleep(1)

            if event_handler.modified:
                logger.debug(f"The exercise '{exercise.title}' was modified.")
                return event_handler.latest_event

    finally:
        observer.stop()
        observer.join()