from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QLabel, QLineEdit
from PyQt6.QtWidgets import QInputDialog, QTableWidgetItem, QDialog, QDialogButtonBox, QVBoxLayout
from PyQt6.QtWidgets import QWidget
import sys
from PyQt5 import uic
from random import randint
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QInputDialog
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import sqlite3

import sqlite3

conn = sqlite3.connect('players.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS players(
   player_id INTEGER PRIMARY KEY,
   name TEXT,
   password TEXT,
   points INTEGER
   );
""")
conn.commit()
more_info = [('admin', 'Abcf8712', 100), ('test', 'voieue44', 8)]
for name, password, points in more_info:
    cur.execute("""INSERT INTO players(name, password, points)
                    VALUES(?, ?, ?);""", (name, password, points))
    conn.commit()

cur.execute('''SELECT name, password, points FROM players''')
# for res in cur.fetchall():
#     print(res)
conn.close()


class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


keyboard = ('йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm')


def check_password(password):
    try:
        if len(password) <= 8:
            raise LengthError
        flag_lower = False
        flag_upper = False
        flag_digit = False
        for elem in password:
            if elem.isalpha():
                if elem.islower():
                    flag_lower = True
                else:
                    flag_upper = True
            elif elem.isdigit():
                flag_digit = True
        if not flag_lower or not flag_upper:
            raise LetterError
        if not flag_digit:
            raise DigitError
        for i in range(len(password) - 2):
            for j in range(len(keyboard)):
                if password[i:i + 3].lower() in keyboard[j]:
                    raise SequenceError
        return 'ok'
    except LengthError:
        return 'LengthError'
    except LetterError:
        return 'LetterError'
    except DigitError:
        return 'DigitError'
    except SequenceError:
        return 'SequenceError'


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # uic.loadUi('Log_reg_btn.ui', self)

    def initUI(self):
        self.resize(1920, 1080)
        self.setWindowTitle('Своя игра')
        self.setObjectName("Main")
        self.setStyleSheet("#Main{border-image:url(game.jpg)}")
        self.log = QPushButton('Войти', self)
        self.log.move(800, 500)
        self.log.resize(150, 80)
        self.reg = QPushButton('Зарегистрироваться', self)
        self.reg.move(800, 420)
        self.reg.resize(150, 80)
        self.reg.clicked.connect(self.registr)
        self.log.clicked.connect(self.enter)

        # self.pushButton.clicked.connect(self.run)
        # self.btn.clicked.connect(self.run)
        # self.btn.clicked.connect(self.paint)

    def enter(self):
        login, ok_pressed = QInputDialog.getText(
            self, "Вход", "Введите Логин")
        if ok_pressed:
            print(login)
            # self.reg.setText()
        password, ok_pressed = QInputDialog.getText(self, "Вход",
                                                    "Введите пароль")

    def registr(self):
        login, ok_pressed = QInputDialog.getText(
            self, "Регистрация", "Придумайте Логин")
        if ok_pressed:
            password, ok_pressed = QInputDialog.getText(self, "Регистрация",
                                                        "Придумайте пароль")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
