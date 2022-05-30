from typing import Set
from classes.field import Field
from classes.ship import Schiff
import random

# den Schiffe werden Namen (Values) "und IDen (Keys)" zugeördnet
SCHIFFSNAMEN = {6: 'F221 Hessen', 5: 'F264 Ludwigshafen am Rhein', 4: 'P6126 S76 Frettchen',
              3: 'M1098 Siegburg', 2: 'M1069 Homburg', 1: 'M1061 Rottweil'}


class Spieler:
    def __init__(self, name, numSchiffe=6):
        self.name = name
        self.Punktzahl = 0
        self.numSchiffe = numSchiffe
        self.schiffe = dict()
        self.field = Field()
        self.initSchiffe()

    # Setters and getters
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setPunktzahl(self, Punktzahl):
        self.Punktzahl = Punktzahl

    def getPunktzahl(self):
        return self.Punktzahl

    def getField(self):
        return self.field

    def setField(self, field):
        self.field = field

    def getSchiffe(self):
        return self.schiffe

    def setSchiffe(self, schiffe):
        self.schiffe = schiffe

    # diese Methode dient zur Initialierung von schiffe
    def initSchiffe(self):

        # die Schleife fängt "an der Stelle" 0 an und geht die "number of schiffe" durch
        for i in range(0, self.numSchiffe):
            # zu jedem Schiff wird eine schiffId "zugeordnet"
            schiffId = len(SCHIFFSNAMEN) - i
            # schiffName wird von dem dict "geholt" 
            schiffName = SCHIFFSNAMEN[schiffId]
            # wird den Wert von "schiffId" zugeordnet
            Größe = schiffId

            # falls die Größe kleiner als 1 oder 1 ist, dann wird sie automatisch
            # die Größe 2 zugeordnet 
            if Größe <= 1:
                Größe = 2

            # schiffe ist dict
            # Schlüssel ist der Id des Schiffes und Wert ist der Schiff-Objekt selbst
            self.schiffe[schiffId] = Schiff(schiffId, schiffName, Größe)

    # diese Methode dient zur Inkremtierung des Punktzahls
    def incrementPunktzahl(self):
        self.setPunktzahl(self.getPunktzahl()+1)
    
    def UmgebungMarkieren(self, schiffPlatz):
        # diese Methode markiert alle Plätze im Feld, 
        # die ein Schiff umgeben als nicht verfügbar
        # und gibt die zurück
        
        plätze = set(schiffPlatz)
        field = set(self.getField().getPositions().keys())
        for platz in schiffPlatz:
            x, y = Field.decodePosition(platz)

            # rechts von einem Platz
            if Field.encodePosition(x+1, y) in field:
                plätze.add(Field.encodePosition(x+1, y))
            
            # Links
            if Field.encodePosition(x-1, y) in field:
                plätze.add(Field.encodePosition(x-1, y))

            # unter
            if Field.encodePosition(x, y+1) in field:
                plätze.add(Field.encodePosition(x, y+1))

            # oben
            if Field.encodePosition(x, y-1) in field:
                plätze.add(Field.encodePosition(x, y-1))

        return set(plätze)

    def SchiffePlatzierenAuto(self):

        # save the used positions in a set
        used = set()

        # save the keys of the "getPositions dictionary" "getField dictionary" to the set 
        field = set(self.getField().getPositions().keys())

        # die For-Schleife geht alle Schiffe (die 'values' in der dic) von CPU durch
        for schiff in self.schiffe.values():

            # possible starting positions are added to a list
            # starting position are all positions in a field without the used plätze
            options = list(field - used)

            # randomly pick a starting position from possible options
            pos = random.choice(options)

            # each schiff has a list of not possible starting plätze, (therefore)
            # create a set that contains the list of impossible starting points
            notPossible = set()

            # the initial status of each schiff is not platziert
            platziert = False

            # from a starting position it can go left ('l'), right ('r'), up ('u'), or down ('d')
            directions = set(['l', 'r', 'u', 'd'])

            # (convert the postion from text to x and y coordinates)
            # ! convert von Referenzen (bsp: A1) to X- und Y-Koordinate (bsp: 'A1' = (x=0, y=0))
            # (A1 => x=0, y=0)
            x, y = Field.decodePosition(pos)

            # Solange ein Schiff keine Position hat, wird die While-Schleife durchgeführt
            while not platziert:

                # adds possible plätze from starting point (if a schiff is not platziert 
                # next to the staring point) and saves it to a list
                möglichePlätze = list()

                # randomly pick a direction and remove it from directions list
                # a dirction will be randoml picked, because directions is a set() (set are not ordered)
                d = directions.pop()

                # if the chosen direction is right
                if d == 'r':
                    start = pos
                    end = Field.encodePosition(x + schiff.Größe - 1, y)
                    # if the field end does fit in the grid
                    if end in field:
                        möglichePlätze = getVonBis(start, end)

                # the same  logic for other directions
                elif d == 'l':
                    start = pos
                    end = Field.encodePosition(x - schiff.Größe + 1, y)
                    if end in field:
                        möglichePlätze = getVonBis(start, end)

                elif d == 'u':
                    start = pos
                    end = Field.encodePosition(x, y - schiff.Größe + 1)
                    if end in field:
                        möglichePlätze = getVonBis(start, end)

                elif d == 'd':
                    start = pos
                    end = Field.encodePosition(x, y + schiff.Größe - 1)
                    if end in field:
                        möglichePlätze = getVonBis(start, end)

                # if the algorithm found a possible platz for the schiff
                if len(möglichePlätze) > 0:
                    # if the platz contains a used position, ignore this "platz" and
                    # start over in other direction
                    if len(set(möglichePlätze) & used) > 0:
                        möglichePlätze.clear()
                    # if the possible plätze don't include used plätze
                    # then platz this schiff here
                    # and mark this platz and plätze around it as used too
                    else:
                        # platz the schiff here
                        for p in möglichePlätze:
                            #
                            self.getField().setValueByRef(p, schiff)

                        self.schiffe[schiff.id].setPosition(möglichePlätze)
                        # show me the result
                        # print('{} in {}'.format(schiff.id, möglichePlätze))

                        used = used.union(
                            self.UmgebungMarkieren(möglichePlätze))
                        # mark the schiff as platziert
                        platziert = True
                # if the algorithm didn't find any platz for the schiff

                # if all direction are tried
                # add this starting position
                # then pick another random position
                if len(directions) == 0 and not platziert:
                    # it is impossible to platz this schiff in the
                    # field starting from this pos
                    # so add pos to (the set of) not possible starting points
                    notPossible.add(pos)

                    # pick a new starting point
                    options = list(set(options) - notPossible)
                    pos = random.choice(options)

                    # re-assign directions for the new starting point
                    directions = set(['l', 'r', 'u', 'd'])
                    x, y = Field.decodePosition(pos)

                if platziert:
                    break

