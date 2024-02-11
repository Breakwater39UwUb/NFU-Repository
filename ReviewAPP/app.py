import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("Hello World!")
label.resize(800, 600)
label.show()

main_page = None

app.exec()