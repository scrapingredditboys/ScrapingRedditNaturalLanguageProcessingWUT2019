#!/usr/bin/env python3
import os
import sys
import csv
from PyQt5.QtWidgets import QMainWindow, QApplication
from gui_main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    data_dir = "data"
    classifiers_dir = "classifiers"
    tables_dir = "data_tables"
    csv_delimiter = ','

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("REDDIT CALCULATOR xD")
        subreddits = self.scan_for_subreddits()
        for sub in subreddits:
            self.commentsTimeSubNameComboBox.addItem(sub)
            self.karmaTimeSubNameComboBox.addItem(sub)
            self.lengthSubNameComboBox.addItem(sub)
            self.meanSentimentSubNameComboBox.addItem(sub)
            self.upvoteSubNameComboBox.addItem(sub)

    def scan_for_subreddits(self):
        with open(os.path.join(self.data_dir, self.classifiers_dir, "AverageWordUsageClassifier.csv")) as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            return next(reader)[1:]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
