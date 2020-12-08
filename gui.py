import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QPushButton

from main import generate_one


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        w_disp, h_disp = QApplication.desktop().width(), QApplication.desktop().height()
        width, height = 600, 100
        
        self.setWindowTitle('Генератор оскорблений')
        self.setGeometry((w_disp - width) // 2, (h_disp - height) // 2, width, height)
        self.setFixedSize(self.width(), self.height())

        self.button = QPushButton('Сгенерировать', self)
        self.button.resize(self.button.width() + 20, self.button.height() + 5)
        self.button.move((width - self.button.width()) // 2,
                         (height - self.button.height()) - 10)
        self.button.setFont(QFont('PT Sans', 10))
        
        self.result_field = QLineEdit(generate_one(), self)
        self.result_field.resize(width - 20, self.result_field.height() + 5)
        self.result_field.move(10, 10)
        self.result_field.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.result_field.setReadOnly(True)
        self.result_field.setFont(QFont('PT Sans', 11))

        self.button.clicked.connect(self.regenerate)

    def regenerate(self):
        self.result_field.setText(generate_one())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wndw = Window()
    wndw.show()
    app.exec()
