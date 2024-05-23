import AiVirtualMouseProcessing as avmp

import sys
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QDialog, QFormLayout, QDialogButtonBox
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QIntValidator
import PySide6.QtAsyncio as QtAsyncio
import asyncio

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Налаштування')
        
        # Form layout for settings input
        layout = QFormLayout()
        
        self.setting1 = QLineEdit()
        self.setting1.setValidator(QIntValidator())
        layout.addRow('Налаштування 1:', self.setting1)
        
        self.setting2 = QLineEdit()
        self.setting2.setValidator(QIntValidator())
        layout.addRow('Налаштування 2:', self.setting2)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)
        
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Головне вікно')
        
        layout = QVBoxLayout()
        
        # Buttons
        self.start_button = QPushButton('Запустити програму')
        self.start_button.clicked.connect(self.start_program)
        
        self.start_button_camera = QPushButton('Запустити програму із зображенням вебкамери')
        self.start_button_camera.clicked.connect(self.start_program_camera)
        
        self.settings_button = QPushButton('Налаштування')
        self.settings_button.clicked.connect(self.open_settings)
        
        layout.addWidget(self.settings_button)
        layout.addWidget(self.start_button_camera)
        layout.addWidget(self.start_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.mouse = None
    
    def start_program(self):
        if self.mouse is None:
            self.mouse = avmp.AiVirtualMouse()
            self.thread = QThread()
            self.mouse.moveToThread(self.thread)
            self.mouse.SetupRun(running=True, ShowVideo=False)
            self.thread.started.connect(self.mouse.run)
            self.mouse.finished.connect(self.thread.quit)
            self.mouse.finished.connect(self.mouse.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
            self.start_button.setText("Зупинити програму")
        else:
            self.mouse.Stop()
            self.start_button.setText("Запустити програму")
            self.mouse = None
            

    def start_program_camera(self):
        if self.mouse is None:
            self.mouse = avmp.AiVirtualMouse()
            self.thread = QThread()
            self.mouse.moveToThread(self.thread)
            self.mouse.SetupRun(running=True, ShowVideo=True)
            self.thread.started.connect(self.mouse.run)
            self.mouse.finished.connect(self.thread.quit)
            self.mouse.finished.connect(self.mouse.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
            self.start_button_camera.setText("Зупинити програму із зображенням камери")
        else:
            self.mouse.Stop()
            self.start_button_camera.setText("Запустити програму із зображенням камери")
            self.mouse = None

    def open_settings(self):
        settings_dialog = SettingsWindow()
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            print("Налаштування збережені:")
            print("Налаштування 1:", settings_dialog.setting1.text())
            print("Налаштування 2:", settings_dialog.setting2.text())

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
