from PyQt5.Qt import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton
from PyQt5.Qt import QFont, QAction, QInputDialog, QLineEdit, QMessageBox
from PyQt5.Qt import QCheckBox

import sys
import os
import tweepy
import requests
import json
import pprint


# Return the authentication keys
def requestKeys(self):
    # Check if keys file exist
    try:
        keys = json.load(open("keys.json", "r"))

        return keys

    except FileNotFoundError:
        return changeKeys(self)


def changeKeys(self):
    # Consumer key
    ok = False
    while not ok:
        consumerKey, ok = QInputDialog.getText(
                                               self,
                                               "CONSUMER KEY",
                                               "Consumer key: ",
                                               QLineEdit.Normal, "")

    # Consumer secret
    ok = False
    while not ok:
        consumerSecret, ok = QInputDialog.getText(
                                                  self,
                                                  "CONSUMER SECRET",
                                                  "Consumer secret: ",
                                                  QLineEdit.Normal, "")

    # Access token
    ok = False
    while not ok:
        accessToken, ok = QInputDialog.getText(
                                               self,
                                               "ACCESS TOKEN",
                                               "Access token: ",
                                               QLineEdit.Normal, "")

    # Access token secret
    ok = False
    while not ok:
        accessTokenSecret, ok = QInputDialog.getText(
                                                     self,
                                                     "ACCESS TOKEN SECRET",
                                                     "Access token secret: ",
                                                     QLineEdit.Normal, "")

    keys = {
        "consumer_key": consumerKey,
        "consumer_secret": consumerSecret,
        "access_token": accessToken,
        "access_token_secret": accessTokenSecret
    }

    json.dump(keys, open("keys.json", "w"))

    return keys


# Receive link of an image and download it for publish on the tweet
def filename(url):
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

    return filename


