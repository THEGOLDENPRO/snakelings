import importlib
from thefuzz import fuzz

EXCEPTED_OUTPUT = "Hello, Snakelings!\n"

def test_output(capsys):
    importlib.import_module("main", "..") # TODO: Fix "ModuleNotFoundError".

    captured = capsys.readouterr()

    fuzzy_value = fuzz.ratio(captured.out, EXCEPTED_OUTPUT)

    assert fuzzy_value > 90