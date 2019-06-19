def getRadius(left, top, right, bottom):
    radiusX = (right - left)//2
    radiusY = (bottom - top)//2
    mediumRadius = (radiusX + radiusY)//2

    return mediumRadius
