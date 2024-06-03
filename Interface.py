import AiVirtualMouseProcessing as avmp
from settings import wCam, hCam, smoothening, press_length, camera


import sys
import threading

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QDialog, QFormLayout, QDialogButtonBox
from PyQt6.QtCore import QThread, pyqtSignal, Qt
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
        layout.addRow('Висота активної зони:', self.setting1)
        self.setting1.setPlaceholderText("1280")
        
        self.setting2 = QLineEdit()
        self.setting2.setValidator(QIntValidator())
        layout.addRow('Ширина активної зони:', self.setting2)
        self.setting2.setPlaceholderText("560")
        
        self.setting3 = QLineEdit()
        self.setting3.setValidator(QIntValidator())
        layout.addRow('Згладжування:', self.setting3)
        self.setting3.setPlaceholderText("5")
        
        self.setting4 = QLineEdit()
        self.setting4.setValidator(QIntValidator())
        layout.addRow('Відносна відстань натискань:', self.setting4)
        self.setting4.setPlaceholderText("40")
        
        self.setting5 = QLineEdit()
        self.setting5.setValidator(QIntValidator())
        layout.addRow('Джерело потоку відео:', self.setting5)
        self.setting5.setPlaceholderText("0")
        
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
        
        self.hints = QLabel("""Піднятий вказівний палець -- переміщення курсору
Підняті всі пальці -- натискання ЛКМ, у разі торкання кінчиків пальців
Підняті всі пальці -- затиснення ЛКМ, у разі тривалого торкання кінчиків пальців
Піднятий вказівний та середній пальці -- натискання ПКМ у разі торкання кінчиків пальців 
Піднятий мізинець -- прокрутка колесика мишки вгору, якщо мізинець знаходиться у верхній половині активної зони
Піднятий мізинець -- прокрутка колисика мишки вниз, якщо мізинець знаходиться у нижній половині активної зони""")
        # self.hints.setAlignment(Qt.AlignmentFlag.AlignCenter)


        layout.addWidget(self.settings_button)
        layout.addWidget(self.start_button_camera)
        layout.addWidget(self.start_button)
        layout.addWidget(self.hints)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
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
            print("Налаштування збережені")
            try:
                wCam = int(settings_dialog.setting1.text())
            except:
                print("hello")
            try:
                hCam = int(settings_dialog.setting2.text())
            except:
                pass
            try:
                smoothening = int(settings_dialog.setting3.text())
            except:
                pass
            try:
                press_length = int(settings_dialog.setting4.text())
            except:
                pass
            
            camera = int(settings_dialog.setting5.text())

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
