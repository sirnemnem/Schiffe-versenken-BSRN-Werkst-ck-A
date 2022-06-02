from typing import Set
from classes.field import Field
from classes.ship import Schiff
import random

# Schiffe werden Namen (Values) und dazugehörigen IDen (Keys) zugeordnet
SCHIFFSNAMEN = {6: 'K-573 Новосибирска', 5: 'B-261 Новорусијска', 4: 'K-139 Београдска',
              3: '610 Настојчивија', 2: 'K-154 Тигар', 1: 'K-461 Вук'}


class Spieler:
    def __init__(self, name, numSchiffe=6):
        self.name = name
        self.Punktzahl = 0
        self.numSchiffe = numSchiffe
        self.schiffe = dict()
        self.field = Field()
        self.initSchiffe()
    
    # Erzeugung der Getter/ Setter Methoden
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

    # Methode dient zur Intitialisierung der Schiffe
    def initSchiffe(self):

        # Schleife fängt bei 0 an und geht die numver von Schiffe durch
        for i in range(0, self.numSchiffe):
            # jedes Schiff bekommt eine SchiffId zugeteilt
            schiffId = len(SCHIFFSNAMEN) - i
            # SchiffName wird von dem dict geholt
            schiffName = SCHIFFSNAMEN[schiffId]
            # wird den Wert von "schiffId" zugeordnet
            Größe = schiffId

            # sofern die Größe kleiner 1 ist, wird sie automatisch der Größe 2 zugeordnet
            if Größe <= 1:
                Größe = 2

            # dict ist Schiffe 
            # Schlüssel ist die Id des Schiffes und Wert ist das Schiff-Objekt selbst
            # Schiffe sind mit der Id eindeutig
            self.schiffe[schiffId] = Schiff(schiffId, schiffName, Größe)

    # Methode zur Implementierung der Punktzahl
    def incrementPunktzahl(self):
        self.setPunktzahl(self.getPunktzahl()+1)
    
    def UmgebungMarkieren(self, schiffPlatz):
        # Methode markiert alle Plätze im Feld, die ein Schiff belegt als nicht verfügbar und gibt diese zurück
        
        plätze = set(schiffPlatz)
        field = set(self.getField().getPositions().keys())
        for platz in schiffPlatz:
            x, y = Field.decodePosition(platz)
            
            # Links von einem Platz
            if Field.encodePosition(x-1, y) in field:
                plätze.add(Field.encodePosition(x-1, y))
            
            # Rechts 
            if Field.encodePosition(x+1, y) in field:
                plätze.add(Field.encodePosition(x+1, y))
            
            # Oben
            if Field.encodePosition(x, y-1) in field:
                plätze.add(Field.encodePosition(x, y-1))
            # Unten
            if Field.encodePosition(x, y+1) in field:
                plätze.add(Field.encodePosition(x, y+1))

            

        return set(plätze)

    def SchiffePlatzierenAuto(self):

        # save the used positions in a set
        # speichert die benutzten postioioneneen in einem set 
        used = set()

        # save the keys of the "getPositions dictionary" "getField dictionary" to the set 
        #SIchert den Schlüssel von dem "getPositions dictionary" "getField dictionary" in dem set
        field = set(self.getField().getPositions().keys())

        # For-Schleife geht jeden Schiff durch (die 'values' in der dicn) von CPU  
        for schiff in self.schiffe.values():

            # mögliche starting postition wurden hinzugefügt zu der Liste
            # die Start position sind alle Positionen in dem Feld ohne die benutzten Fäldern 
            options = list(field - used)

            # randomly pick a starting position from possible options
            # zufällige start position von den gegebenen Optionen 
            pos = random.choice(options)

            # each schiff has a list of not possible starting plätze, (therefore)
            # jeder Schiff hat eine Liste für nicht mögliche starting postitionen, ()
            # create a set that contains the list of impossible starting points
            # erstellen eine set die beinhaltet eine Liste für alle mögliche starting positionen
            notPossible = set()

            # the initial status of each schiff is not platziert
            # initial status für jedes Schiff das nicht plaziert ist 
            platziert = False

            # from a starting position it can go left ('l'), right ('r'), up ('u'), or down ('d')
            # von der Startpostition kann es rechts ('r'), links ('l'), hoch ('u') oder runter ('d')
            directions = set(['l', 'r', 'u', 'd'])

            # (convert the postion from text to x and y coordinates)
            # (converntiert die Posttion von einen text zu einem coordinate)
            # ! convert von Referenzen (bsp: A1) to X- und Y-Koordinate (bsp: 'A1' = (x=0, y=0))
            # ! conventiert von Referenze (Beispiel: D1) zu X- und Y-Koordinate (Beispiel: 'D1' = (x=0; y=0))
            # (A1 => x=0, y=0)
            # (D1 => x=0, y=0)
            x, y = Field.decodePosition(pos)

            # Solange ein Schiff keine Position hat, wird die While-Schleife durchgeführt
            # Solange ein Schiff keine besitztende Postion hat, wird die While-Schleife ausgeführt
            while not platziert:

                # adds possible plätze from starting point (if a schiff is not platziert
                # next to the staring point) and saves it to a list
                # fügt mögliche plätze von Starting point hinzu (Wenn ein Schiff nicht plaziert konnte wurden geht es zu dem nächsten starting point)
                # und sichert es in eine Liste 
                möglichePlätze = list()

                # randomly pick a direction and remove it from directions list
                # a dirction will be randoml picked, because directions is a set() (set are not ordered)
                # wählt zufällig eine Richtung aus und löscht die von der directions list
                # a direction wird zufällig gewählt, weil die directions is a set() (set sind nicht geordnet) 
                d = directions.pop()

                # if the chosen direction is right
                # wenn die ausgewählte direction rechts ist
                if d == 'r':
                    start = pos
                    end = Field.encodePosition(x + schiff.Größe - 1, y)
                    # if the field end does fit in the grid
                    # wenn das Feld ende nicht ein das Grid passt 
                    if end in field:
                        möglichePlätze = getVonBis(start, end)

                # the same  logic for other directions
                # gehe logik für die anderen richtungen 
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
                # wenn der algroith ein geeigneten Platz finden für das Schiff wird das ausgeführt 
                if len(möglichePlätze) > 0:
                    # if the platz contains a used position, ignore this "platz" and
                    # start over in other direction
                    # wenn des Platz eine benutzets ist, wird dies ignoriert als "platz" und dann startet es in eine ander richtung
                    if len(set(möglichePlätze) & used) > 0:
                        möglichePlätze.clear()
                    # if the possible plätze don't include used plätze
                    # then platz this schiff here
                    # and mark this platz and plätze around it as used too
                    # wenn die ausgewählte Position nicht benutzt ist
                    # wird das Schiff das Plaziert
                    # und die postition wird als und die positionen darum (beniutzten postitionenen) werden las vergeben markiert
                    else:
                        # platz the schiff here
                        # schiff wird auf der position plaziert 
                        for p in möglichePlätze:
                            #
                            self.getField().setValueByRef(p, schiff)

                        self.schiffe[schiff.id].setPosition(möglichePlätze)
                        # show me the result
                        # print('{} in {}'.format(schiff.id, möglichePlätze))
                        # resultat wird präsenteirt
                        # print('{} in {}'.format(schiff.id, möglichePlätze))

                        used = used.union(
                            self.UmgebungMarkieren(möglichePlätze))
                        # mark the schiff as platziert
                        # markieren die schiffe als plaziert 
                        platziert = True
                # if the algorithm didn't find any platz for the schiff
                # wemm das algroithm kein platz findet für das Schiff 

                # if all direction are tried
                # add this starting position
                # then pick another random position
                # wenn alle directionenen versucht wurden sind 
                # wird die startpostion hinzugefügt
                # dann wird eine neue Sartpostion ausgewählt 
                if len(directions) == 0 and not platziert:
                    # it is impossible to platz this schiff in the
                    # field starting from this pos
                    # so add pos to (the set of) not possible starting points
                    # wenn es unmöglich ist ein platz für ein Shciff zu finden
                    #startet das feld von der Position
                    # und fügt pos zu (set of) nicht startbate positionen 
                    notPossible.add(pos)

                    # pick a new starting point
                    # wählt eine neue start position uas 
                    options = list(set(options) - notPossible)
                    pos = random.choice(options)

                    # re-assign directions for the new starting point
                    # neu zugewisene richtung von der neuen start position 
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
