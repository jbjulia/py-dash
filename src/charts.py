from PyQt5.QtChart import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QHorizontalBarSeries,
    QLineSeries,
    QPieSeries,
    QPieSlice,
    QValueAxis
)
from PyQt5.QtCore import Qt

from src import functions as f


def bar_chart(horizontal=True):
    series = QHorizontalBarSeries() if horizontal else QBarSeries()
    chart = QChart()

    set0 = QBarSet("Metric 1")
    set1 = QBarSet("Metric 2")
    set2 = QBarSet("Metric 3")
    set3 = QBarSet("Metric 4")

    set0.append([1, 2, 3, 4])
    set1.append([5, 0, 0, 4])
    set2.append([3, 5, 8, 13])
    set3.append([5, 6, 7, 3])

    series.append(set0)
    series.append(set1)
    series.append(set2)
    series.append(set3)

    chart.addSeries(series)
    chart.setTitle("Metrics")
    chart.setAnimationOptions(QChart.AllAnimations)
    chart.setTheme(0)  # 0 - 7

    months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June')

    y_axis = QBarCategoryAxis()
    y_axis.append(months)
    chart.addAxis(y_axis, Qt.AlignLeft)
    series.attachAxis(y_axis)

    x_axis = QValueAxis()
    chart.addAxis(x_axis, Qt.AlignBottom)
    series.attachAxis(x_axis)

    x_axis.applyNiceNumbers()

    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)

    return chart


def line_chart():
    series = QLineSeries()
    chart = QChart()

    series.append(
        f.load_backend()["metrics"]["metric_1"],
        f.load_backend()["metrics"]["metric_3"],
    )
    series.append(
        f.load_backend()["metrics"]["metric_2"],
        f.load_backend()["metrics"]["metric_4"],
    )

    chart.setAnimationOptions(QChart.AllAnimations)
    chart.setTheme(0)  # 0 - 7
    chart.addSeries(series)
    chart.setTitle("Metrics")
    chart.createDefaultAxes()

    return chart


def pie_chart():
    series = QPieSeries()
    chart = QChart()

    series.append("Metric 1", f.load_backend()["metrics"]["metric_1"])
    series.append("Metric 2", f.load_backend()["metrics"]["metric_2"])
    series.append("Metric 3", f.load_backend()["metrics"]["metric_3"])
    series.append("Metric 4", f.load_backend()["metrics"]["metric_4"])

    series.setLabelsVisible(True)
    series.setLabelsPosition(QPieSlice.LabelOutside)

    for sliver in series.slices():
        sliver.setLabel("{:.2f}%".format(100 * sliver.percentage()))

    chart.setTheme(0)  # 0 - 7
    chart.addSeries(series)
    chart.createDefaultAxes()
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.setTitle("Metrics")

    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)
    chart.legend().markers(series)[0].setLabel("Metric 1")
    chart.legend().markers(series)[1].setLabel("Metric 2")
    chart.legend().markers(series)[2].setLabel("Metric 3")
    chart.legend().markers(series)[3].setLabel("Metric 4")

    return chart
