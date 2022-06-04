from typing import Set
from classes.feld import Feld
from classes.schiff import Schiff
import random

# Schiffe werden Namen (Values) und dazugehörigen IDen (Keys) zugeordnet
SCHIFFSNAMEN = {6: 'K-573 Новосибирска', 5: 'B-261 Новорусијска', 4: 'K-139 Београдска',
              3: 'DD-610 Настојчивија', 2: 'K-154 Тигар', 1: 'K-461 Вук'}


class Spieler:
    def __init__(self, name, numSchiffe=6):
        self.name = name
        self.Punktzahl = 0
        self.numSchiffe = numSchiffe
        self.schiffe = dict()
        self.feld = Feld()
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

    def getFeld(self):
        return self.feld

    def setFeld(self, feld):
        self.feld = feld

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
        feld = set(self.getFeld().getPositions().keys())
        for platz in schiffPlatz:
            x, y = Feld.decodePosition(platz)
            
            # Links von einer Position
            if Feld.encodePosition(x-1, y) in feld:
                plätze.add(Feld.encodePosition(x-1, y))
            
            # Rechts 
            if Feld.encodePosition(x+1, y) in feld:
                plätze.add(Feld.encodePosition(x+1, y))
            
            # Drüber
            if Feld.encodePosition(x, y-1) in feld:
                plätze.add(Feld.encodePosition(x, y-1))
            # Drunter
            if Feld.encodePosition(x, y+1) in feld:
                plätze.add(Feld.encodePosition(x, y+1))

            

        return set(plätze)

    def SchiffePlatzierenAuto(self):

        # speichert die benutzten Positionen in einem set 
        used = set()

        # sichert den Schlüssel von dem "getPositions dictionary" "getFeld dictionary" in dem set
        feld = set(self.getFeld().getPositions().keys())

        # For-Schleife geht jedes Schiff durch (die 'values' in der dicn) von CPU  
        for schiff in self.schiffe.values():

            # mögliche Start-Position wurde hinzugefügt zu der Liste
            # die Start-Position sind alle Positionen in dem Feld ohne die benutzten Felder
            options = list(feld - used)

            # zufällige Start-Position von den gegebenen Optionen 
            pos = random.choice(options)

            # jedes Schiff hat eine Liste für nicht mögliche Start-Positionen
            # erstellen ein set, welches eine Liste beinhaltet für alle mögliche Start-Positionen
            notPossible = set()

            # Ausgangszustand für jedes Schiff, welches nicht plaziert wurde 
            platziert = False

            # von der Startpostition kann es rechts ('r'), links ('l'), hoch ('u') oder runter ('d')
            directions = set(['l', 'r', 'u', 'd'])

            # konvertiert die Position von einem Text zu einer Koordinate
            # ! konvertiert vom String (Beispiel: D1) zu X- und Y-Koordinate (bsp.: 'D1' = (x=0; y=0))
            # (A1 => x=0, y=0)
            # (D1 => x=0, y=0)
            x, y = Feld.decodePosition(pos)

            # Solange ein Schiff keine besetzte Postion hat, wird die While-Schleife ausgeführt
            while not platziert:

                # fügt mögliche Positionen für den Start-Punkt hinzu 
                # (Wenn ein Schiff nicht plaziert werden konnte, geht es zu dem nächsten Start-Punkt)
                # und sichert es in eine Liste 
                möglichePlätze = list()

                # wählt zufällig eine Richtung aus und löscht diese von der directions list
                # eine Richtung wird zufällig gewählt, weil die directions ein set() ist (set sind nicht geordnet) 
                d = directions.pop()

                # wenn die ausgewählte Richtung rechts ist
                if d == 'r':
                    start = pos
                    end = Feld.encodePosition(x + schiff.Größe - 1, y)

                    # wenn das Feld Ende nicht in das Feld passt 
                    if end in feld:
                        möglichePlätze = getVonBis(start, end)

                # die selbe Logik für die anderen Richtungen 
                elif d == 'l':
                    start = pos
                    end = Feld.encodePosition(x - schiff.Größe + 1, y)
                    if end in feld:
                        möglichePlätze = getVonBis(start, end)

                elif d == 'u':
                    start = pos
                    end = Feld.encodePosition(x, y - schiff.Größe + 1)
                    if end in feld:
                        möglichePlätze = getVonBis(start, end)

                elif d == 'd':
                    start = pos
                    end = Feld.encodePosition(x, y + schiff.Größe - 1)
                    if end in feld:
                        möglichePlätze = getVonBis(start, end)


                # wenn der Algorithmus einen geeigneten Platz findet für das Schiff
                if len(möglichePlätze) > 0:

                    # wenn der Platz schon belegt ist, wird dieser "Platz" ignoriert
                    # startet in eine andere Richtung
                    if len(set(möglichePlätze) & used) > 0:
                        möglichePlätze.clear()

                    # wenn die ausgewählte Position nicht benutzt ist
                    # wird das Schiff dort plaziert
                    # und die Position, und die Positionen um diesen Platz, (benutzten Positionen) werden als vergeben markiert
                    else:
                        # Schiff wird auf der Position plaziert 
                        for p in möglichePlätze:
                            #
                            self.getFeld().setValueByRef(p, schiff)

                        self.schiffe[schiff.id].setPosition(möglichePlätze)
                        # Resultat wird präsenteirt
                        # print('{} in {}'.format(schiff.id, möglichePlätze))

                        used = used.union(
                            self.UmgebungMarkieren(möglichePlätze))
                        # die Schiffe werden als plaziert markiert
                        platziert = True
                # wenn der Algorithmus Kein platz findet für das Schiff 

                # wenn alle Richtungen versucht wurden  
                # wird die Start-Postion hinzugefügt
                # daraufhin wird eine neue zufällige Start-Postion ausgewählt 
                if len(directions) == 0 and not platziert:
                    
                    # wenn es unmöglich ist ein Platz für ein Schiff zu finden
                    # startet das Feld von dieser Position
                    # und fügt pos zu (set of) nicht startbare Positionen 
                    notPossible.add(pos)

                    # wählt eine neue Start-Position aus 
                    options = list(set(options) - notPossible)
                    pos = random.choice(options)

                    # neu zugewiesene Richtung von der neuen Start-Position 
                    directions = set(['l', 'r', 'u', 'd'])
                    x, y = Feld.decodePosition(pos)

                if platziert:
                    break

