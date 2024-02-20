from PyQt5 import QtWidgets, QtGui, QtCore
import sys
app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle('美食評論系統')
Form.resize(600, 200)

label = QtWidgets.QLabel(Form)
label.setText('請選擇你是商家還是使用著')
label.setStyleSheet('font-size:20px;')
label.setGeometry(50,30,300,30)

btn = QtWidgets.QPushButton(Form)
btn.setText('商家')
btn.setStyleSheet('font-size:16px;')
btn.setGeometry(190,60,120,40)
btn.clicked.connect(lambda:Form2.show())  # 使用 lambda 函式，顯示新視窗

btn2 = QtWidgets.QPushButton(Form)
btn2.setText('使用著')
btn2.setStyleSheet('font-size:16px;')
btn2.setGeometry(40,60,120,40)
btn2.clicked.connect(lambda:Form3.show())

Form2 = QtWidgets.QWidget()               # 建立新視窗
Form2.setWindowTitle('商家')
Form2.resize(300, 200)

Form3 = QtWidgets.QWidget()               # 建立新視窗
Form3.setWindowTitle('使用著')
Form3.resize(300, 200)

Form4 = QtWidgets.QWidget()               # 建立新視窗
Form4.setWindowTitle('GOOGLE')
Form4.resize(300, 200)

Form5 = QtWidgets.QWidget()               # 建立新視窗
Form5.setWindowTitle('FOODPANDA')
Form5.resize(300, 200)

btn3 = QtWidgets.QPushButton(Form2)
btn4 = QtWidgets.QPushButton(Form2)
btn5 = QtWidgets.QPushButton(Form3)

label2 = QtWidgets.QLabel(Form2)
label3 = QtWidgets.QLabel(Form4)
label4 = QtWidgets.QLabel(Form5)


line = QtWidgets.QLineEdit(Form4)
line2 = QtWidgets.QLineEdit(Form5)
line3 = QtWidgets.QLineEdit(Form3)
line4 = QtWidgets.QLineEdit(Form3)

line.setGeometry(10,60,200,30)
line2.setGeometry(10,60,200,30)
line3.setGeometry(10,10,200,30)
line4.setGeometry(10,40,270,160)

label2.setText('請選擇平台')
label2.setStyleSheet('font-size:20px;')
label2.setGeometry(50,30,300,30)

label3.setText('請輸入網址: ')
label3.setStyleSheet('font-size:20px;')
label3.setGeometry(50,30,300,30)

label4.setText('請輸入網址: ')
label4.setStyleSheet('font-size:20px;')
label4.setGeometry(50,30,300,30)

btn3.setText('GOOGLE')
btn3.setStyleSheet('font-size:16px;')
btn3.setGeometry(50,60,120,40)
btn3.clicked.connect(lambda:Form4.show())

btn4.setText('FOODPANDA')
btn4.setStyleSheet('font-size:16px;')
btn4.setGeometry(190,60,120,40)
btn4.clicked.connect(lambda:Form5.show())

btn5.setText('送出')
btn5.setStyleSheet('font-size:16px;')
btn5.setGeometry(190,60,120,40)

Form.show()
sys.exit(app.exec_())