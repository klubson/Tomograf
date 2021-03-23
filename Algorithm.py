import numpy as np
import math
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage


class Algorithm:
    alfa = 0
    n = 0
    l = 0
    r = 0
    S = (0, 0)
    E = [0, 0]
    D = []
    image = QImage
    iterations = np.arange

    def __init__(self, picture, deltaAlfa, detectors, range):
        """Inicjalizacja klasy wykonującej obliczenia"""

        self.alfa = (360 - deltaAlfa) / 2 * -2 * math.pi
        """krok dla układu emiter/detektor - od użytkownika"""

        self.n = detectors
        """liczba detektorów - od użytkownika"""

        self.l = range / 360 * 2 * math.pi
        """Rozwartość/rozpiętość układu emiter/detektor - od użytkownika"""

        self.image = picture.toImage()
        """Obraz pobrany z komputera"""

        self.r = self.image.width() / 2
        """Promień okręgu wpisanego w obrazek - z wczytanego zdjęcia"""

        self.S = (0, 0)
        """Środek obrazka - z wczytanego zdjęcia"""

        self.E = [self.r * math.cos(0), self.r * math.sin(0)]
        """Emiter i jego właściwości"""

        self.D = []
        """Kontener zawierający współrzędne detektorów"""

        self.iterations = np.arange(0, 180, self.alfa)
        """Liczba kroków podczas tworzenia sinogramu"""

        self.createDetectorsCoordinates()
        print(self.D)

    def createDetectorsCoordinates(self):
        """Metoda inicjalizująca współrzędne detektorów"""
        for d in range(self.n):
            self.D.append((0, 0))
        list(enumerate(D))

    def createSinogram(self):
        """Metoda tworząca sinogram"""
        for angle in self.iterations:
            for detector in self.D:
                self.D[detector][0] = self.r * math.cos(angle + math.pi - self.l / 2 + self.d * self.l / (self.n - 1))
                self.D[detector][1] = self.r * math.sin(angle + math.pi - self.l / 2 + self.d * self.l / (self.n - 1))

                deltaX = self.E[0] - self.D[detector][0]
                deltaY = self.E[1] - self.D[detector][1]

                if deltaX < deltaY:
                    """Zmiana Driving Axis"""
                    tmp = self.E[0]
                    self.E[0] = self.E[1]
                    self.E[1] = tmp

                    tmp = self.D[detector][0]
                    self.D[detector][0] = self.D[detector][1]
                    self.D[detector][1] = tmp
                j = self.E[1]
                slope = deltaY - deltaX
                if deltaX >= 0:
                    if deltaY >= 0:
                        # if deltaX >= deltaY:
                        #     print("good")
                        # else:
                        print("bez zmian")
                    else:
                        print("zmiana znaku deltaX przy odejmowaniu od epsilon")
                else:
                    if deltaY >= 0:
                        print("")
                    else:
                        print("zmiana znaku deltaX oraz deltaY przy działaniu z epsilon")
                for i in range(startPoint[0], endPoint[0] - 1):
                    # illuminate(i,j)
                    print(i, j, "    ", slope)
                    if slope >= 0:
                        j += 1
                        slope -= deltaX
                        print(i, j, "    ", slope)
                    slope += deltaY
                    i += 1

"""Całkowitoliczbowy algorytm Bresenhama"""