# Klasse Computer "irbt" von Klasse Spieler, da Klasse Computer die "Eigenschaften/Methoden " von Klasse
# Spieler irbt (as well as Attribute/andere Methoden (Zeilen 72, 90, 98, 115))
class Computer(Spieler):

    # ... und die Anzahl von Schiffen initializieren (numSchiffe=6)
    def __init__(self, name='CPU', numSchiffe=6):
        super().__init__(name, numSchiffe)
        self.letzterErfolg = ''
        self.played = set()
        self.memory = dict()

    def Schießen(self, plätzeListe):

        # options beinhaltet alle Plätze im Feld außer die benuztze Plätze
        options = list(set(plätzeListe) - self.played)
        # Mithilfe von "random-module" und choice-Methode wird ein
        # zufälliges Element von der "Liste" 'Options' in den "Wert" 'choice' gespeichert
        choice = random.choice(options)

        # prüfen ob etwas im Gedächtniss des Coputer liegt
        if len(self.memory) > 0:
            # memrory ist ein Dict
            # der Schlüssel ist die Referenz eines Platz im Feld, wo letzlich 
            # Cpu eine Schif getroffen hatte

            # Der Wert ist eine List, die nächste mögliche Platzrefenze in der Umgebung beihaltet
            # zum Beispiel:
            # Hätte der Cpu ein Schiff im Platz B2
            # wäre memory so:
            #       {'B2': ['B1','B3','A2','C2']}

            # falls ja, dann die Auswahl ersetzten
            key = random.choice(list(self.memory.keys()))
            
            choice = self.memory[key].pop()


            if len(self.memory[key]) == 0:
                self.memory.pop(key, 'None')

        self.played.add(choice)

        return choice

    def Erfolg(self, ref):
        # cpu wird mit dieser Methode hingewiesen, dass sein Wurf erflogreich war,
        # sodass, er sich an diesem Punk errinert, und im Memory die Refrenz als Schlüssel und 
        # und Die Referenzen der umgebenden Plätze als Wert speichert
        self.letzterErfolg = ref

        next = self.UmgebungMarkieren([ref])

        self.memory[ref] = set(next - self.played)

    def UmgebungMarkieren(self, schiffPlatz):
        # diese Methode markiert alle Plätze im Feld, 
        # die ein Schiff umgeben als nicht verfügbar
        # und gibt die zurück
        
        plätze = set(schiffPlatz)
        field = set(self.getField().getPositions().keys())
        for platz in schiffPlatz:
            x, y = Field.decodePosition(platz)

            # rechts von einem Platz
            if Field.encodePosition(x+1, y) in field:
                plätze.add(Field.encodePosition(x+1, y))
            
            # Links
            if Field.encodePosition(x-1, y) in field:
                plätze.add(Field.encodePosition(x-1, y))

            # unter
            if Field.encodePosition(x, y+1) in field:
                plätze.add(Field.encodePosition(x, y+1))

            # oben
            if Field.encodePosition(x, y-1) in field:
                plätze.add(Field.encodePosition(x, y-1))

        return set(plätze)

    def SchiffePlatzieren(self):

        # save the used positions in a set
        used = set()

        # save the keys of the "getPositions dictionary" "getField dictionary" to the set 
        field = set(self.getField().getPositions().keys())

        # die For-Schleife geht alle Schiffe (die 'values' in der dic) von CPU durch
        for schiff in self.schiffe.values():

            # possible starting positions are added to a list
            # starting position are all positions in a field without the used plätze
            options = list(field - used)

            # randomly pick a starting position from possible options
            pos = random.choice(options)

            # each schiff has a list of not possible starting plätze, (therefore)
            # create a set that contains the list of impossible starting points
            notPossible = set()

            # the initial status of each schiff is not platziert
            platziert = False

            # from a starting position it can go left ('l'), right ('r'), up ('u'), or down ('d')
            directions = set(['l', 'r', 'u', 'd'])

            # (convert the postion from text to x and y coordinates)
            # ! convert von Referenzen (bsp: A1) to X- und Y-Koordinate (bsp: 'A1' = (x=0, y=0))
            # (A1 => x=0, y=0)
            x, y = Field.decodePosition(pos)

            # Solange ein Schiff keine Position hat, wird die While-Schleife durchgeführt
            while not platziert:

                # adds possible plätze from starting point (if a schiff is not platziert 
                # next to the staring point) and saves it to a list
                möglichePlätze = list()

                # randomly pick a direction and remove it from directions list
                # a dirction will be randoml picked, because directions is a set() (set are not ordered)
                d = directions.pop()

                # if the chosen direction is right
                if d == 'r':
                    start = pos
                    end = Field.encodePosition(x + schiff.Größe - 1, y)
                    # if the field end does fit in the grid
                    if end in field:
                        möglichePlätze = getVonBis(start, end)

                # the same  logic for other directions
                elif d == 'l':
                    start = pos
                    end = Field.encodePosition(x - schiff.Größe + 1, y)
                    if end in field:
                        möglichePlätze = getVonBis(start, end)

                elif d == 'u':
                    start = pos
                    end = Field.encodePosition(x, y - schiff.Größe + 1)
                    if end in field:
                        möglichePlätze = getVonBis(start, end)

                elif d == 'd':
                    start = pos
                    end = Field.encodePosition(x, y + schiff.Größe - 1)
                    if end in field:
                        möglichePlätze = getVonBis(start, end)

                # if the algorithm found a possible platz for the schiff
                if len(möglichePlätze) > 0:
                    # if the platz contains a used position, ignore this "platz" and
                    # start over in other direction
                    if len(set(möglichePlätze) & used) > 0:
                        möglichePlätze.clear()
                    # if the possible plätze don't include used plätze
                    # then platz this schiff here
                    # and mark this platz and plätze around it as used too
                    else:
                        # platz the schiff here
                        for p in möglichePlätze:
                            #
                            self.getField().setValueByRef(p, schiff)

                        self.schiffe[schiff.id].setPosition(möglichePlätze)
                        # show me the result
                        # print('{} in {}'.format(schiff.id, möglichePlätze))

                        used = used.union(
                            self.UmgebungMarkieren(möglichePlätze))
                        # mark the schiff as platziert
                        platziert = True
                # if the algorithm didn't find any platz for the schiff

                # if all direction are tried
                # add this starting position
                # then pick another random position
                if len(directions) == 0 and not platziert:
                    # it is impossible to platz this schiff in the
                    # field starting from this pos
                    # so add pos to (the set of) not possible starting points
                    notPossible.add(pos)

                    # pick a new starting point
                    options = list(set(options) - notPossible)
                    pos = random.choice(options)

                    # re-assign directions for the new starting point
                    directions = set(['l', 'r', 'u', 'd'])
                    x, y = Field.decodePosition(pos)

                if platziert:
                    break

# diese Methode gibt alle Plätze in einem Feld zwischen start und Ende
# zB: getVonBis('A1', 'A6') ==> ['A1','A2','A3','A4','A5','A6']
def getVonBis(start, end):

    start_x, start_y = Field.decodePosition(start)
    end_x, end_y = Field.decodePosition(end)

    # !! den Resultat in einer Liste speichern
    result = list()

    # Falls Start und Ende auf dem selben Spalte stehn
    if start_x == end_x:
        x = start_x
        # dafür sorgen, dass Start kleiner als End
        if start_y > end_y:
            tmp = start_y
            start_y = end_y
            end_y = tmp
        # von Start bis Ende inklusive durlaufen
        # Alle Punkte (x,y) in Referenz abbilden: (0,0) = 'A1'
        for y in range(start_y, end_y + 1):
            ref = Field.encodePosition(x, y)
            result.append(ref)

    # Falls Start und Ende auf derselben Zeile liegen
    elif start_y == end_y:
        y = start_y
        if start_x > end_x:
            tmp = start_x
            start_x = end_x
            end_x = tmp
        for x in range(start_x, end_x + 1):
            ref = Field.encodePosition(x, y)
            result.append(ref)

    return result
