import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
)
from PyQt5.QtCore import QTimer, QTime, Qt


class Clock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clock app")
        self.setMinimumSize(800, 500)
        self.setMaximumSize(800, 500)

        self.tab_1 = QWidget()
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()

        self.tab_1.setStyleSheet("background-color: #222222; color: #eeeeee")
        self.tab_2.setStyleSheet("background-color: #222222; color: #eeeeee")
        self.tab_3.setStyleSheet("background-color: #222222; color: #eeeeee")

        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab_1, "Digital Clock")
        self.tabs.addTab(self.tab_2, "Stopwatch")
        self.tabs.addTab(self.tab_3, "Alarm Clock")

        self.setCentralWidget(self.tabs)

        digital_clock = self.tab_1

        digital_clock.clock_layout = QVBoxLayout()
        clock_layout = digital_clock.clock_layout

        self.time_label = QLabel(self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 120px")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        clock_layout.addWidget(self.time_label)
        self.tab_1.setLayout(clock_layout)

        self.update_time()

        clock_layout.addWidget(self.time_label)
        self.tab_1.setLayout(clock_layout)

        self.stopwatch_layout = QVBoxLayout()

        self.time = QTime(0, 0, 0, 0)
        self.stopwatch_time_label = QLabel("00:00:00:00")

        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet(
            "background-color: #dddddd; color: #111111; height: 40px; font-size: 22px; border-width: 1px; border-style: none; border-color: black; border-radius: 10px;"
        )
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setStyleSheet(
            "background-color: #dddddd; color: #111111; height: 40px; font-size: 22px; border-width: 1px; border-style: none; border-color: black; border-radius: 10px;"
        )
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setStyleSheet(
            "background-color: #dddddd; color: #111111; height: 40px; font-size: 22px; border-width: 1px; border-style: none; border-color: black; border-radius: 10px;"
        )

        self.lap_button = QPushButton("Lap", self)
        self.lap_button.setStyleSheet(
            "background-color: #dddddd; color: #111111; height: 40px; font-size: 22px; border-width: 1px; border-style: none; border-color: black; border-radius: 10px;"
        )
        self.lap_button.setCursor(Qt.PointingHandCursor)

        self.lap_list = QListWidget(self)
        self.lap_list.setStyleSheet(
            "font-size: 18px; background-color: #333333; color: #eeeeee;"
        )

        self.start_button.setCursor(Qt.PointingHandCursor)
        self.stop_button.setCursor(Qt.PointingHandCursor)
        self.reset_button.setCursor(Qt.PointingHandCursor)
        self.lap_button.setCursor(Qt.PointingHandCursor)

        self.stopwatch_timer = QTimer(self)
        self.hbox_layout = QHBoxLayout()

        self.stopwatch_layout.addWidget(self.stopwatch_time_label)
        self.stopwatch_layout.addWidget(self.lap_list)
        self.stopwatch_layout.addLayout(self.hbox_layout)
        self.stopwatch_time_label.setAlignment(Qt.AlignHCenter)
        self.stopwatch_time_label.setStyleSheet("font-size: 110px;")

        self.hbox_layout.addWidget(self.reset_button)
        self.hbox_layout.addWidget(self.start_button)
        self.hbox_layout.addWidget(self.stop_button)
        self.hbox_layout.addWidget(self.lap_button)

        self.reset_button.clicked.connect(self.reset)
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.lap_button.clicked.connect(self.lap)
        self.stopwatch_timer.timeout.connect(self.update_display)

        self.lap_count = 0

        self.tab_2.setLayout(self.stopwatch_layout)

        self.alarm_layout = QVBoxLayout()
        self.tab_3.setLayout(self.alarm_layout)
        self.alarm_label = QLabel("Comming soon...")
        self.alarm_label.setStyleSheet("font-size: 80px;")
        self.alarm_label.setAlignment(Qt.AlignCenter)
        self.alarm_layout.addWidget(self.alarm_label)

    def start(self):
        self.stopwatch_timer.start(10)

    def stop(self):
        self.stopwatch_timer.stop()

    def lap(self):
        if not self.stopwatch_timer.isActive():
            return
        self.lap_count += 1
        lap_time = self.format_time(self.time)
        self.lap_list.insertItem(0, f"Lap {self.lap_count}: {lap_time}")

    def reset(self):
        self.stopwatch_timer.stop()
        self.time = QTime(0, 0, 0, 0)
        # self.stopwatch_time_label.setText("00:00:00:00") I used this in the beginning and it worked fine
        # here is a cleaner way
        self.stopwatch_time_label.setText(self.format_time(self.time))
        self.lap_list.clear()
        self.lap_count = 0

    def format_time(self, time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        miliseconds = time.msec() // 10

        return f"{hours:02}:{minutes:02}:{seconds:02}.{miliseconds:02}"

    def update_display(self):
        self.time = self.time.addMSecs(10)
        self.stopwatch_time_label.setText(self.format_time(self.time))

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.time_label.setText(current_time)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Clock()
    window.show()
    sys.exit(app.exec_())
