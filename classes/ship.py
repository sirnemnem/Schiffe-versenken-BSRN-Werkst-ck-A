class Schiff:

    def __init__(self, id, name, Größe):
        self.id = id
        self.name = name
        self.Größe = Größe
        # Default "Status des Schiffes" ist nicht getroffen (true)
        self.Status = True
        self.Treffer = 0
        # Positionen speichern in list()
        self.position = list()

# getter and setter Methoden erstellen (Zeile 14 - Zeile 48) um Zugriff in anderen Klassen zu haben
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
        # überprüfen, ob die Anzahl der Treffer mehr als die Größe des Schiffes sind
        if self.getTreffer() >= self.getGröße():
            # Wenn dies zutrifft User darauf hinweisen, dass ein Schiff zerstört wurde
            self.Status = False

    def SchiffPlatzieren(self, platz):
        # Platz zum Ende der Liste hinzufügen
        self.position.append(platz)
