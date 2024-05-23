import Interface as i
import sys

app = i.QApplication(sys.argv)
window = app.MainWindow()
window.show()
sys.exit(app.exec())

