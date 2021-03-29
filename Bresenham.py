import math

def get_points(self, start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    is_steep = abs(dx) - abs(dy) < 0
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    m = 1024

    dx = x2 - x1
    dy = y2 - y1

    mdx = math.floor(m*(x2 - x1))
    mdy = math.floor(m*(y2 - y1))

    i1 = math.floor(x1)
    i2 = math.floor(x2)
    y = math.floor(y1)

    error = math.floor(-m * (dx * (1-y1) - dy * (1-x1)))
    error = -error if error > 0 else error

    ystep = 1 if y1 < y2 else -1

    points = []
    for x in range(i1, i2+1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error += abs(mdy)
        if error > 0:
            y += ystep
            error -= mdx

    if swapped:
        points.reverse()
    return points
