import logging
from devgoldyutils import add_custom_handler, Colours

__all__ = ("snakelings_logger",)

snakelings_logger = add_custom_handler(
    logger = logging.getLogger(Colours.GREEN.apply("snakelings")), 
    level = logging.INFO
)