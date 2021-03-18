from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton
from PyQt5.QtCore import pyqtSlot

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
        self.initUi()

    def initUi(self):
        """Inicjalizacja Startowego UI

        Ustawia wymiary okna, tytuł i połorzenie.
        Następnie pokazuje okno

        Obecnie tworzy jeden przycisk odpowiadający za wybranie pliku."""

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        choose_file_button = QPushButton("Choose file", self)
        choose_file_button.move(300, 250)
        choose_file_button.clicked.connect(self.on_click_choose_files)

        self.show()

    @pyqtSlot()
    def on_click_choose_files(self):
        """Funkcja określająca działanie przycisku przy kliknięciu.
        Otwiera okno wyszukiwania pojedyńczego pliku."""

        self.openFileNameDialog()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

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