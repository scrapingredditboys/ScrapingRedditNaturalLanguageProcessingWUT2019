#!/usr/bin/env python3
import itertools
import math
import os
import string
import sys
import csv
from enum import Enum
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from gui_main_window import Ui_MainWindow


# TODO: result text size

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

        self.tabWidget.setCurrentWidget(self.tabWidget.findChild(QWidget, "commentsTimeTab"))

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

        # sentiment based on upvote ratio
        self.upvoteSubNameComboBox.currentIndexChanged.connect(self.sentiment_ratio)
        self.upvoteSpinBox.valueChanged.connect(self.sentiment_ratio)
        self.upvoteRawDataCheckBox.stateChanged.connect(self.sentiment_ratio)

        # comments based on time
        self.commentsTimeSubNameComboBox.currentIndexChanged.connect(self.comments_time)
        self.commentsWeekdayComboBox.currentIndexChanged.connect(self.comments_time)
        self.commentsTimeEdit.timeChanged.connect(self.comments_time)
        self.commentsTimeRawDataCheckBox.stateChanged.connect(self.comments_time)
        self.commentsTimeCombineDaysCheckBox.stateChanged.connect(lambda: self.combine_days_changed("commentsTime"))

    def scan_for_subreddits(self):
        with open(os.path.join(self.data_dir, self.classifiers_dir, "AverageWordUsageClassifier.csv")) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            return next(reader)[1:]

    def get_number_of_lines(self, path):
        with open(path) as file:
            return sum(1 for line in file) - 1

    def combine_days_changed(self, caller):
        if caller == "karmaTime":
            if self.karmaTimeCombineDaysCheckBox.isChecked():
                self.karmaWeekdayComboBox.setDisabled(True)
            else:
                self.karmaWeekdayComboBox.setEnabled(True)
            self.karma_time()
        elif caller == "commentsTime":
            if self.commentsTimeCombineDaysCheckBox.isChecked():
                self.commentsWeekdayComboBox.setDisabled(True)
            else:
                self.commentsWeekdayComboBox.setEnabled(True)
            self.comments_time()

    def karma_length(self):
        # karma based on length
        path = os.path.join(self.data_dir, self.tables_dir, "karma_of_comments_based_on_comment_length.csv")
        length = self.lengthSpinBox.value()
        sub = self.lengthSubNameComboBox.currentText()

        if length == 0:
            self.lengthResultLabel.setText("")
            self.lengthResultLabel.setDisabled(True)
            return
        # performance: save the max value for later
        if length > self.get_number_of_lines(path):
            self.lengthResultLabel.setText("NO COMMENTS OF LENGTH " + str(length) + " ON /r/" + sub)
            self.lengthResultLabel.setDisabled(True)
            return

        print("Calculating karma for post of length", length, "on", sub, "...")
        # performance: maybe keep it opened in memory
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            if self.lengthRawDataCheckBox.isChecked():
                result = next(itertools.islice(reader, length, None))[self.subreddits.index(sub) + 1]
            else:
                total = 0
                i = 0
                lbound = math.floor(length / 50) * 50 + 1
                ubound = math.ceil(length / 50) * 50
                print(lbound, ubound)
                for row in list(reader)[lbound:ubound]:
                    total += float(row[self.subreddits.index(sub) + 1])
                    i += 1
                result = total / i

            print("Result:", result)
            if self.lengthRawDataCheckBox.isChecked():
                if float(result) < 0.00001:
                    result_string = " LENGTH " + str(length) + " NOT FOUND"
                else:
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
        # performance: maybe keep it opened in memory
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            raw = self.karmaTimeRawDataCheckBox.isChecked()
            if raw:
                if combine_days:
                    result = next(itertools.islice(reader, time.hour() + 1, None))[self.subreddits.index(sub) + 1]
                else:
                    result = next(itertools.islice(reader, weekday * 24 + time.hour() + 1,
                                                   None))[self.subreddits.index(sub) + 2]
            else:
                total = 0
                i = 0
                lbound = math.floor(time.hour() / 3) * 3
                ubound = math.ceil((time.hour() + 1) / 3) * 3
                if combine_days:
                    for row in list(reader)[lbound + 1:ubound + 1]:
                        total += float(row[self.subreddits.index(sub) + 1])
                        print(total)
                        i += 1
                    result = total / i
                else:
                    for row in list(reader)[weekday * 24 + lbound + 1:weekday * 24 + ubound + 1]:
                        total += float(row[self.subreddits.index(sub) + 2])
                        print(total)
                        i += 1
                    result = total / i
            print("Result:", result)
            if raw:
                result_string = str(result)
            else:
                if combine_days:
                    result_string = "Posting at " + time.toString("hh:mm") + " on /r/" + sub + " results in " \
                                    + str(round(result)) + " karma on average"
                else:
                    result_string = "Posting at " + time.toString("hh:mm") + " on " \
                                    + self.karmaWeekdayComboBox.currentText() + " on /r/" + sub + " results in " \
                                    + str(round(result)) + " karma on average"
            self.karmaTimeResultLabel.setEnabled(True)
            self.karmaTimeResultLabel.setText(result_string)

    def comments_time(self):
        # comments based on time
        time = self.commentsTimeEdit.time()
        sub = self.commentsTimeSubNameComboBox.currentText()
        combine_days = self.commentsTimeCombineDaysCheckBox.isChecked()
        result_label = self.commentsTimeResultLabel

        path = os.path.join(self.data_dir, self.tables_dir, "number_of_comments_based_on_weekday_and_hour.csv")
        if combine_days:
            print("Calculating # of comments for post at", time.toString("hap"), "on", sub, "...")
        else:
            weekday = self.commentsWeekdayComboBox.currentIndex()
            print("Calculating # of comments for post at", time.toString("hap"), "on",
                  self.commentsWeekdayComboBox.currentText(), "on", sub, "...")
        # performance: maybe keep it opened in memory
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            raw = self.commentsTimeRawDataCheckBox.isChecked()
            if raw:
                if combine_days:
                    total = 0
                    for i in range(0, 7):
                        for _, row in enumerate(reader):
                            if row[1] == time.toString("hap"):
                                total += int(row[self.subreddits.index(sub) + 2])
                                break
                    result = round(total/7)
                else:
                    result = next(itertools.islice(reader, weekday * 24 + time.hour() + 1,
                                                   None))[self.subreddits.index(sub) + 2]
            else:
                total = 0
                lbound = math.floor(time.hour() / 3) * 3
                ubound = math.ceil((time.hour() + 1) / 3) * 3
                if combine_days:
                        for i in range(7):
                            for row in list(reader)[lbound + 1:ubound + 1]:
                                total += float(row[self.subreddits.index(sub) + 2])
                                print(total)
                        result = total / (3*7)
                else:
                    for row in list(reader)[weekday * 24 + lbound + 1:weekday * 24 + ubound + 1]:
                        total += float(row[self.subreddits.index(sub) + 2])
                        print(total)
                    result = total / 3
            print("Result:", result)
            if raw:
                result_string = str(result)
            else:
                if combine_days:
                    result_string = "Posting at " + time.toString("hh:mm") + " on /r/" + sub + " results in " \
                                    + str(round(result)) + " comments on average"
                else:
                    result_string = "Posting at " + time.toString("hh:mm") + " on " \
                                    + self.karmaWeekdayComboBox.currentText() + " on /r/" + sub + " results in " \
                                    + str(round(result)) + " comments on average"
        result_label.setText(result_string)
        result_label.setEnabled(True)

    def sentiment_ratio(self):
        raw = self.upvoteRawDataCheckBox.isChecked()
        ratio = self.upvoteSpinBox.value()
        if ratio < 62:
            ratio_index = ratio - 59
        else:
            if ratio == 62:
                ratio_index = 4 # because there's no ratio 0.62 in tables...
            ratio_index = ratio - 60
        sub = self.upvoteSubNameComboBox.currentText()
        result_label = self.upvoteResultLabel
        path_pos = os.path.join(self.data_dir, self.tables_dir,
                               "positive_sentiments_of_submissions_based_on_upvote_ratio.csv")
        path_neg = os.path.join(self.data_dir, self.tables_dir,
                               "negative_sentiments_of_submissions_based_on_upvote_ratio.csv")
        with open(path_pos) as csvfile_pos, open(path_neg) as csvfile_neg:
            reader_pos = csv.reader(csvfile_pos, delimiter=self.csv_delimiter)
            reader_neg = csv.reader(csvfile_neg, delimiter=self.csv_delimiter)
            if raw:
                result_pos = next(itertools.islice(reader_pos, ratio_index, None))[self.subreddits.index(sub) + 1]
                result_neg = next(itertools.islice(reader_neg, ratio_index, None))[self.subreddits.index(sub) + 1]
                print(result_neg, result_pos)
            else:
                total_pos = 0
                total_neg = 0
                lbound = math.floor(ratio_index / 3) * 3 + 1
                ubound = math.ceil((ratio_index + 1) / 3) * 3 + 1
                for row in list(reader_pos)[lbound:ubound]:
                    total_pos += float(row[self.subreddits.index(sub) + 1])
                for row in list(reader_neg)[lbound:ubound]:
                    total_neg += float(row[self.subreddits.index(sub) + 1])
                result_pos = total_pos / 3
                result_neg = total_neg / 3

            print("Result: pos ", result_pos, " neg: ", result_neg)
            if math.fabs(float(result_pos)) < 0.00001 and abs(float(result_neg)) < 0.00001:
                result_string = "DATA NOT AVAILABLE"
            else:
                if raw:
                    result_string = "positive: " + str(result_pos) + " negative: " + str(result_neg)
                else:
                    result_string = "A post with upvote ratio " + str(ratio) + "% on /r/" + sub + " is likely to have " \
                                    + "positive sentiment with probability: " + str(math.fabs(round(result_pos, 2))) + \
                                    ", and negative with: " + str(math.fabs(round(result_neg, 2)))
            result_label.setText(result_string)
            result_label.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
