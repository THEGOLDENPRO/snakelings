import os
import sys

__all__ = ()

def proper_clear():
    """
    Handles clearing the terminal cross platform **properly**. 
    WIP! Only supports Linux and Windows atm.
    """

    if sys.platform == "win32":
        os.system("clear")

    # Simply using the clear command won't work on terminals 
    # that have scrollback and will lead to side effects.
    os.system("echo -ne '\033c'")