# Login in Twitter
def login(self):
    # Authentication to access to Twitter
    keys = requestKeys(self)

    auth = tweepy.OAuthHandler(
        keys["consumer_key"],
        keys["consumer_secret"]
        )
    auth.set_access_token(
        keys["access_token"],
        keys["access_token_secret"]
        )

    global api
    api = tweepy.API(auth)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Login on the account
        login(self)

        # Create the title font
        self.titleFont = QFont()
        self.titleFont.setBold(True)
        self.titleFont.setPixelSize(24)

        # Create the window
        self.width = 750
        self.height = 475

        self.setGeometry(10, 10, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.initUI()

        self.show()

    def initUI(self):
        # Title
        title = QLabel(self)
        title.setFont(self.titleFont)
        title.setText("TEXT TO THREAD")
        title.setMinimumWidth(int(self.width/2))
        title.move(5, 22)

        # Text box
        self.text = QTextEdit(self)
        self.text.setMinimumWidth(self.width-10)
        self.text.setMinimumHeight(self.height-110)
        self.text.move(5, 50)

        # Publish button
        self.send = QPushButton(self)
        self.send.setText("Publish")
        self.send.setMinimumWidth(self.width-10)
        self.send.move(5, self.height-35)
        self.send.clicked.connect(self.convertToThread)

        # Add images checkbox
        self.images = QCheckBox(self)
        self.images.setText("Add images")
        self.images.move(10, self.height - 62)

        # Create the menu bar
        menu = self.menuBar()
        actions = menu.addMenu("&Actions")

        # Clear the text box
        new = QAction("&New", self)
        new.setShortcut("Ctrl+N")
        new.setStatusTip("Clear the window")
        new.triggered.connect(self.text.clear)
        actions.addAction(new)

        # Send the tweets
        send = QAction("&Send", self)
        send.setShortcut("Ctrl+Return")
        send.setStatusTip("Send the tweets")
        send.triggered.connect(self.convertToThread)
        actions.addAction(send)

        # Rewrite the access credentials
        credentials = QAction("&Change credentials", self)
        credentials.setShortcut("Ctrl+R")
        credentials.setStatusTip("Change the credentials, restart required")
        credentials.triggered.connect(self.changeKeys)
        actions.addAction(credentials)

        # Exit from the app
        exit = QAction("&Exit", self)
        exit.setShortcut("Ctrl+Q")
        exit.setStatusTip("Exit from the app")
        exit.triggered.connect(sys.exit)
        actions.addAction(exit)

    def changeKeys(self):
        # Ask if user wants to continue
        # If true, change credentials and close the app
        yesNo = QMessageBox.question(self, "", "Restart required, continue?",
                                     QMessageBox.Yes | QMessageBox.No)

        if yesNo == QMessageBox.Yes:
            changeKeys(self)
            sys.exit()

    def convertToThread(self):
        # Get the text from the input
        text = self.text.toPlainText()

        # Create a list and fill it with the paragraphs
        listPar = []

        initChar = 0
        i = 0

        for char in text:
            # Check if change of line, if true, add the paragraph to the list
            if char == "\n":
                listPar.append(text[initChar:i])

                initChar = i + 1

            # Check if end of the text, if true, add the paragraph to the list
            if i == len(text)-1:
                listPar.append(text[initChar:i+1])

            i += 1

        # Dividing the text into 280 or less characters strings
        self.listTweets = []
        listDots = []

        for par in listPar:
            # Remove from the list the paragraph without text
            if len(par) <= 280:
                self.listTweets.append(par)
            else:
                # Select the points where are "."
                listDots = []
                initChar = 0

                for i in range(0, len(par)):
                    if par[i] == ".":
                        listDots.append(i)

                # Pass in the dots list
                for i in range(0, len(listDots)-1):
                    # Check if the dot position is more than 280
                    # If true add it to the tweets list
                    if listDots[i] - initChar > 280:
                        self.listTweets.append(par[initChar:listDots[i-1]+1])

                        initChar = listDots[i-1] + 2

                    # Check is the dot is the last one in the list
                    # If true, add it to the list
                    if i == len(listDots)-2:
                        self.listTweets.append(par[initChar:listDots[i]+1])

        # Remove empty tweets from the list
        for tweet in self.listTweets:
            if tweet == "":
                self.listTweets.remove(tweet)

        # Check if checkbox is checked, if true, execute add images function
        # If not, convert tweets format and publish them
        if self.images.isChecked():
            self.addImages()
        else:
            self.tweets = []
            for tweet in self.listTweets:
                self.tweets.append({
                    "tweet": tweet,
                    "image": ""
                })

            self.publish()

    def addImages(self):
        self.tweets = []

        for tweet in self.listTweets:
            # Ask if add add image
            message = 'Add an image to the tweet: "' + tweet + '"?'

            yesNo = QMessageBox.question(self, "Do you want to add an image?",
                                         message,
                                         QMessageBox.Yes | QMessageBox.No)

            # Ask the link of the image
            if yesNo == QMessageBox.Yes:
                url, ok = QInputDialog.getText(self, "Image URL",
                                               "Image URL: ",
                                               QLineEdit.Normal, "")

                self.tweets.append({
                    "tweet": tweet,
                    "image": url
                })

        self.publish()

    def publish(self):
        i = 0

        # Pass into the tweets
        for tweet in self.tweets:
            i += 1

            # Check if the tweet has an image
            if tweet["image"] == "":
                # Check if the tweet is a response or the first and send it
                if i == 1:
                    status = api.update_status(tweet["tweet"])
                else:
                    status = api.update_status(tweet["tweet"],
                                               in_reply_to_status_id=status.id)
            else:
                # Download the image
                file = filename(tweet["image"])

                # Check if the tweet is a response or the first and send it
                if i == 1:
                    status = api.update_with_media(file, status=tweet["tweet"])
                else:
                    status = api.update_with_media(file,
                                                   status=tweet["tweet"],
                                                   in_reply_to_status_id=status.id)

                os.remove(file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
