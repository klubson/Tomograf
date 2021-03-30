import numpy as np
import matplotlib.pyplot as plt
import time
import math
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtGui import *


class Algorithm:
    alfa = 0
    """Krok dla układów emiter/detektor"""
    n = 0
    """Liczba detektorów"""
    l = 0
    """Rozwartość kątowa detektorów"""
    r = 0
    """Promień okręgu wpisanego w obrazek"""
    S = [0, 0]
    """Współrzędne środka obrazka"""
    E = []
    """Inicjalizacja tablicy współrzędnych emiterów"""
    Emitter = np.array
    """Inicjalizacja tablicy współrzędnych emiterów"""
    D = []
    """Inicjalizacja tablicy współrzędnych detektorów"""
    Detectors = np.array
    """Inicjalizacja tablicy współrzędnych emiterów"""
    image = QImage
    """Zmienna przechowująca wczytany z pliku obrazek"""
    iterations = np.arange
    """Inicjalizacja tablicy przechowującej wartości kątów, po których iterują funkcje"""
    sinogram = []
    """Inicjalizacja tablicy przechowującej sinogram"""
    greyPicture = []
    """Inicjalizacja tablicy obrazka w skali szarości"""
    square = None
    """Inicjalizacja tablicy przechowującej obraz końcowy"""

    def __init__(self, picture, deltaAlfa, detectors, range):
        """Inicjalizacja klasy wykonującej obliczenia"""

        self.alfa = 180 / deltaAlfa
        self.n = detectors
        self.l = math.radians(range)
        self.image = picture.toImage()
        self.r = self.image.width() / 2
        self.S = [self.image.width() / 2, self.image.height() / 2]
        self.E = []
        self.D = []
        self.iterations = np.arange(0, 180, self.alfa)

        self.createDetectorsCoordinates()
        self.makePictureGray()
        self.sinogram = self.createSinogram()
        self.createOutput()

    def createDetectorsCoordinates(self):
        """Metoda inicjalizująca współrzędne detektorów i emiterów"""
        for d in range(self.n):
            self.D.append([0, 0])
            self.E.append([0, 0])

    def updateDetectorsCoordinates(self, angle):
        """Metoda aktualizująca współrzędne detektorów podczas iteracji"""
        for counter in range(len(self.D)):
            self.D[counter][0] = self.r * math.cos(angle + math.pi - self.l / 2 + counter * self.l / (self.n - 1)) + self.S[0]
            self.D[counter][1] = self.r * math.sin(angle + math.pi - self.l / 2 + counter * self.l / (self.n - 1)) + self.S[1]
            self.E[counter][0] = self.r * math.cos(angle - self.l / 2 + counter * self.l / (self.n - 1)) + self.S[0]
            self.E[counter][1] = self.r * math.sin(angle - self.l / 2 + counter * self.l / (self.n - 1)) + self.S[1]
        self.Detectors = np.array(self.D)
        self.E.reverse()
        self.Emitter = np.array(self.E)

    def makePictureGray(self):
        """Metoda tworząca odpowiednik obrazka w skali szarości"""
        self.greyPicture = np.zeros((self.image.width(), self.image.height()), dtype=int)
        for x in range(self.image.width()):
            for y in range(self.image.height()):
                self.greyPicture[x][y] = qGray(self.image.pixel(x, y))
    """
    N-D Bresenham line algorithm
    """
    import numpy as np
    def bresenhamline_nslope(self, slope):
        """
        Normalize slope for Bresenham's line algorithm.

        >>> s = np.array([[-2, -2, -2, 0]])
        >>> _bresenhamline_nslope(s)
        array([[-1., -1., -1.,  0.]])

        >>> s = np.array([[0, 0, 0, 0]])
        >>> _bresenhamline_nslope(s)
        array([[ 0.,  0.,  0.,  0.]])

        >>> s = np.array([[0, 0, 9, 0]])
        >>> _bresenhamline_nslope(s)
        array([[ 0.,  0.,  1.,  0.]])
        """
        scale = np.amax(np.abs(slope), axis=1).reshape(-1, 1)
        zeroslope = (scale == 0).all(1)
        scale[zeroslope] = np.ones(1)
        normalizedslope = np.array(slope, dtype=np.double) / scale
        normalizedslope[zeroslope] = np.zeros(slope[0].shape)
        return normalizedslope

    def bresenhamlines(self, start, end, max_iter):
        """
        Returns npts lines of length max_iter each. (npts x max_iter x dimension)

        >>> s = np.array([[3, 1, 9, 0],[0, 0, 3, 0]])
        >>> _bresenhamlines(s, np.zeros(s.shape[1]), max_iter=-1)
        array([[[ 3,  1,  8,  0],
                [ 2,  1,  7,  0],
                [ 2,  1,  6,  0],
                [ 2,  1,  5,  0],
                [ 1,  0,  4,  0],
                [ 1,  0,  3,  0],
                [ 1,  0,  2,  0],
                [ 0,  0,  1,  0],
                [ 0,  0,  0,  0]],
        <BLANKLINE>
               [[ 0,  0,  2,  0],
                [ 0,  0,  1,  0],
                [ 0,  0,  0,  0],
                [ 0,  0, -1,  0],
                [ 0,  0, -2,  0],
                [ 0,  0, -3,  0],
                [ 0,  0, -4,  0],
                [ 0,  0, -5,  0],
                [ 0,  0, -6,  0]]])
        """
        if max_iter == -1:
            max_iter = np.amax(np.amax(np.abs(end - start), axis=1))
        npts, dim = start.shape
        nslope = self.bresenhamline_nslope(end - start)

        # steps to iterate on
        stepseq = np.arange(1, max_iter + 1)
        stepmat = np.tile(stepseq, (dim, 1)).T

        # some hacks for broadcasting properly
        bline = start[:, np.newaxis, :] + nslope[:, np.newaxis, :] * stepmat

        # Approximate to nearest int
        return np.array(np.rint(bline), dtype=start.dtype)

    def bresenhamline(self, start, end, max_iter=5):
        """
        Returns a list of points from (start, end] by ray tracing a line b/w the
        points.
        Parameters:
            start: An array of start points (number of points x dimension)
            end:   An end points (1 x dimension)
                or An array of end point corresponding to each start point
                    (number of points x dimension)
            max_iter: Max points to traverse. if -1, maximum number of required
                      points are traversed

        Returns:
            linevox (n x dimension) A cumulative array of all points traversed by
            all the lines so far.

        >>> s = np.array([[3, 1, 9, 0],[0, 0, 3, 0]])
        >>> bresenhamline(s, np.zeros(s.shape[1]), max_iter=-1)
        array([[ 3,  1,  8,  0],
               [ 2,  1,  7,  0],
               [ 2,  1,  6,  0],
               [ 2,  1,  5,  0],
               [ 1,  0,  4,  0],
               [ 1,  0,  3,  0],
               [ 1,  0,  2,  0],
               [ 0,  0,  1,  0],
               [ 0,  0,  0,  0],
               [ 0,  0,  2,  0],
               [ 0,  0,  1,  0],
               [ 0,  0,  0,  0],
               [ 0,  0, -1,  0],
               [ 0,  0, -2,  0],
               [ 0,  0, -3,  0],
               [ 0,  0, -4,  0],
               [ 0,  0, -5,  0],
               [ 0,  0, -6,  0]])
        """
        # Return the points as a single array
        return self.bresenhamlines(start, end, max_iter).reshape(-1, start.shape[-1])

    def createSinogram(self):
        """Metoda tworząca sinogram"""

        plt.ion()
        sin = np.zeros((len(self.iterations), len(self.D)))
        plt.figure("Sinogram")
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(100, 200, 640, 545)
        self.updatePlot(sin)
        for angleIndex, angle in enumerate(self.iterations):
            self.updateDetectorsCoordinates(math.radians(angle))
            print("Tworzenie sinogramu. Postęp: ", "%.2f" % (angleIndex / len(self.iterations) * 100), "%")
            for emitter in range(len(self.Emitter)):
                dist = math.sqrt(math.pow(self.Emitter[emitter][0]-self.Detectors[emitter][0], 2) + math.pow(self.Emitter[emitter][1]-self.Detectors[emitter][1], 2))
                if np.isnan(dist):
                    dist = 0.0
                dist = int(dist)
                pts = self.bresenhamline(np.array([self.Emitter[emitter]]), np.array([self.Detectors[emitter]]), dist)
                colorValue = 0.0
                for point in pts:
                    try:
                        pt_0 = int(point[0])
                        pt_1 = int(point[1])
                        colorValue += self.greyPicture[pt_0][pt_1]
                    except IndexError:
                        pass
                try:
                    sin[angleIndex][emitter] = colorValue
                except ValueError:
                    sin[angleIndex][emitter] = 0.0
            if angleIndex % int((len(self.iterations) / 20)) == 0 or angleIndex == len(self.iterations) - 1:
                self.updatePlot(sin)
        print("Zakończono tworzenie sinogramu")
        return sin

    def makeSquare(self, radius):
        """Metoda inicjalizująca obraz wyjściowy"""
        self.square = np.zeros((int(radius), int(radius)))

    def createOutput(self):
        """Metoda tworząca obraz wyjściowy"""
        self.makeSquare(2*self.r)
        plt.ion()
        plt.figure("Obraz wyjściowy")
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(1200, 200, 640, 545)
        self.updatePlot(self.square)

        for angleIndex, angle in enumerate(self.iterations):
            self.newFigureCoordinates(math.radians(angle))
            print("Tworzenie obraz wyjściowego. Postęp: ", "%.2f" % (angleIndex / len(self.iterations) * 100), "%")
            for emitter in range(len(self.Emitter)):
                dist = math.sqrt(math.pow(self.Emitter[emitter][0] - self.Detectors[emitter][0], 2) + math.pow(self.Emitter[emitter][1] - self.Detectors[emitter][1], 2))
                # print(dist)
                if np.isnan(dist):
                    dist = 0.0
                dist = int(dist)
                pts = self.bresenhamline(np.array([self.Emitter[emitter]]), np.array([self.Detectors[emitter]]), dist)
                
                if dist == 0:
                    dist = 1
                
                colorValue = self.sinogram[angleIndex][emitter] / dist
                for point in pts:
                    try:
                        pt_0 = int(point[0])
                        pt_1 = int(point[1])
                        self.square[pt_1][pt_0] = (self.square[pt_1][pt_0]*emitter + colorValue) / (emitter+1)
                    except IndexError:
                        pass
            if angleIndex % int((len(self.iterations) / 20)) == 0 or angleIndex == len(self.iterations) - 1:
                self.updatePlot(self.square)
        print("Zakończono tworzenie obrazu wyjściowego")

    def newFigureCoordinates(self, angle):
        for counter in range(len(self.D)):
            self.D[counter][0] = self.r * math.cos(angle + math.pi - self.l / 2 + counter * self.l / (self.n - 1)) + self.r
            self.D[counter][1] = self.r * math.sin(angle + math.pi - self.l / 2 + counter * self.l / (self.n - 1)) + self.r
            self.E[counter][0] = self.r * math.cos(angle - self.l / 2 + counter * self.l / (self.n - 1)) + self.r
            self.E[counter][1] = self.r * math.sin(angle - self.l / 2 + counter * self.l / (self.n - 1)) + self.r
        self.Detectors = np.array(self.D)
        self.E.reverse()
        self.Emitter = np.array(self.E)

    def updatePlot(self, img):
        plt.imshow(img, cmap='gray')
        plt.draw()
        plt.pause(0.01)
