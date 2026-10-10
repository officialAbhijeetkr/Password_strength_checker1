# ============================================================
#  Password Strength Checker — Launcher
#  Double-click this file to open the GUI application.
# ============================================================

import subprocess
import sys
import os

# Make sure we run from the folder where this file lives,
# so that password_checker.py can always be found.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

subprocess.run([sys.executable, "password_checker_gui.py"])
