import os
import sys
import importlib
from thefuzz import fuzz

EXCEPTED_OUTPUT = "Hello, Snakelings!\n"

sys.path.insert(1, os.environ.get("SNAKELINGS_EXERCISE_PATH"))

def test_output(capsys):
    importlib.import_module("main")

    captured = capsys.readouterr()

    fuzzy_value = fuzz.ratio(captured.out, EXCEPTED_OUTPUT)

    assert fuzzy_value > 80 