# Computer Klasse "irbt" von der Spieler Klasse, da die Computer Klasse "Eigenschaften/Methoden " von den Spieler Klasse irbt
class Computer(Spieler):

    # die Anzahl von Schiffen werden initialisiert (numSchiffe=6) gesetzt
    def __init__(self, name='CPU', numSchiffe=6):
        super().__init__(name, numSchiffe)
        self.letzterErfolg = ''
        self.played = set()
        self.memory = dict()

    def Schießen(self, plätzeListe):

        # options beinhaltet alle nicht benutzten Plätze
        options = list(set(plätzeListe) - self.played)
        # "random-module" und choice-Methode erzeugen ein zufälliges Element der Liste "Options" welcher in den Wert "choice" gespeichert
        choice = random.choice(options)

        # checkt ob es im Speicher des Computers liegt
        if len(self.memory) > 0:
            # memory ist ein Dict, von welchem der Schlüssel die Referenz eines Platzes im Spielfeld ist,
            # wo der CPU ein Treffer erzielt hat 

            # Der Wert ist eine Liste, welche die in der Umgebung möglichen Platzrefenzen beinhaltet
            # Beispiel: 
            # hätte ein Schiff des CPU´s den Platz B2 wird es so gespeichert {'B2':['B1','B3','A2','C2']}

            # falls dies der Fall ist, dann wir die Auswahl ersetzt
            key = random.choice(list(self.memory.keys()))
            
            choice = self.memory[key].pop()


            if len(self.memory[key]) == 0:
                self.memory.pop(key, 'None')

        self.played.add(choice)

        return choice

    def Erfolg(self, ref):
        # die Methode weißt den CPU darauf hin, dass sein Schuss ein Treffer war, 
        # somit kann er diesen Punkt speichern und sich an diesem für den nächsten Schuss orientieren,
        # dies wird dann als Referenz Schlüssel der umgebenden Plätze als Wert gespeichert
        self.letzterErfolg = ref

        next = self.UmgebungMarkieren([ref])

        self.memory[ref] = set(next - self.played)

    def UmgebungMarkieren(self, schiffPlatz):
        # die Methode dient zur Markierung alle Felder die von einem Schiff besetzt sind und gibt diese zurück
        
        plätze = set(schiffPlatz)
        feld = set(self.getFeld().getPositions().keys())
        for platz in schiffPlatz:
            x, y = Feld.decodePosition(platz)

            # Rechts von einer Position
            if Feld.encodePosition(x+1, y) in feld:
                plätze.add(Feld.encodePosition(x+1, y))
            
            # Links
            if Feld.encodePosition(x-1, y) in feld:
                plätze.add(Feld.encodePosition(x-1, y))

            # Drunter
            if Feld.encodePosition(x, y+1) in feld:
                plätze.add(Feld.encodePosition(x, y+1))

            # Drüber
            if Feld.encodePosition(x, y-1) in feld:
                plätze.add(Feld.encodePosition(x, y-1))

        return set(plätze)

    def SchiffePlatzieren(self):

        # speichert die benutzten Positionen in einem set 
        used = set()

        # sichert den Schlüssel von dem "getPositions dictionary" "getFeld dictionary" in dem set
        feld = set(self.getFeld().getPositions().keys())

        # For-Schleife geht jedes Schiff durch (die 'values' in der dict) von CPU 
        for schiff in self.schiffe.values():

            # mögliche Start-Position wurde hinzugefügt zu der Liste
            # die Start-Position sind alle Positionen in dem Feld ohne die benutzten Felder 
            options = list(feld - used)

            # zufällige Start-Position von den gegebenen Optionen 
            pos = random.choice(options)

            # jedes Schiff hat eine Liste für nicht mögliche Start-Positionen
            # erstellen ein set, welches eine Liste beinhaltet für alle mögliche Start-Positionen
            notPossible = set()

            # Ausgangszustand für jedes Schiff, welches nicht plaziert wurde 
            platziert = False

            # von der Startpostition kann es rechts ('r'), links ('l'), hoch ('u') oder runter ('d')
            directions = set(['l', 'r', 'u', 'd'])

            # konvertiert die Position von einem Text zu einer Koordinate
            # ! konvertiert vom String (Beispiel: D1) zu X- und Y-Koordinate (bsp.: 'D1' = (x=0; y=0))
            # (A1 => x=0, y=0)
            # (D1 => x=0, y=0)
            x, y = Feld.decodePosition(pos)

            # Solange ein Schiff keine besetzte Postion hat, wird die While-Schleife ausgeführt
            while not platziert:

                # fügt mögliche Positionen für den Start-Punkt hinzu 
                # (Wenn ein Schiff nicht plaziert werden konnte, geht es zu dem nächsten Start-Punkt)
                # und sichert es in eine Liste 
                möglichePlätze = list()

                # wählt zufällig eine Richtung aus und löscht diese von der directions list
                # eine Richtung wird zufällig gewählt, weil die directions ein set() ist (set sind nicht geordnet)
                d = directions.pop()

                # wenn die ausgewählte Richtung rechts ist
                if d == 'r':
                    start = pos
                    end = Feld.encodePosition(x + schiff.Größe - 1, y)
                    
                    # wenn das Feld Ende nicht in das Feld passt
                    if end in feld:
                        möglichePlätze = getVonBis(start, end)

                # die selbe Logik für die anderen Richtungen  
                elif d == 'l':
                    start = pos
                    end = Feld.encodePosition(x - schiff.Größe + 1, y)
                    if end in feld:
                        möglichePlätze = getVonBis(start, end)

                elif d == 'u':
                    start = pos
                    end = Feld.encodePosition(x, y - schiff.Größe + 1)
                    if end in feld:
                        möglichePlätze = getVonBis(start, end)

                elif d == 'd':
                    start = pos
                    end = Feld.encodePosition(x, y + schiff.Größe - 1)
                    if end in feld:
                        möglichePlätze = getVonBis(start, end)

                # wenn der Algorithmus einen geeigneten Platz findet für das Schiff
                if len(möglichePlätze) > 0:
                    
                    # wenn der Platz schon belegt ist, wird dieser "Platz" ignoriert
                    # startet in eine andere Richtung
                    if len(set(möglichePlätze) & used) > 0:
                        möglichePlätze.clear()

                    # wenn die ausgewählte Position nicht benutzt ist
                    # wird das Schiff dort plaziert
                    # und die Position, und die Positionen um diesen Platz, (benutzten Positionen) werden als vergeben markiert
                    else:
                        # Schiff wird auf der Position plaziert 
                        for p in möglichePlätze:
                            #
                            self.getFeld().setValueByRef(p, schiff)

                        self.schiffe[schiff.id].setPosition(möglichePlätze)
                        # Resultat wird präsenteirt
                        # print('{} in {}'.format(schiff.id, möglichePlätze))

                        used = used.union(
                            self.UmgebungMarkieren(möglichePlätze))
                        # die Schiffe werden als plaziert markiert
                        platziert = True
                # wenn der Algorithmus Kein platz findet für das Schiff 
                

                # wenn alle Richtungen versucht wurden  
                # wird die Start-Postion hinzugefügt
                # daraufhin wird eine neue zufällige Start-Postion ausgewählt 
                if len(directions) == 0 and not platziert:
                    # wenn es unmöglich ist ein Platz für ein Schiff zu finden
                    # startet das Feld von dieser Position
                    # und fügt pos zu (set of) nicht startbare Positionen
                    notPossible.add(pos)

                    # wählt eine neue Start-Position aus
                    options = list(set(options) - notPossible)
                    pos = random.choice(options)

                    # neu zugewiesene Richtung von der neuen Start-Position
                    directions = set(['l', 'r', 'u', 'd'])
                    x, y = Feld.decodePosition(pos)

                if platziert:
                    break

