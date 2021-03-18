from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    """Klasa głównego okna aplikacji"""

    def __init__(self):
        """Inicjalizacja

        Ustala domyślne wymiary (640 x 480), tytuł i połorzenie okna
        oraz inicjuje startowe UI
        """

        super(MainWindow, self).__init__()
        self.title = "Tomograf"
        self.left = 650
        self.top = 300
        self.width = 640
        self.height = 480
        self.fileName = ""
        self.fileImage = QPixmap()
        self.label = QLabel()
        self.choose_file_button = QPushButton("Choose file", self)
        self.close_button = QPushButton("Close", self)
        self.continue_button = QPushButton("Continue", self)

        self.initUi()

    def initUi(self):
        """Inicjalizacja Startowego UI

        Ustawia wymiary okna, tytuł i połorzenie.
        Następnie pokazuje okno

        Obecnie tworzy jeden przycisk odpowiadający za wybranie pliku."""

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        main_layout = QVBoxLayout()
        file_choose_layout = QHBoxLayout()

        self.initButtons()

        file_choose_layout.addWidget(self.close_button)
        file_choose_layout.addStretch(1)
        file_choose_layout.addWidget(self.choose_file_button)
        file_choose_layout.addWidget(self.continue_button)

        main_layout.addWidget(self.label)
        main_layout.addStretch(1)
        main_layout.addLayout(file_choose_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.show()

    def initButtons(self):
        """Nadanie przyciskom funkcji"""
        self.choose_file_button.clicked.connect(self.on_click_choose_files)
        self.close_button.clicked.connect(self.close)
        # self.continue_button.clicked.connect()

    @pyqtSlot()
    def on_click_choose_files(self):
        """Funkcja określająca działanie przycisku przy kliknięciu.
        Otwiera okno wyszukiwania pojedyńczego pliku."""

        self.openFileNameDialog()

    def openFileNameDialog(self):
        """Funkcja potencajlnie wybiera plik i zapisuje jego ścieżkę."""

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if self.fileName != "":
            print(self.fileName)
            self.fileImage.load(self.fileName)
            self.label.setPixmap(self.fileImage)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)