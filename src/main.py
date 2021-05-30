import json
import os.path
import sys
from datetime import datetime

import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QDesktopWidget,
    QListWidgetItem
)

from athena import __version__
from src import charts
from src import constants as c
from src import functions as f


class Dashboard(QMainWindow):
    def __init__(self, ui):
        super(Dashboard, self).__init__()
        uic.loadUi(ui, self)

        self.run_operations()

    def run_operations(self):
        self.setup_ui()
        self.pull_metrics()
        self.check_backend()
        self.check_internet()
        self.check_version()
        self.get_tasks()

    def setup_ui(self):
        """
        Removes window border, map button icons and actions. Gets
        current username and outstanding tasks and sets greeting.
        :return:
        """
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(c.OWL))
        self.btnLogo.setIcon(QIcon(c.OWL))
        self.btnQuit.setIcon(QIcon(c.QUIT))
        self.btnSettings.setIcon(QIcon(c.SETTINGS))
        self.btnUser.setIcon(QIcon(c.USER))
        self.btnCollapse.setIcon(QIcon(c.COLLAPSE))
        self.btnToggleWindowSize.setIcon(QIcon(c.MAXIMIZE))
        self.btnBarChart.setIcon(QIcon(c.BAR_CHART))
        self.btnLineChart.setIcon(QIcon(c.LINE_CHART))
        self.btnPieChart.setIcon(QIcon(c.PIE_CHART))
        self.btnBackend.setIcon(QIcon(c.BACKEND))
        self.btnInternet.setIcon(QIcon(c.INTERNET))
        self.btnVersion.setIcon(QIcon(c.VERSION))

        self.btnQuit.clicked.connect(self.quit_app)
        self.btnSettings.clicked.connect(self.settings)
        self.btnUser.clicked.connect(self.user)
        self.btnCollapse.clicked.connect(lambda: self.toggle_window_size(collapse=True))
        self.btnToggleWindowSize.clicked.connect(self.toggle_window_size)
        self.btnBarChart.clicked.connect(self.bar_chart)
        self.btnLineChart.clicked.connect(self.line_chart)
        self.btnPieChart.clicked.connect(self.pie_chart)
        self.btnBackend.clicked.connect(lambda: self.check_backend(prompt=True))
        self.btnInternet.clicked.connect(lambda: self.check_internet(prompt=True))
        self.btnVersion.clicked.connect(lambda: self.check_version(prompt=True))

        self.lblGreeting.setText(
            f"Hello, {f.get_login()}! You have ({len(f.load_backend()['tasks']['outstanding_tasks'])}) outstanding "
            f"tasks to complete.")

    def pull_metrics(self):
        """
        Pulls metrics from backend file and updates dashboard labels.
        TODO: Increment animation for setText()
        :return:
        """
        metrics_list = []

        for value in f.load_backend()["metrics"].values():
            if value > 999:
                metrics_list.append(f"{str(value)[:1]}.{str(value)[1]}k")
            else:
                metrics_list.append(f"{value}")

        self.lblMetric1_Count.setText(metrics_list[0])
        self.lblMetric2_Count.setText(metrics_list[1])
        self.lblMetric3_Count.setText(metrics_list[2])
        self.lblMetric4_Count.setText(metrics_list[3])

        self.widget.setChart(charts.bar_chart(horizontal=True))

    def check_backend(self, prompt=False):
        """
        Validates integrity of application backend (backend.json).
        TODO: Restore backend upon exception
        :return:
        """
        try:
            with open(c.JSON) as in_file:
                json.load(in_file)
                self.btnBackend.setText("LINKED")
                if prompt:
                    f.prompt_user(
                        "Information",
                        "Backend is linked successfully!",
                        "Application Backend"
                    )
        except ValueError as e:
            print("JSON Error: %s" % e)
            self.btnBackend.setText("UNLINKED\nCLICK TO FIX")
            if prompt:
                f.prompt_user(
                    "Warning",
                    "Error:  Cannot link to backend.\n\n%s" % e,
                    "Application Backend"
                )

    def check_internet(self, prompt=False):
        """
        Sends generic URL request to test internet connection.
        TODO: Restore internet connection upon exception
        :return:
        """
        try:
            requests.get("https://www.py-dash.com", timeout=5)
            self.btnInternet.setText("CONNECTED")
            if prompt:
                f.prompt_user(
                    "Information",
                    "Internet is connected successfully!",
                    "Internet Connection"
                )
        except (requests.ConnectionError, requests.Timeout) as e:
            print("Connection Error: %s" % e)
            self.btnInternet.setText("DISCONNECTED\nCLICK TO FIX")
            if prompt:
                f.prompt_user(
                    "Warning",
                    "Error:  Cannot connect to the internet.\n\n%s" % e,
                    "Internet Connection"
                )

    def check_version(self, prompt=False):
        """
        Checks GitHub repository for new updates.
        TODO: Download and install new updates
        :return:
        """
        last_updated = datetime.fromtimestamp(os.stat(__file__).st_mtime)
        self.btnVersion.setText("UP TO DATE")
        if prompt:
            f.prompt_user(
                "Information",
                f"You are running the current version of Athena!\n\nv.{__version__} last updated on {last_updated}.",
                "Application Version"
            )
        return

    def get_tasks(self):
        for item in f.load_backend()["tasks"]["completed_tasks"]:
            task = QListWidgetItem(item)
            task.setFlags(
                Qt.ItemIsEnabled
                | Qt.ItemIsEditable
                | Qt.ItemIsUserCheckable
            )
            task.setCheckState(Qt.Checked)
            font = task.font()
            font.setStrikeOut(True)
            font.setItalic(True)
            task.setFont(QFont(font))
            self.listWidget.addItem(task)
        for item in f.load_backend()["tasks"]["outstanding_tasks"]:
            task = QListWidgetItem(item)
            task.setFlags(
                Qt.ItemIsEnabled
                | Qt.ItemIsEditable
                | Qt.ItemIsUserCheckable
            )
            task.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(task)

    def quit_app(self):
        """
        Prompts user to confirm application exit.
        :return:
        """
        self.setWindowOpacity(.65)

        if f.prompt_user(
                "Question",
                "Are you sure you want to quit?",
                "Quit Application"
        ) == QMessageBox.Yes:
            sys.exit(0)
        else:
            self.setWindowOpacity(.97)
            return

    def settings(self):
        """
        This function is ready for development!
        :return:
        """
        return

    def user(self):
        """
        This functions is ready for development!
        :return:
        """
        return

    def toggle_window_size(self, collapse=True):
        """
        Checks current window state, then either minimizes or maximizes
        window. Moves buttons to respective places inside frames.
        :return:
        """
        if collapse:
            self.showMinimized()
            return
        elif self.btnToggleWindowSize.toolTip() == "Maximize Window":
            self.showMaximized()
            self.btnToggleWindowSize.setIcon(QIcon(c.MINIMIZE))
            self.btnToggleWindowSize.setToolTip("Minimize Window")
        else:
            self.showNormal()
            self.center()
            self.btnToggleWindowSize.setIcon(QIcon(c.MAXIMIZE))
            self.btnToggleWindowSize.setToolTip("Maximize Window")

        self.btnQuit.move(0, self.frmMenu.height() - 51)
        self.btnSettings.move(70, self.frmMenu.height() - 51)
        self.btnUser.move(140, self.frmMenu.height() - 51)
        self.btnCollapse.move((self.frmHeader.width() - 81), 10)
        self.btnToggleWindowSize.move((self.frmHeader.width() - 41), 10)

    def bar_chart(self):
        """
        Pulls metrics and displays bar chart.
        # TODO: Option to toggle vertical/horizontal.
        :return:
        """
        self.widget.setChart(charts.bar_chart(horizontal=True))

    def line_chart(self):
        """
        Pulls metrics and displays line chart.
        :return:
        """
        self.widget.setChart(charts.line_chart())

    def pie_chart(self):
        """
        Pulls metrics and displays pie chart.
        :return:
        """
        self.widget.setChart(charts.pie_chart())

    def add_item(self):
        """
        Adds new item to listWidget and sets flags.
        :return:
        """
        self.listWidget.addItem("New Item")

    def remove_item(self):
        """
        Removes current selected items from listWidget.
        :return:
        """
        list_items = self.listWidget.selectedItems()

        if list_items:
            for item in list_items:
                self.listWidget.takeItem(self.listWidget.row(item))
        else:
            return

    def center(self):
        """
        Captures desktop geometry and centers window on screen.
        :return:
        """
        window = self.frameGeometry()
        centered = QDesktopWidget().availableGeometry().center()
        window.moveCenter(centered)
        self.move(window.topLeft())

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)
