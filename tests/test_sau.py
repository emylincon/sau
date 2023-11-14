import sys
import os

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, f"{os.path.dirname(os.path.abspath(__file__))}/../src/")

from sau.__main__ import Log

a = Log()
