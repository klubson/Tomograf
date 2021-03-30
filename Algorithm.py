import numpy as np
import matplotlib.pyplot as plt
import time
import math
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtGui import *


class Algorithm:
    alfa = 0
    n = 0 # number of detectors
    l = 0 # range of detectors
    r = 0 # radius
    S = [0, 0] # picture's center's coordinates
    E = [] #emitters' coordinates
    Emitter = np.array
    D = []  #list of detectors
    Detectors = np.array
    image = QImage
    iterations = np.arange
    sinogram = []
    greyPicture = []
    square = None

    def __init__(self, picture, deltaAlfa, detectors, range):
        """Inicjalizacja klasy wykonującej obliczenia"""

        self.alfa = 180 / deltaAlfa
        """krok dla układu emiter/detektor - od użytkownika"""

        self.n = detectors
        """liczba detektorów - od użytkownika"""

        self.l = math.radians(range)
        """Rozwartość/rozpiętość układu emiter/detektor - od użytkownika"""

        self.image = picture.toImage()
        """Obraz pobrany z komputera"""

        self.r = self.image.width() / 2
        """Promień okręgu wpisanego w obrazek - z wczytanego zdjęcia"""

        self.S = [self.image.width() / 2, self.image.height() / 2]
        """Środek obrazka - z wczytanego zdjęcia"""
        print(self.S)

        self.E = []
        """Emiter i jego właściwości"""

        self.D = []
        """Kontener zawierający współrzędne detektorów"""

        self.iterations = np.arange(0, 180, self.alfa)
        """Liczba kroków podczas tworzenia sinogramu"""

        self.createDetectorsCoordinates()
        #print(self.D)
        #print(self.image)
        self.makePictureGray()
        #print(self.greyPicture)
        self.sinogram = self.createSinogram()
        #print(self.sinogram)
        self.createOutput()

    def heatmap2d(self, array):
        plt.imshow(array, cmap='Greys')
        plt.show()

    def createDetectorsCoordinates(self):
        """Metoda inicjalizująca współrzędne detektorów"""
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
        #print(self.Emitter)

    def makePictureGray(self):
        #print(type(self.image.width()))
        self.greyPicture = np.zeros((self.image.width(), self.image.height()), dtype=int)
        for x in range(self.image.width()):
            for y in range(self.image.height()):
                self.greyPicture[x][y] = qGray(self.image.pixel(x, y))
    """
    N-D Bresenham line algo
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
        sin = [ [0]*len(self.D) for i in range(len(self.iterations))]
        for angleIndex, angle in enumerate(self.iterations):
            self.updateDetectorsCoordinates(math.radians(angle))
            #print(angle)
            #print(self.r)
            #print(self.r * 2)
            print("%.2f" % (angleIndex / len(self.iterations) * 100), "%")
            for emitter in range(len(self.Emitter)):
                dist = math.sqrt(math.pow(self.Emitter[emitter][0]-self.Detectors[emitter][0], 2) + math.pow(self.Emitter[emitter][1]-self.Detectors[emitter][1], 2))
                #print(dist)
                if np.isnan(dist):
                    dist = 0.0
                dist = int(dist)
                pts = self.bresenhamline(np.array([self.Emitter[emitter]]), np.array([self.Detectors[emitter]]), dist)
                #print(pts)
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

            #pts = self.bresenhamline(self.Emitter, self.Detectors, 2 * self.r).reshape(len(self.D), int(2 * self.r), 2)
        #print(sin)
        return sin

    def makeSquare(self, radius):
        self.square = np.zeros((int(radius), int(radius)))


    def createOutput(self):
        self.makeSquare(2*self.r)
        for angleIndex, angle in enumerate(self.iterations):

            self.newFigureCoordinates(math.radians(angle))
            print("%.2f" % (angleIndex / len(self.iterations) * 100), "%")
            for emitter in range(len(self.Emitter)):
                dist = math.sqrt(math.pow(self.Emitter[emitter][0] - self.Detectors[emitter][0], 2) + math.pow(self.Emitter[emitter][1] - self.Detectors[emitter][1], 2))
                # print(dist)
                if np.isnan(dist):
                    dist = 0.0
                dist = int(dist)
                pts = self.bresenhamline(np.array([self.Emitter[emitter]]), np.array([self.Detectors[emitter]]), dist)

                colorValue = self.sinogram[angleIndex][emitter] / (2 * self.r)
                properColorValue = 0.0
                for point in pts:
                    try:
                        pt_0 = int(point[0])
                        pt_1 = int(point[1])
                        self.square[pt_0][pt_1] = (self.square[pt_0][pt_1]*emitter + colorValue) / (emitter+1)
                        # print(colorValue)
                    except IndexError:
                        pass
            """if properColorValue != self.sinogram[angleIndex][detectorIndex]:
                    for point in pts[detectorIndex]:
                        try:
                            pt_0 = point[0]
                            pt_1 = point[1]
                            self.square[pt_0][pt_1] = colorValue
                            # print(colorValue)
                        except IndexError:
                            pass"""
            """else:
                    for point in pts[detectorIndex]:
                        try:
                            pt_0 = point[0]
                            pt_1 = point[1]
                            self.square[pt_0][pt_1] += 1
                            # print(colorValue)
                        except IndexError:
                            pass"""


    def newFigureCoordinates(self, angle):
        for counter in range(len(self.D)):
            self.D[counter][0] = self.r * math.cos(angle + math.pi - self.l / 2 + counter * self.l / (self.n - 1)) + self.r
            self.D[counter][1] = self.r * math.sin(angle + math.pi - self.l / 2 + counter * self.l / (self.n - 1)) + self.r
            self.E[counter][0] = self.r * math.cos(angle - self.l / 2 + counter * self.l / (self.n - 1)) + self.r
            self.E[counter][1] = self.r * math.sin(angle - self.l / 2 + counter * self.l / (self.n - 1)) + self.r
        self.Detectors = np.array(self.D)
        self.E.reverse()
        self.Emitter = np.array(self.E)

