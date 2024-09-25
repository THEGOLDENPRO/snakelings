import os
import sys
import importlib

sys.path.insert(1, os.environ.get("SNAKELINGS_EXERCISE_PATH"))

def test_do_math():
    main_module = importlib.import_module("main")

    assert main_module.do_math() == 60