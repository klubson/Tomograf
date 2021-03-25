from PyQt5.QtWidgets import QDialog, QPushButton, QSlider, QFileDialog, QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap


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

        self.width = 640
        self.height = 480

        self.resize(self.width, self.height)

        self.close_button = QPushButton("Close", self)
        self.save_button = QPushButton("Save", self)

        self.picture_slider = QSlider(Qt.Horizontal)

        self.result_picture = QPixmap()
        self.sinogram_picture = QPixmap()
        self.sinogram_picture_label = QLabel()
        self.result_picture_label = QLabel()

        self.main_layout = QVBoxLayout()
        self.picture_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()

        self.fileName = ""

        self.setupUI()

    def setupUI(self):

        self.main_layout.addLayout(self.picture_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.picture_slider)
        self.main_layout.addLayout(self.button_layout)

        self.picture_layout.addWidget(self.sinogram_picture_label)
        self.picture_layout.addWidget(self.result_picture_label)

        self.button_layout.addWidget(self.close_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.on_click_save)
        self.close_button.clicked.connect(self.on_click_close)

        self.setLayout(self.main_layout)

    @pyqtSlot()
    def on_click_save(self):
        self.saveFileDialog()

    @pyqtSlot()
    def on_click_close(self):
        self.close()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)