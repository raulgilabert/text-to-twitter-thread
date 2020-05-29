from PyQt5.Qt import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton
from PyQt5.Qt import QFont, QAction

import sys
import pprint


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.titleFont = QFont()
        self.titleFont.setBold(True)
        self.titleFont.setPixelSize(24)

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
        self.text.setMinimumHeight(self.height-90)
        self.text.move(5, 50)

        # Publish button
        self.send = QPushButton(self)
        self.send.setText("Publish")
        self.send.setMinimumWidth(self.width-10)
        self.send.move(5, self.height-35)
        self.send.clicked.connect(self.publish)

        # Create the menu bar
        menu = self.menuBar()
        actions = menu.addMenu("&Actions")

        # Clear the text box
        new = QAction("&New", self)
        new.setShortcut("Ctrl+N")
        new.setStatusTip("Clear the window")
        new.triggered.connect(self.text.clear)
        actions.addAction(new)

        # Rewrite the access credentials
        credentials = QAction("&Change credentials", self)
        credentials.setShortcut("Ctrl+R")
        credentials.setStatusTip("Change the credentials")
        actions.addAction(credentials)

        # Exit from the app
        exit = QAction("&Exit", self)
        exit.setShortcut("Ctrl+Q")
        exit.setStatusTip("Exit from the app")
        exit.triggered.connect(sys.exit)
        actions.addAction(exit)

    def publish(self):
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
            if i == len(text):
                listPar.append(text[initChar:i])

            i += 1

        # Dividing the text into 280 or less characters strings
        listTweets = []
        listDots = []

        for par in listPar:
            # Remove from the list the paragraph without text
            if len(par) <= 280:
                listTweets.append(par)
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
                        listTweets.append(par[initChar:listDots[i-1]+1])

                        initChar = listDots[i-1] + 2

                    # Check is the dot is the last one in the list
                    # If true, add it to the list
                    if i == len(listDots)-2:
                        listTweets.append(par[initChar:listDots[i]+1])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
