class Ship:

    def __init__(self, id, name, size):
        self.id = id
        self.name = name
        self.size = size
        # the automatic "state of ship" is not hit (True)
        self.state = True
        self.hits = 0
        # save positions to list
        self.position = list()

# make getter and setter methods (Zeile 14 - Zeile 48) um Zugriff in anderen Klassen zu haben
    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getSize(self):
        return self.size

    def setSize(self, size):
        self.size = size

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getHits(self):
        return self.hits

    def setHits(self, hits):
        self.hits = hits

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def gotDirectHit(self):
        self.hits += 1
        # prüfen, ob die Anzahl der Schläge die Größe des Schiffes "beinhalten"
        if self.getHits() >= self.getSize():
            # falls ja, dazu hinweisen, dass ein Schiff zerstört wurde
            self.state = False

    def placeShip(self, place):
        # Add place to the end of the list
        self.position.append(place)