# diese Methode gibt alle Positionen im Feld zwischen Start und Ende wieder 
# Beispiel getVonBis('D1', 'D6') ==> ['D1','D2','D3','D4','D5','D6']
def getVonBis(start, end):

    start_x, start_y = Feld.decodePosition(start)
    end_x, end_y = Feld.decodePosition(end)

    # Resultate werden in einer Liste gespeichert
    result = list()

    # Wenn der fall eintreten sollte, dass Start und Ende in der selben Spalte stehen
    if start_x == end_x:
        x = start_x

        # sorgt dies dafür, dass der Start kleiner als das Ende bleibt 
        if start_y > end_y:
            tmp = start_y
            start_y = end_y
            end_y = tmp

        # Start bis Ende durchlaufen
        # Alle Punkte (x,y) in Referenz abbilden: (0,0)='A1'
        for y in range(start_y, end_y + 1):
            ref = Feld.encodePosition(x, y)
            result.append(ref)

    # Wenn der fall eintritt, dass Start und Ende in derselben Zeile liegen 
    elif start_y == end_y:
        y = start_y
        if start_x > end_x:
            tmp = start_x
            start_x = end_x
            end_x = tmp
        for x in range(start_x, end_x + 1):
            ref = Feld.encodePosition(x, y)
            result.append(ref)

    return result
