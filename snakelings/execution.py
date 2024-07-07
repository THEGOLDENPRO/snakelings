from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple
    from .exercise import Exercise

import sys
import subprocess
from devgoldyutils import LoggerAdapter
import pytest
import io

from .logger import snakelings_logger

__all__ = (
    "handle_execution",
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

def execute_pytest(exercise: Exercise) -> Tuple[bool, str]:
    main_py_path = exercise.path.joinpath("main.py").absolute()

    logger.debug(f"Using pytest to execute '{main_py_path}'...")

    output_buffer = io.StringIO()

    sys.stdout = output_buffer
    sys.stderr = output_buffer

    return_code = pytest.main([main_py_path])

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    return True if return_code == 0 else False, "" if return_code == 0 else output_buffer.getvalue()

def handle_execution(exercise: Exercise) -> Tuple[bool, str]:
    if exercise.use_pytest is False:
        result, output = execute_exercise_code(exercise)
    else:
        result, output = execute_pytest(exercise)
    
    return result, output