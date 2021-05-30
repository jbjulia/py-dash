__author__ = "Joseph Julian"
__version__ = "1.0.0"

import sys

from PyQt5.QtWidgets import QApplication

from src import constants as c
from src import main

"""
This dashboard is inspired by the ancient Greek god Ares.
Design includes basic functions, features and elements, but may be
modified to meet specific needs. Visit www.py-dash.com for support.
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main.Dashboard(ui=c.ARES)
    window.show()
    sys.exit(app.exec_())
