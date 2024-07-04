from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple
    from .exercise import Exercise

import sys
import subprocess
from devgoldyutils import LoggerAdapter

from .logger import snakelings_logger

__all__ = (
    "execute_exercise_code",
)

logger = LoggerAdapter(snakelings_logger, prefix = "execution")

def execute_exercise_code(exercise: Exercise) -> Tuple[bool, str]:
    main_py_path = exercise.path.joinpath("main.py")

    logger.debug(f"Calling python to execute '{main_py_path}'...")
    popen = subprocess.Popen(
        [sys.executable, main_py_path], 
        stderr = subprocess.PIPE, 
        stdout = subprocess.PIPE, 
        text = True, 
    )

    return_code = popen.wait()
    output, output_error = popen.communicate()

    logger.debug(f"Return code: {return_code}")

    return True if return_code == 0 else False, output if return_code == 0 else output_error