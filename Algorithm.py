import numpy as np
import math

startPoint = (0, 0)
endPoint = (5, 3)

"""Całkowitoliczbowy algorytm Bresenhama"""

"""krok dla układu emiter/detektor - od użytkownika"""
alfa = 30 / 360
"""liczba detektorów - od użytkownika"""
n = 5
"""Rozwartość/rozpiętość układu emiter/detektor - od użytkownika"""
l = 90 / 360
"""Promień okręgu wpisanego w obrazek - z wczytanego zdjęcia"""
r = 10
"""Środek obrazka - z wczytanego zdjęcia"""
S = (0, 0)
"""Emiter i jego właściwości"""
E = (r * math.cos(alfa), r * math.sin(alfa))
"""Kontener zawierający parametry detektorów"""
D = []
for d in range(n):
    a = (r * math.cos(alfa + math.pi - l / 2 + d * l / (n - 1)), r * math.sin(alfa + math.pi - l / 2 + d * l / (n - 1)))
    D.append(a)
print(D)
deltaX = endPoint[0] - startPoint[0]
deltaY = endPoint[1] - startPoint[1]
j = startPoint[1]
slope = deltaY - deltaX

for i in range(startPoint[0], endPoint[0] - 1):
    # illuminate(i,j)
    print(i, j, "    ", slope)
    if slope >= 0:
        j += 1
        slope -= deltaX
        print(i, j, "    ", slope)
    slope += deltaY
    i += 1
