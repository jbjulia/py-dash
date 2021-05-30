import getpass
import json
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from src import constants as c


def get_login():
    try:
        return os.getlogin()
    except OSError:
        return getpass.getuser()


def prompt_user(action, text, title):
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(c.OWL))
    msg_box.setText(text)
    msg_box.setWindowTitle(title)

    if action == "Question":
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    elif action == "Information":
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    elif action == "Warning":
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    return msg_box.exec()


def load_backend():
    try:
        with open(c.JSON) as in_file:
            return json.load(in_file)
    except (KeyError, ValueError) as e:
        print("JSON Error: %s" % e)
        prompt_user(
            "Warning",
            "Error: Cannot connect to backend.",
            "Application Error"
        )
        return None
