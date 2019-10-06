from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QMainWindow
import sys
import functions


class MainWindow(QMainWindow):
    def __init__(self):
        # Create the main window
        super(MainWindow, self).__init__()
        self.height = 300
        self.width = 500
        self.setGeometry(200, 200, self.width, self.height)
        self.setWindowTitle("Twitbot")
        self.initUI()

    # Initialize the initial UI, or the main page
    def initUI(self):
        # Main label
        self.twitlabel = QLabel(self)
        self.twitlabel.setText("Twitbot")
        self.twitlabel.setGeometry(0, 0, 300, 100)
        self.twitlabel.setStyleSheet("font: 30pt Arial; background-color: rgb(66, 135, 245)")
        self.twitlabel.move((self.width / 2) - (self.twitlabel.width() / 2), (self.height / 4) - (self.twitlabel.height() / 2))
        self.twitlabel.setAlignment(Qt.AlignCenter)
        # Login button
        self.loginbutton = QPushButton(self)
        self.loginbutton.setStyleSheet("font: 13pt Arial")
        self.loginbutton.setGeometry(0, 0, 60, 40)
        self.loginbutton.setText("Login")
        self.loginbutton.move((self.width / 2) - (self.loginbutton.width() / 2), self.twitlabel.pos().y()+120)
        # Scrape button
        self.scrapebutton= QPushButton(self)
        self.scrapebutton.setText("Scrape")
        self.scrapebutton.setGeometry(0, 0, 64, 40)
        self.scrapebutton.setStyleSheet("font: 13pt Arial")
        self.scrapebutton.move(self.loginbutton.pos().x() - 2, self.loginbutton.pos().y()+self.scrapebutton.height())
        # Post tweet button
        self.tweetbutton = QPushButton(self)
        self.tweetbutton.setText("Post Tweet")
        self.tweetbutton.setGeometry(0, 0, 88, 40)
        self.tweetbutton.setStyleSheet("font: 13pt Arial")
        self.tweetbutton.move(self.loginbutton.pos().x() - 14, self.scrapebutton.pos().y() + self.scrapebutton.height())
        # go wild button
        self.gowildbutton = QPushButton(self)
        self.gowildbutton.setText("Go Wild")
        self.gowildbutton.setGeometry(0, 0, 88, 40)
        self.gowildbutton.setStyleSheet("font: 13pt Arial")
        self.gowildbutton.move(self.loginbutton.pos().x() - 14, self.tweetbutton.pos().y() + self.tweetbutton.height())

    def update(self):
        pass

    def bindfuncttobuttn(self, func, button):
        pass