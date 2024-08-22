from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    from watchdog.events import FileSystemEvent

import logging
from watchdog.events import FileSystemEventHandler

__all__ =(
    "LoggingEventHandler",
)

class LoggingEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        super().__init__()
        self.logger = logger or logging.root

    def on_moved(self, event: FileSystemEvent) -> None:
        super().on_moved(event)

        what = "directory" if event.is_directory else "file"
        self.logger.debug("Moved %s: from %s to %s", what, event.src_path, event.dest_path)

    def on_created(self, event: FileSystemEvent) -> None:
        super().on_created(event)

        what = "directory" if event.is_directory else "file"
        self.logger.debug("Created %s: %s", what, event.src_path)

    def on_deleted(self, event: FileSystemEvent) -> None:
        super().on_deleted(event)

        what = "directory" if event.is_directory else "file"
        self.logger.debug("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        super().on_modified(event)

        what = "directory" if event.is_directory else "file"
        self.logger.debug("Modified %s: %s", what, event.src_path)

    def on_closed(self, event: FileSystemEvent) -> None:
        super().on_closed(event)

        self.logger.debug("Closed file: %s", event.src_path)

    def on_opened(self, event: FileSystemEvent) -> None:
        super().on_opened(event)

        self.logger.debug("Opened file: %s", event.src_path)