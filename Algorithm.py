import numpy as np
import math
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage

class Algorithm:
    alfa = 0
    n = 0 # number of detectors
    l = 0 # range of detectors
    r = 0 # radius
    S = [0, 0] # picture's center's coordinates
    E = [0, 0] #emitter's coordinates
    D = [] #list of detectors
    image = QImage
    iterations = np.arange

    def __init__(self, picture, deltaAlfa, detectors, range):
        """Inicjalizacja klasy wykonującej obliczenia"""

        self.alfa = math.radians(deltaAlfa)
        """krok dla układu emiter/detektor - od użytkownika"""

        self.n = detectors
        """liczba detektorów - od użytkownika"""

        self.l = math.radians(range/(self.n - 1))
        """Rozwartość/rozpiętość układu emiter/detektor - od użytkownika"""

        self.image = picture.toImage()
        """Obraz pobrany z komputera"""

        self.r = self.image.width() / 2
        """Promień okręgu wpisanego w obrazek - z wczytanego zdjęcia"""

        self.S = [self.image.width() / 2, self.image.height() / 2]
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
            self.D.append([0, 0])

    def updateDetectorsCoordinates(self, angle):
        """Metoda aktualizująca współrzędne detektorów podczas iteracji"""
        for detector in self.D:
            self.D[detector][0] = self.r * math.cos(angle + math.pi - self.l / 2 + counter * self.l / (self.n - 1))
            self.D[detector][1] = self.r * math.sin(angle + math.pi - self.l / 2 + counter * self.l / (self.n - 1))

    def get_points(startPoint, endPoint):
        """Algorytm Bresenhama"""
        x1, y1 = startPoint
        x2, y2 = endPoint
        dx = x2 - x1
        dy = y2 - y1

        is_steep = abs(dx) - abs(dy)
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        dx = x2 - x1
        dy = y2 - y1

        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        if swapped:
            points.reverse()
        return points
    def createSinogram(self):
        """Metoda tworząca sinogram"""
        sinogram = [ [0]*len(self.D) for i in range(len(self.iterations))]
        for angleIndex, angle in enumerate(self.iterations):
            self.updateDetectorsCoordinates(angle)
            for detectorIndex, detector in enumerate(self.D):
                pts = self.get_points(self.E, detector)
                colorValue = 0.0
                for point in pts:
                    colorValue += qGray(self.image.pixel(point[0], point[1]))
                sinogram[angleIndex][detectorIndex] = colorValue

        return sinogram
