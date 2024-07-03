from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    from watchdog.events import FileSystemEvent

from watchdog.events import FileSystemEventHandler

__all__ = (
    "ModifiedEventHandler",
)

class ModifiedEventHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.modified = False
        self.latest_event: Optional[FileSystemEvent] = None

        super().__init__()

    def on_modified(self, event: FileSystemEvent) -> None:
        super().on_modified(event)

        self.modified = True
        self.latest_event = event