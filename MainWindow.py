from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QSlider, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap

from SliderBox import SliderBox

class MainWindow(QMainWindow):
    """Klasa głównego okna aplikacji"""

    def __init__(self):
        """Inicjalizacja

        Ustala domyślne wymiary (640 x 480), tytuł i położenie okna
        oraz inicjuje startowe UI
        """

        super(MainWindow, self).__init__()
        self.title = "Tomograf"
        self.left = 450
        self.top = 200
        self.width = 640
        self.height = 480
        self.fileName = ""
        self.fileImage = QPixmap()
        self.fileImageScaled = QPixmap()
        self.label = QLabel()
        self.choose_file_button = QPushButton("Choose file", self)
        self.close_button = QPushButton("Close", self)
        self.continue_button = QPushButton("Continue", self)
        self.file_choose_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()
        self.angle_slider = SliderBox("Angle:", 45, 270, 45)
        self.sensor_slider = SliderBox("Sensors:", 90, 720, 90)
        self.scan_count_slider = SliderBox("Scans:", 90, 720, 90)

        self.initUi()

    def initUi(self):
        """Inicjalizacja Startowego UI

        Ustawia wymiary okna, tytuł i położenie.
        Inicjalizuje przyciski i Layout.
        Następnie pokazuje okno"""

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label.setMinimumSize(1, 1)

        self.initButtons()
        self.initLayout()

        self.show()

    def initButtons(self):
        """Nadanie przyciskom funkcji"""
        self.choose_file_button.clicked.connect(self.on_click_choose_files)
        self.close_button.clicked.connect(self.close)
        self.continue_button.clicked.connect(self.on_click_continue)

    def initLayout(self):
        """Ustawienie layout"""
        self.file_choose_layout.addWidget(self.close_button)
        self.file_choose_layout.addStretch(1)
        self.file_choose_layout.addWidget(self.choose_file_button)
        self.file_choose_layout.addWidget(self.continue_button)

        self.main_layout.addWidget(self.label, 1)
        self.main_layout.addLayout(self.angle_slider)
        self.main_layout.addLayout(self.sensor_slider)
        self.main_layout.addLayout(self.scan_count_slider)
        self.main_layout.addLayout(self.file_choose_layout)

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    @pyqtSlot()
    def on_click_choose_files(self):
        """Funkcja określająca działanie przycisku przy kliknięciu.
        Otwiera okno wyszukiwania pojedyńczego pliku."""

        self.openFileNameDialog()

    def openFileNameDialog(self):
        """Funkcja potencajlnie wybiera plik i zapisuje jego ścieżkę."""

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Select a file", "",
                                                  "All Files (*);;IMG Files (*.jpg)", options=options)
        if self.fileName != "":
            print(self.fileName)
            self.fileImage.load(self.fileName)
            self.fileImageScaled = self.fileImage.scaled(
                self.label.frameGeometry().width(), self.label.frameGeometry().height(), Qt.KeepAspectRatio).copy()
            self.label.setPixmap(self.fileImageScaled)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.fileImageScaled = self.fileImage.scaled(
            self.label.frameGeometry().width(), self.label.frameGeometry().height(), Qt.KeepAspectRatio).copy()
        self.label.setPixmap(self.fileImageScaled)

    def on_click_continue(self):
        if self.fileName:
            print('good')
            algorithm = Algorithm(self.fileImage, self.angle_slider.getVal, self.sensor_slider.getVal, self.scan_count_slider.getVal)
        else:
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle('Error')
            error_dialog.setText('No file chosen!')
            error_dialog.exec_()
