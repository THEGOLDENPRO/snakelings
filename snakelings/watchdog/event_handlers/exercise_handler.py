from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from watchdog.events import FileSystemEvent

from pathlib import Path
from watchdog.events import FileSystemEventHandler

from ...exercise import Exercise

__all__ = (
    "ExerciseEventHandler",
)

class ExerciseEventHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.completed = False
        super().__init__()

    def on_modified(self, event: FileSystemEvent) -> None:
        super().on_modified(event)

        if event.is_directory is True:
            self.completed = Exercise(Path(event.src_path)).completed