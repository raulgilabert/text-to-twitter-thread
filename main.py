from PyQt5.Qt import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton
from PyQt5.Qt import QFont, QAction

import sys


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
