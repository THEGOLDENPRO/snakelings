import os
import sys
import importlib

sys.path.insert(1, os.environ.get("SNAKELINGS_EXERCISE_PATH"))

# DO NOT TOUCH 🐈 🐾 MEOW!
def test_cat_variable():
    main_module = importlib.import_module("main")

    cat_amount = getattr(main_module, "cat_amount", None)

    assert cat_amount is not None, "Are you sure that 'cat_amount' variable " \
        "is assigned as 'cat_amount'! Please do not rename it!"

    assert cat_amount == 7