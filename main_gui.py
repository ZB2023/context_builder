import sys
from gui import run_gui

if __name__ == "__main__":
    sys.argv.append("--gui")
    run_gui()