class Schiff:

    def __init__(self, id, name, Größe):
        self.id = id
        self.name = name
        self.Größe = Größe
        # the automatic "Status of Schiff" is not hit (True)
        self.Status = True
        self.Treffer = 0
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

    def getGröße(self):
        return self.Größe

    def setGröße(self, Größe):
        self.Größe = Größe

    def getStatus(self):
        return self.Status

    def setStatus(self, Status):
        self.Status = Status

    def getTreffer(self):
        return self.Treffer

    def setTreffer(self, Treffer):
        self.Treffer = Treffer

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def gotdirektTreffer(self):
        self.Treffer += 1
        # prüfen, ob die Anzahl der Schläge die Größe des Schiffes "beinhalten"
        if self.getTreffer() >= self.getGröße():
            # falls ja, dazu hinweisen, dass ein Schiff zerstört wurde
            self.Status = False

    def SchiffPlatzieren(self, platz):
        # Add platz to the end of the list
        self.position.append(platz)
