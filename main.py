import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from MainWindow import *

def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    # Start the event loop.
    app.exec_()

if __name__ == "__main__":
    main()