from classes.position import *


class Feld:

    def __init__(self, height=10, width=10):
        self.height = height
        self.width = width
        self.positions = dict()
        self.initFeld()

    #Erstellung der getter und setter Methoden
    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def getWidth(self):
        return self.width

    def setWidth(self, width):
        self.width = width

    def getPositions(self):
        return self.positions

    def setPositions(self, positions):
        self.positions = positions

    def initFeld(self):
        # Initialisierung des Feldes
        for x in range(self.width):
            for y in range(self.height):
                pos = Position(x, y)
                self.positions[pos.getRef()] = pos

    def getValueByRef(self, ref):
        pos = self.positions[ref]
        return pos.getValue()

    def setValueByRef(self, ref, value):
        self.positions[ref].setValue(value)

    def getValueByCor(self, x, y):
        ref = self.encodePosition(x, y)
        return self.getValueByRef(ref)

    def setValueByCor(self, x, y, value):
        ref = self.encodePosition(x, y)
        self.setValueByRef(ref, value)

    @staticmethod
    def encodePosition(xCor, yCor):
        # Zuweisung der Spielfeldkoordinaten
        # encodePosition(0,0) ==> 'A1'
        # encodePosition(0,1) ==> 'A2'
        return Position(xCor, yCor).getRef()

    @staticmethod
    def decodePosition(ref):
        col = ref[0]
        row = ref[1:]

        x = COLS.index(col.upper())
        y = int(row) - 1

        return (x, y)
