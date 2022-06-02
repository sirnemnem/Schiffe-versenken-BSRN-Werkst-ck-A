COLS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']



class Position:
    def __init__(self, x_cor, y_cor):
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.value = 'O'
        self.ref = '{}{}'.format(COLS[self.x_cor], self.y_cor+1)

    #Erstellung der getter und setter Methoden
    def getX_cor(self):
        return self.x_cor

    def setX_cor(self, x_cor):
        self.x_cor = x_cor

    def getY_cor(self):
        return self.y_cor

    def setY_cor(self, y_cor):
        self.y_cor = y_cor

    def getRef(self):
        return self.ref

    def setRef(self, ref):
        self.ref = ref

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value
