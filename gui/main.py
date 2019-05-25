#!/usr/bin/env python3
import itertools
import os
import string
import sys
import csv
from enum import Enum
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from gui_main_window import Ui_MainWindow

#TODO: result text size

class DaysOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class MainWindow(QMainWindow, Ui_MainWindow):
    data_dir = "data"
    classifiers_dir = "classifiers"
    tables_dir = "data_tables"
    csv_delimiter = ','
    subreddits = []

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("REDDIT CALCULATOR xD")

        # populate comboboxes with subreddits
        self.subreddits = self.scan_for_subreddits()
        for sub in self.subreddits:
            self.commentsTimeSubNameComboBox.addItem(sub)
            self.karmaTimeSubNameComboBox.addItem(sub)
            self.lengthSubNameComboBox.addItem(sub)
            self.meanSentimentSubNameComboBox.addItem(sub)
            self.upvoteSubNameComboBox.addItem(sub)

        # populate comboboxes with days of week
        for day in DaysOfWeek:
            day = str(day.name).title()
            self.commentsWeekdayComboBox.addItem(day)
            self.karmaWeekdayComboBox.addItem(day)
            self.meanSentimentWeekdayComboBox.addItem(day)

        # karma based on length
        self.lengthSubNameComboBox.currentIndexChanged.connect(self.karma_length)
        self.lengthSpinBox.valueChanged.connect(self.karma_length)
        self.lengthRawDataCheckBox.stateChanged.connect(self.karma_length)

        # karma based on time
        self.karmaTimeSubNameComboBox.currentIndexChanged.connect(self.karma_time)
        self.karmaWeekdayComboBox.currentIndexChanged.connect(self.karma_time)
        self.karmaTimeEdit.timeChanged.connect(self.karma_time)
        self.karmaTimeRawDataCheckBox.stateChanged.connect(self.karma_time)
        self.karmaTimeCombineDaysCheckBox.stateChanged.connect(lambda: self.combine_days_changed("karmaTime"))

        self.tabWidget.setCurrentWidget(self.tabWidget.findChild(QWidget, "timeTab"))

    def scan_for_subreddits(self):
        with open(os.path.join(self.data_dir, self.classifiers_dir, "AverageWordUsageClassifier.csv")) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            return next(reader)[1:]

    def get_number_of_lines(self, path):
        with open(path) as file:
            return sum(1 for line in file)

    def combine_days_changed(self, caller):
        if caller == "karmaTime":
            if self.karmaTimeCombineDaysCheckBox.isChecked():
                self.karmaWeekdayComboBox.setDisabled(True)
            else:
                self.karmaWeekdayComboBox.setEnabled(True)
            self.karma_time()


    def karma_length(self):
        path = os.path.join(self.data_dir, self.tables_dir, "karma_of_comments_based_on_comment_length.csv")
        #TODO: performance: maybe move it somewhere else
        self.lengthSpinBox.setMaximum(self.get_number_of_lines(path))
        # karma based on length
        length = self.lengthSpinBox.value()
        sub = self.lengthSubNameComboBox.currentText()
        if length == 0:
            self.lengthResultLabel.setText("")
            self.lengthResultLabel.setDisabled(True)
            return
        print("Calculating karma for post of length", length, "on", sub, "...")
        #TODO: performance: maybe keep it opened in memory
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            result = next(itertools.islice(reader, length, None))[self.subreddits.index(sub) + 1]
            print("Result:", result)
            if self.lengthRawDataCheckBox.isChecked():
                result_string = str(result)
            else:
                result_string = "A post of length " + str(length) + " on /r/" + sub + " gains " \
                                + str(result) + " karma on average"
            self.lengthResultLabel.setEnabled(True)
            self.lengthResultLabel.setText(result_string)

    def karma_time(self):
        time = self.karmaTimeEdit.time()
        sub = self.karmaTimeSubNameComboBox.currentText()
        # karma based on time
        combine_days = self.karmaTimeCombineDaysCheckBox.isChecked()
        if combine_days:
            path = os.path.join(self.data_dir, self.tables_dir, "karma_of_comments_based_on_hour.csv")
            print("Calculating karma for post at", time.toString("hap"), "on", sub, "...")
        else:
            path = os.path.join(self.data_dir, self.tables_dir, "karma_of_comments_based_on_weekday_and_hour.csv")
            weekday = self.karmaWeekdayComboBox.currentIndex()
            print("Calculating karma for post at", time.toString("hap"), "on", self.karmaWeekdayComboBox.currentText(),
                  "on", sub, "...")
        #TODO: performance: maybe keep it opened in memory
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            if combine_days:
                result = next(itertools.islice(reader, time.hour() + 1, None))[self.subreddits.index(sub) + 1]
            else:
                result = next(itertools.islice(reader, weekday * 24 + time.hour() + 1,
                                               None))[self.subreddits.index(sub) + 2]
            print("Result:", result)
            if self.karmaTimeRawDataCheckBox.isChecked():
                result_string = str(result)
            else:
                if combine_days:
                    result_string = "Posting at " + time.toString("hh:mm") + " on /r/" + sub + " results in " \
                                    + str(result) + " karma on average"
                else:
                    result_string = "Posting at " + time.toString("hh:mm") + " on " \
                                    + self.karmaWeekdayComboBox.currentText() + " on /r/" + sub + " results in " \
                                    + str(result) + " karma on average"
            self.karmaTimeResultLabel.setEnabled(True)
            self.karmaTimeResultLabel.setText(result_string)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
