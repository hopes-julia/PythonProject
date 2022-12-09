import sys
import sqlite3

import csv
from random import sample
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QComboBox
from PyQt5.QtWidgets import QInputDialog, QPushButton, QWidget, QTableView, QPlainTextEdit
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

SCREEN_SIZE_main = [700, 500]
SCREEN_SIZE_sub = [1910, 975]
questions = []
answers = ["A", "B", "C", "D"]
prices = {14: "15 ◇ 1000000", 13: "14 ◇ 500000", 12: "13 ◇ 250000", 11: "12 ◇ 125000",
          10: "11 ◇ 64000", 9: "10 ◇ 32000", 8: "9 ◇ 16000", 7: "8 ◇ 8000", 6: "7 ◇ 4000", 5: "6 ◇ 2000",
          4: "5 ◇ 1000", 3: "4 ◇ 500", 2: "3 ◇ 300", 1: "2 ◇ 200", 0: "1 ◇ 100"}
countable = {14: 1000000, 13: 500000, 12: 250000, 11: 125000, 10: 64000, 9: 32000,
             8: 16000, 7: 8000, 6: 4000, 5: 2000, 4: 1000, 3: 500, 2: 300, 1: 200, 0: 100}


class Error1(Exception):
    pass


class Error2(Exception):
    pass


class FirstSubWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('design3.ui', self)  # Загружаем дизайн
        self.label_7.hide()
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('redactor_db.db')
        db.open()
        # Создадим объект QSqlTableModel,
        # зададим таблицу, с которой он будет работать,
        #  и выберем все данные
        model = QSqlTableModel(self, db)
        model.setTable('redact')
        model.select()
        self.tableView.setModel(model)
        self.pushButton.clicked.connect(self.save_q)
        self.pushButton_2.clicked.connect(self.end)

    def save_q(self):
        print("ok")
        try:
            self.label_7.hide()
            q = self.lineEdit.text()
            a = self.lineEdit_2.text()
            b = self.lineEdit_3.text()
            c = self.lineEdit_4.text()
            d = self.lineEdit_5.text()
            cor = self.lineEdit_6.text().upper()
            if q == "" or a == "" or b == "" or c == "":
                raise Error2
            if d == "" or cor == "" or not cor.isalpha():
                raise Error2
            if cor.upper() not in answers:
                raise Error2
            if q[0].isdigit():
                raise Error2
            con = sqlite3.connect("redactor_db.db")
            cur = con.cursor()
            cur.execute("""insert into redact(Question, V1, V2, V3, V4, Answer)
                     values(?, ?, ?, ?, ?, ?)""", (q, a, b, c, d, cor))
            con.commit()
            con.close()
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.lineEdit_6.setText("")
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('redactor_db.db')
            db.open()
            # Создадим объект QSqlTableModel,
            # зададим таблицу, с которой он будет работать,
            #  и выберем все данные
            model = QSqlTableModel(self, db)
            model.setTable('redact')
            model.select()
            self.tableView.setModel(model)
        except:
            self.label_7.setText("Ошибка: некорректно введены данные")
            self.label_7.show()

    def end(self):
        FirstSubWindow.hide()


class SecondSubWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('design1.ui', self)  # Загружаем дизайн
        con = sqlite3.connect("redactor_db.db")
        cur = con.cursor()
        res = cur.execute("""select Question from redact""").fetchall()
        with open('try.csv', 'w', newline='', encoding="utf8") as csvfile:
            writer = csv.writer(
                csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in res:
                writer.writerow(i[0])
        self.quest = []
        with open('try.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for i in reader:
                self.quest.append("".join(i))
        print(self.quest)
        self.plainTextEdit.setEnabled(False)
        self.pushButton_3.hide()
        self.lineEdit.hide()
        self.label.hide()
        self.lineEdit_2.hide()
        self.label_2.hide()
        self.pushButton_4.hide()
        self.flag = 0
        self.pushButton_2.clicked.connect(self.choose2)
        self.pushButton.clicked.connect(self.choose)
        self.pushButton_5.clicked.connect(self.end)

    def choose2(self):
        try:
            self.label.hide()
            self.lineEdit_2.hide()
            self.label_2.hide()
            self.pushButton_4.hide()
            self.lineEdit.setText("")
            self.lineEdit.show()
            self.pushButton_3.show()
            self.flag = 2
            self.pushButton_3.clicked.connect(self.result)
        except:
            self.label_2.show()
            self.label_2.setText("Ошибка: неккоректно введено число")

    def result(self):
        try:
            self.label_2.hide()
            if self.lineEdit == "":
                raise Error1
            if self.flag == 1:
                print(self.lineEdit_2.text().split(","))
                self.chosen = [self.quest[int(i) - 1] for i in self.lineEdit_2.text().split(",")]
                stroka = "Список выбранных вопросов:" + "\n" + "\n".join(self.chosen)
                with open("question.txt", "wt", encoding="utf8") as f:
                    f.write("")
                    f.write("@".join([self.quest[int(i.strip()) - 1] for i in self.lineEdit_2.text().split(",")]))
                self.plainTextEdit.setPlainText(stroka)
                self.pushButton_4.show()
            elif self.flag == 2:
                try:
                    if int(self.lineEdit.text()) > 15:
                        raise Error1
                    self.spisok = list(sample(self.quest, int(self.lineEdit.text())))
                    print(self.spisok)
                    stroka = "Список выбранных вопросов:" + "\n" + "\n".join(self.spisok)
                    self.plainTextEdit.setPlainText(stroka)
                    with open("question.txt", "wt", encoding="utf8") as f:
                        f.write("")
                        f.write("@".join(list(sample(self.quest, int(self.lineEdit.text())))))
                    self.pushButton_4.show()
                except Error1:
                    self.label_2.show()
                    self.label_2.setText("Ошибка: количество выбранных вопросов не должно превышать 15")

        except Error1:
            self.pushButton_4.hide()
            self.label_2.setText("Ошибка: количество вопросов не указано")
            self.plainTextEdit.setPlainText("")
            self.label_2.show()
        except:
            self.pushButton_4.hide()
            self.label_2.setText("Ошибка: неккоректно введены данные")
            self.plainTextEdit.setPlainText("")
            self.label_2.show()

    def choose(self):
        self.label_2.hide()
        self.pushButton_4.hide()
        self.lineEdit.hide()
        self.lineEdit.setText("")
        stroka = "Список вопросов:" + "\n" + "\n".join(self.quest)
        with open("question.txt", "wt", encoding="utf8") as f:
            f.write("")
            f.write("@".join(self.quest))
        self.plainTextEdit.setPlainText(stroka)
        self.pushButton_3.show()
        self.label.show()
        self.lineEdit_2.show()
        self.flag = 1
        self.pushButton_3.clicked.connect(self.result)

    def end(self):
        SecondSubWindow.hide()


class ThirdSubWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('design2.ui', self)  # Загружаем дизайн
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit_2.setEnabled(False)
        self.pushButton_2.hide()
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_5.hide()
        self.pushButton_6.hide()
        self.plainTextEdit.hide()
        self.plainTextEdit_2.hide()
        self.con = sqlite3.connect("redactor_db.db")
        self.cur = self.con.cursor()
        with open("question.txt", "rt", encoding="utf8") as f:
            for i in f.read().split("@"):
                questions.append(i)
        print(questions)
        self.spisok = [prices[j] for j in range(len(questions))]
        self.j = 0
        self.itog = 0
        self.pushButton.clicked.connect(self.play)

    def correctA(self):
        print("!")
        if self.cur.execute("""select Answer from redact where Question = ?""", (self.i,)).fetchone()[0] == "A"\
                and self.j < len(questions):
            self.spisok[self.j] = self.spisok[self.j] + " ✅"
            self.plainTextEdit_2.setPlainText("\n".join(self.spisok) + "\n" + "Вы дали правильный ответ")
            self.itog += countable[self.j]
        elif self.j < len(questions):
            self.spisok[self.j] = self.spisok[self.j] + " ❌"
            self.plainTextEdit_2.setPlainText("\n".join(self.spisok) + "\n" + "Ваш ответ неверный")
        self.j += 1
        self.pushButton_6.show()
        self.pushButton_2.hide()
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_5.hide()
        self.pushButton_6.clicked.connect(self.play)
        print(self.j)

    def correctB(self):
        if self.cur.execute("""select Answer from redact where Question = ?""", (self.i,)).fetchone()[0] == "B"\
                and self.j < len(questions):
            self.spisok[self.j] = self.spisok[self.j] + " ✅"
            self.plainTextEdit_2.setPlainText("\n".join(self.spisok) + "\n" + "Вы дали правильный ответ")
            self.itog += countable[self.j]
        elif self.j < len(questions):
            self.spisok[self.j] = self.spisok[self.j] + " ❌"
            self.plainTextEdit_2.setPlainText("\n".join(self.spisok) + "\n" + "Ваш ответ неверный")
        self.j += 1
        self.pushButton_6.show()
        self.pushButton_2.hide()
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_5.hide()
        self.pushButton_6.clicked.connect(self.play)
        print(self.j)

    def correctC(self):
        if self.cur.execute("""select Answer from redact where Question = ?""", (self.i,)).fetchone()[0] == "C" \
                and self.j < len(questions):
            self.spisok[self.j] = self.spisok[self.j] + " ✅"
            self.plainTextEdit_2.setPlainText("\n".join(self.spisok) + "\n" + "Вы дали правильный ответ")
            self.itog += countable[self.j]
        elif self.j < len(questions):
            self.spisok[self.j] = self.spisok[self.j] + " ❌"
            self.plainTextEdit_2.setPlainText("\n".join(self.spisok) + "\n" + "Ваш ответ неверный")
        self.j += 1
        self.pushButton_6.show()
        self.pushButton_2.hide()
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_5.hide()
        self.pushButton_6.clicked.connect(self.play)
        print(self.j)

    def correctD(self):
        if self.cur.execute("""select Answer from redact where Question = ?""", (self.i,)).fetchone()[0] == "D"\
                and self.j < len(questions):
            self.spisok[self.j] = self.spisok[self.j] + " ✅"
            self.plainTextEdit_2.setPlainText("\n".join(self.spisok) + "\n" + "Вы дали правильный ответ")
            self.itog += countable[self.j]
        elif self.j < len(questions):
            self.spisok[self.j] = self.spisok[self.j] + " ❌"
            self.plainTextEdit_2.setPlainText("\n".join(self.spisok) + "\n" + "Ваш ответ неверный")
        self.j += 1
        self.pushButton_6.show()
        self.pushButton_2.hide()
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_5.hide()
        self.pushButton_6.clicked.connect(self.play)
        print(self.j)

    def play(self):
        self.pushButton_6.hide()
        self.pushButton_2.show()
        self.pushButton_3.show()
        self.pushButton_4.show()
        self.pushButton_5.show()
        self.plainTextEdit.show()
        self.plainTextEdit_2.show()
        self.pushButton.hide()
        self.plainTextEdit_2.setPlainText("\n".join(self.spisok))
        print(self.j < len(questions))
        print(self.j, questions)
        if self.j < len(questions):
            self.i = questions[self.j]
            text = self.i[0].upper() + self.i[1:] + "?"
            self.plainTextEdit.setPlainText(text)
            res = self.cur.execute("""select V1 from redact where Question = ?""", (self.i,)).fetchone()
            self.pushButton_2.setText("Вариант A: " + res[0])
            res = self.cur.execute("""select V2 from redact where Question = ?""", (self.i,)).fetchone()
            self.pushButton_3.setText("Вариант B: " + res[0])
            res = self.cur.execute("""select V3 from redact where Question = ?""", (self.i,)).fetchone()
            self.pushButton_4.setText("Вариант C: " + res[0])
            res = self.cur.execute("""select V4 from redact where Question = ?""", (self.i,)).fetchone()
            self.pushButton_5.setText("Вариант D: " + res[0])
            self.pushButton_2.clicked.connect(self.correctA)
            self.pushButton_3.clicked.connect(self.correctB)
            self.pushButton_4.clicked.connect(self.correctC)
            self.pushButton_5.clicked.connect(self.correctD)
        else:
            self.pushButton_2.hide()
            self.pushButton_3.hide()
            self.pushButton_4.hide()
            self.pushButton_5.hide()
            self.pushButton_6.hide()
            self.plainTextEdit.hide()
            self.plainTextEdit_2.setPlainText("\n".join(self.spisok) + "\n" + f"Набранная вами сумма: {self.itog}")


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, *SCREEN_SIZE_main)
        # self.showFullScreen()
        self.setWindowTitle('Отображение картинки')

        self.pixmap = QtGui.QPixmap('pict0.jpg')
        self.image = QLabel(self)
        self.image.move(75, 20)
        self.image.resize(400, 250)
        self.image.setPixmap(self.pixmap)

        self.btn = QPushButton(self)
        self.btn.resize(150, 50)
        self.btn.move(275, 325)
        self.btn.setText("Start")

        self.btn.clicked.connect(self.change1)

    def change1(self):
        text, ok_pressed = QInputDialog.getItem(self, "Выберите роль", "Кем вы хотите быть?",
                                                ("Редактор", "Ведущий", "Игрок"), 0, False)
        if ok_pressed:
            self.role = text
            if self.role == "Редактор":
                # self.change_red()
                self.sub_window = FirstSubWindow()
                # Button Event
                self.sub_window.show()
                self.btn.setText("Continuation")
            elif self.role == "Ведущий":
                # self.change_red()
                self.sub_window = SecondSubWindow()
                # Button Event
                self.sub_window.show()
                self.btn.setText("Continuation")
            elif self.role == "Игрок":
                # self.change_red()
                self.sub_window = ThirdSubWindow()
                # Button Event
                self.sub_window.show()
                self.btn.setText("Continuation")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
