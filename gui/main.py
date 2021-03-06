#!/usr/bin/env python3
import csv
import itertools
import math
import os
import string
import sys
from enum import Enum

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from gui_main_window import Ui_MainWindow

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
    res_dir = "resources"
    classifiers_dir = "classifiers"
    tables_dir = "data_tables"
    csv_delimiter = ','
    output_round = 3
    subreddits = []

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("REDDIT CALCULATOR xD")
        self.setWindowIcon(QIcon(os.path.join(self.res_dir, "icon.png")))

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

        self.tabWidget.setCurrentWidget(self.tabWidget.findChild(QWidget, "subredditTab"))

        # guessing sub based on given text
        self.subredditGuessButtonR.clicked.connect(self.subreddit_guess)
        self.subredditGuessButtonL.setVisible(False)
        self.subredditGuessResultLabel.setVisible(False)
        self.subredditGuessResultLabel_2.setVisible(False)
        self.subredditGuessResultLabel_3.setVisible(False)
        self.subredditGuessButtonL.clicked.connect(self.subreddit_guess_details)

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

        # mean sentiments of comments
        self.meanSentimentSubNameComboBox.currentIndexChanged.connect(self.mean_sentiment)
        self.meanSentimentWeekdayComboBox.currentIndexChanged.connect(self.mean_sentiment)
        self.meanSentimentTimeEdit.timeChanged.connect(self.mean_sentiment)
        self.meanSentimentRawDataCheckBox.stateChanged.connect(self.mean_sentiment)
        self.meanSentimentCombineDaysCheckBox.stateChanged.connect(lambda: self.combine_days_changed("meanSentiment"))

        self.old_text = ""

    def scan_for_subreddits(self):
        with open(os.path.join(self.data_dir, self.classifiers_dir, "AverageWordUsageClassifier.csv"),
                  encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            return next(reader)[1:]

    def get_number_of_lines(self, path):
        with open(path, encoding="utf-8") as file:
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
        elif caller == "meanSentiment":
            if self.meanSentimentCombineDaysCheckBox.isChecked():
                self.meanSentimentWeekdayComboBox.setDisabled(True)
            else:
                self.meanSentimentWeekdayComboBox.setEnabled(True)
            self.mean_sentiment()

    def subreddit_guess(self):
        self.subreddit_less_details()
        self.subredditGuessResultLabel.setVisible(True)
        self.subredditGuessResultLabel.setText("")
        self.subredditGuessResultLabel_2.setVisible(False)
        self.subredditGuessResultLabel_3.setVisible(False)
        self.subredditGuessButtonL.setVisible(False)
        self.subredditGuessButtonR.setEnabled(False)
        self.subredditGuessButtonL.setEnabled(False)
        button_r_old_text = self.subredditGuessButtonR.text()
        self.subredditGuessButtonR.setText("Please wait...")
        sub_not_available = False
        emotion_not_available = False
        topic_not_available = False
        input = self.subredditGuessField.toPlainText()
        result_label = self.subredditGuessResultLabel
        path_sub = os.path.join(self.data_dir, self.classifiers_dir, "AverageWordUsageClassifier.csv")
        path_emotion = os.path.join(self.data_dir, self.classifiers_dir, "EmotionsClassifier.csv")
        path_topic = os.path.join(self.data_dir, self.classifiers_dir, "TopicsClassifier.csv")
        results = []
        result_label.setText("")
        self.update()

        scores = [0] * len(self.subreddits)
        # prepare words from input for processing
        table = str.maketrans({key: None for key in string.punctuation})
        input_stripped = input.strip().translate(table)
        words_cap = input_stripped.split(' ')
        words = []
        for word_cap in words_cap:
            words.append(word_cap.lower())

        words_set = set(words)

        # SUBREDDIT GUESSING
        # performance: no need to update every time
        # find all available words in the classifier
        available_words = []
        with open(path_sub, encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            for row in list(reader)[1:]:
                available_words.append(row[0])

            avail_set = set(available_words)
            intersect = words_set.intersection(avail_set)
            if len(intersect) < 3:
                sub_not_available = True

            for word in intersect:
                with open(path_sub, encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
                    for row in list(reader)[0:]:
                        if row[0] == word:
                            scores = [float(x) + y for x, y in zip(row[1:], scores)]
                            break

        candidates = []
        for i in range(3):
            candidates.append((self.subreddits[scores.index(max(scores))], max(scores)))
            scores[scores.index(max(scores))] = 0
        if candidates[0][0] == "WritingPrompts":
            candidates[0] = (candidates[0][0], candidates[0][1] * 0.85)
            candidates.sort(key=lambda tup: tup[1], reverse=True)
        l = []
        for pair in candidates:
            l.append(pair)
        results.append(l)

        # EMOTION GUESSING
        # find all available emotions in the classifier
        with open(path_emotion, encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            available_emotions = next(reader)[1:]

            # find all available words in the classifier
            emotion_available_words = []
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            for row in list(reader)[1:]:
                emotion_available_words.append(row[0])

            emotion_avail_set = set(emotion_available_words)
            emotion_intersect = words_set.intersection(emotion_avail_set)
            if len(emotion_intersect) < 3:
                emotion_not_available = True

        emotion_scores = [0] * len(available_emotions)
        found_count = 0
        for word in emotion_intersect:
            with open(path_emotion, encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
                for row in list(reader)[0:]:
                    if row[0] == word:
                        found_count += 1
                        emotion_scores = [float(x) + y for x, y in zip(row[1:], emotion_scores)]
                        break

        if max(emotion_scores) == 0:
            emotion_not_available = True
        else:
            for i in range(len(available_emotions)):
                emotion_scores[i] /= found_count
                emotion_scores[i] = round(emotion_scores[i], 3)

        l = []
        for i in range(3):
            l.append((available_emotions[i], emotion_scores[i]))
        results.append(l)

        # TOPIC GUESSING
        topic_words_topics = []
        with open(path_topic, encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            for row in list(reader)[1:]:
                if row[1] != "adjectives" and row[1] != "adverbs":
                    topic_words_topics.append((row[0], row[2]))

        # performance: definitely can be improved here
        topic_scores = {}
        for word in words_set:
            for word_topic in topic_words_topics:
                if word == word_topic[0]:
                    if word_topic[1] in topic_scores:
                        topic_scores[word_topic[1]] += 1
                    else:
                        topic_scores[word_topic[1]] = 0

        topic_scores = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        if len(topic_scores) > 2:
            if topic_scores[i][0] == 0:
                topic_not_available = True
            else:
                l = []
                for i in range(3):
                    if (topic_scores[i][1] != 0):
                        l.append((topic_scores[i][0], str(topic_scores[i][1])))
                results.append(l)
        else:
            topic_not_available = True

        result_label.setEnabled(True)

        # SUBREDDIT
        result_string = ["This text is"]
        if not sub_not_available:
            sub_score = results[0][0][1]
            if sub_score > 0.7:
                sub_likely = " very"
            elif sub_score < 0.4:
                sub_likely = " quite"
            elif sub_score < 0.1:
                sub_likely = " a bit"
            else:
                sub_likely = ""
            result_string.append("{0} likely to come from /r/{1}".format(sub_likely, results[0][0][0]))

        # EMOTIONS
        if not emotion_not_available:
            valence = results[1][0][1] - 0.5
            arousal = results[1][1][1] - 0.6
            if results[0][0][0] == "depression":
                valence -= 0.1
                if arousal >= 0:
                    arousal -= 0.1
                else:
                    arousal -= 0.1
            if valence == 0:
                valence += 0.0001
            theta = math.degrees(math.tan(arousal/valence) ** -1) % 360
            theta = round(theta) % 360
            if 0 <= theta < 30:
                emotion = "pleased"
            elif 30 <= theta < 60:
                emotion = "happy"
            elif 60 <= theta < 90:
                emotion = "excited"
            elif 90 <= theta < 120:
                emotion = "annoying"
            elif 120 <= theta < 150:
                emotion = "angry"
            elif 150 <= theta < 170:
                emotion = "nervous"
            elif 170 <= theta < 210:
                emotion = "sad"
            elif 210 <= theta < 250:
                emotion = "bored"
            elif 250 <= theta < 270:
                emotion = "sleepy"
            elif 270 <= theta < 300:
                emotion = "calm"
            elif 300 <= theta < 330:
                emotion = "peaceful"
            elif 330 <= theta <= 360:
                emotion = "relaxed"
            else:
                emotion = "relaxed"
            result_string.append(", the dominating emotion is {0}".format(emotion))
            results[1].append(("THETA (DEG)", round(theta)))
        # TOPIC
        if not topic_not_available:
            if emotion_not_available and sub_not_available:
                topic_score = results[0][0]
            elif emotion_not_available and not sub_not_available:
                topic_score = results[1][0]
            else:
                topic_score = results[2][0]
            result_string.append(", the topic is {0}".format(topic_score[0]))
        if len(result_string) <= 1:
            result_label.setText("DATA NOT AVAILABLE")
        else:
            for substring in result_string:
                result_label.setText(result_label.text() + substring)
            self.subredditGuessButtonL.setVisible(True)
        self.old_text = result_label.text()
        self.results = results
        self.sn_available = sub_not_available
        self.tn_available = topic_not_available
        self.en_available = emotion_not_available
        self.subredditGuessButtonR.setText(button_r_old_text)
        self.subredditGuessButtonR.setEnabled(True)
        self.subredditGuessButtonL.setEnabled(True)

    def subreddit_guess_details(self):
        self.subredditGuessResultLabel.setText("")
        self.subredditGuessResultLabel_2.setVisible(True)
        self.subredditGuessResultLabel_3.setVisible(True)
        result_labels = [self.subredditGuessResultLabel, self.subredditGuessResultLabel_2,
                         self.subredditGuessResultLabel_3]
        avail_flags = [ self.sn_available, self.en_available, self.tn_available ]
        result_types = [ "SUBREDDITS", "EMOTION COEFF.", "TOPICS" ]
        i = 0
        for results in self.results:
            result_labels[i].setText(result_types[i])
            if not avail_flags[i]:
                for result in results:
                    result_labels[i].setText("{0}\n{1}: {2}".format(result_labels[i].text(),
                                                                    result[0], result[1]))
            else:
                result_labels[i].setText("DATA NOT AVAILABLE")
            i += 1
        self.subredditGuessButtonL.clicked.disconnect(self.subreddit_guess_details)
        self.subredditGuessButtonL.clicked.connect(self.subreddit_less_details)
        self.subredditGuessButtonL.setText("Less details")

    def subreddit_less_details(self):
        result_labels = [self.subredditGuessResultLabel_2, self.subredditGuessResultLabel_3]
        for label in result_labels:
            label.setText("")
            label.setVisible(False)

        self.subredditGuessResultLabel.setText(self.old_text)
        self.subredditGuessButtonL.setText("More details")
        self.subredditGuessButtonL.clicked.connect(self.subreddit_guess_details)

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
        with open(path, encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            if self.lengthRawDataCheckBox.isChecked():
                result = next(itertools.islice(reader, length, None))[self.subreddits.index(sub) + 1]
            else:
                total = 0
                i = 0
                lbound = math.floor(length / 50) * 50 + 1
                ubound = math.ceil((length + 1) / 50) * 50
                print("calculating avg in the interval:", lbound, ubound)
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
                                + str(round(result, self.output_round)) + " karma on average"
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
        with open(path, encoding="utf-8") as csvfile:
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
                        i += 1
                    result = total / i
                else:
                    for row in list(reader)[weekday * 24 + lbound + 1:weekday * 24 + ubound + 1]:
                        total += float(row[self.subreddits.index(sub) + 2])
                        i += 1
                    result = total / i
            print("Result:", result)
            if raw:
                result_string = str(result)
            else:
                if combine_days:
                    result_string = "Posting at " + time.toString("hh:mm") + " on /r/" + sub + " results in " \
                                    + str(round(result, self.output_round)) + " karma on average"
                else:
                    result_string = "Posting at " + time.toString("hh:mm") + " on " \
                                    + self.karmaWeekdayComboBox.currentText() + " on /r/" + sub + " results in " \
                                    + str(round(result, self.output_round)) + " karma on average"
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
        with open(path, encoding="utf-8") as csvfile:
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
                    result = round(total / 7, self.output_round)
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
                    result = total / (3 * 7)
                else:
                    for row in list(reader)[weekday * 24 + lbound + 1:weekday * 24 + ubound + 1]:
                        total += float(row[self.subreddits.index(sub) + 2])
                    result = total / 3
            print("Result:", result)
            if raw:
                result_string = str(result)
            else:
                if combine_days:
                    result_string = "Posting at " + time.toString("hh:mm") + " on /r/" + sub + " results in " \
                                    + str(round(result, self.output_round)) + " comments on average"
                else:
                    result_string = "Posting at " + time.toString("hh:mm") + " on " \
                                    + self.karmaWeekdayComboBox.currentText() + " on /r/" + sub + " results in " \
                                    + str(round(result, self.output_round)) + " comments on average"
        result_label.setText(result_string)
        result_label.setEnabled(True)

    def sentiment_ratio(self):
        raw = self.upvoteRawDataCheckBox.isChecked()
        ratio = self.upvoteSpinBox.value()
        if ratio < 62:
            ratio_index = ratio - 59
        else:
            if ratio == 62:
                ratio_index = 4  # because there's no ratio 0.62 in tables...
            ratio_index = ratio - 60
        sub = self.upvoteSubNameComboBox.currentText()
        result_label = self.upvoteResultLabel
        path_pos = os.path.join(self.data_dir, self.tables_dir,
                                "positive_sentiments_of_submissions_based_on_upvote_ratio.csv")
        path_neg = os.path.join(self.data_dir, self.tables_dir,
                                "negative_sentiments_of_submissions_based_on_upvote_ratio.csv")
        with open(path_pos, encoding="utf-8") as csvfile_pos, open(path_neg, encoding="utf-8") as csvfile_neg:
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
                                    + "positive sentiment with probability: " + str(
                        math.fabs(round(result_pos, self.output_round))) + \
                                    ", and negative with: " + str(math.fabs(round(result_neg, self.output_round)))
            result_label.setText(result_string)
            result_label.setEnabled(True)

    def mean_sentiment(self):
        # mean sentiments of comments
        time = self.meanSentimentTimeEdit.time()
        sub = self.meanSentimentSubNameComboBox.currentText()
        combine_days = self.meanSentimentCombineDaysCheckBox.isChecked()
        result_label = self.meanSentimentResultLabel
        raw = self.meanSentimentRawDataCheckBox.isChecked()

        path = os.path.join(self.data_dir, self.tables_dir, "mean_sentiments_of_comments_based_on_weekday_and_hour.csv")
        if combine_days:
            print("Calculating mean sentiments of comments for post at", time.toString("hap"), "on", sub, "...")
        else:
            weekday = self.meanSentimentWeekdayComboBox.currentIndex()
            print("Calculating mean sentiments of comments for post at", time.toString("hap"), "on",
                  self.meanSentimentWeekdayComboBox.currentText(), "on", sub, "...")
        # performance: maybe keep it opened in memory
        with open(path, encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=self.csv_delimiter)
            if raw:
                if combine_days:
                    total = 0.0
                    for i in range(0, 7):
                        for _, row in enumerate(reader):
                            if row[1] == str(time.hour()):
                                total += float(row[self.subreddits.index(sub) + 2])
                                break
                    result = round(total / 7, self.output_round)
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
                    result = total / (3 * 7)
                else:
                    for row in list(reader)[weekday * 24 + lbound + 1:weekday * 24 + ubound + 1]:
                        total += float(row[self.subreddits.index(sub) + 2])
                    result = total / 3
            print("Result:", result)
            if raw:
                result_string = str(result)
            else:
                if combine_days:
                    result_string = "Posting at " + time.toString("hh:mm") + " on /r/" + sub
                else:
                    result_string = "Posting at " + time.toString("hh:mm") + " on " \
                                    + self.karmaWeekdayComboBox.currentText() + " on /r/" + sub
                result_string += " is "
                if abs(result) > 0.5:
                    result_string += "very"
                else:
                    result_string += "quite"
                result_string += " likely to have "
                if result >= 0:
                    result_string += "negative"
                else:
                    result_string += "positive"
                result_string += " sentiment."
        result_label.setText(result_string)
        result_label.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
