from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple
    from .exercise import Exercise

import os
import sys
import subprocess
from devgoldyutils import LoggerAdapter

from .logger import snakelings_logger

__all__ = (
    "test_exercise",
)

logger = LoggerAdapter(snakelings_logger, prefix = "execution")

def execute_exercise_code(exercise: Exercise) -> Tuple[bool, str]:
    main_py_path = exercise.path.joinpath("main.py")

    logger.debug(f"Calling python to execute '{main_py_path}'...")
    popen = subprocess.Popen(
        [sys.executable, main_py_path], 
        stderr = subprocess.PIPE, 
        stdout = subprocess.PIPE, 
        text = True
    )

    return_code = popen.wait()
    output, output_error = popen.communicate()

    logger.debug(f"Return code: {return_code}")

    return True if return_code == 0 else False, output if return_code == 0 else output_error

def test_exercise_with_pytest(exercise: Exercise) -> Tuple[bool, str]:
    logger.debug(
        f"Testing exercise '{exercise.path.joinpath('main.py').absolute()}' with pytest..."
    )

    pytest_scripts = exercise.get_pytest_scripts()

    args = [
        sys.executable,
        "-m",
        "pytest",
        "--quiet"
    ]

    args.extend(
        [str(path) for path in pytest_scripts]
    )

    env_to_pass = os.environ.copy()

    # letting the test scripts known where the exercise is.
    env_to_pass["SNAKELINGS_EXERCISE_PATH"] = exercise.path.absolute()

    popen = subprocess.Popen(
        args,
        stderr = subprocess.PIPE,
        stdout = subprocess.PIPE,
        text = True,
        env = env_to_pass
    )

    stdout, stderr = popen.communicate()
    return_code = popen.wait()

    return True if return_code == 0 else False, stdout

def test_exercise(exercise: Exercise) -> Tuple[bool, str]:
    if exercise.config_data.get("pytest") is not None:
        return test_exercise_with_pytest(exercise)

    return execute_exercise_code(exercise)