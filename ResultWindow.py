from PyQt5.QtWidgets import QDialog, QPushButton
from PyQt5.QtCore import Qt


class ResultWindow(QDialog):
    """Okno do wyswietlania wyników

    TODO
    +---------------+--------------------+
    |               |                    |
    |               |                    |
    |     sinogram  |   wyjściowy        |
    |               |                    |
    |_______________|____________________|
    |                przyciski           |
    +------------------------------------+
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Wyniki")
        self.setWindowModality(Qt.ApplicationModal)
        self.test_button = QPushButton("OK")
        self.test_button.move(50, 50)

        self.temp = 0
        print("Hello world!")
