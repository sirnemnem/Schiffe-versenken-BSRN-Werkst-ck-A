from typing import Set
from classes.field import Field
from classes.ship import Ship
import random

# den Schiffe werden Namen (Values) "und IDen (Keys)" zugeördnet
SHIP_NAMES = {6: 'F221 Hessen', 5: 'F264 Ludwigshafen am Rhein', 4: 'P6126 S76 Frettchen',
              3: 'M1098 Siegburg', 2: 'M1069 Homburg', 1: 'M1061 Rottweil'}


class Player:
    def __init__(self, name, numShips=6):
        self.name = name
        self.score = 0
        self.numShips = numShips
        self.ships = dict()
        self.field = Field()
        self.initShips()

    # Setters and getters
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def getField(self):
        return self.field

    def setField(self, field):
        self.field = field

    def getShips(self):
        return self.ships

    def setShips(self, ships):
        self.ships = ships

    # diese Methode dient zur Initialierung von ships
    def initShips(self):

        # die Schleife fängt "an der Stelle" 0 an und geht die "number of ships" durch
        for i in range(0, self.numShips):
            # zu jedem Schiff wird eine shipId "zugeordnet"
            shipId = len(SHIP_NAMES) - i
            # shipName wird von dem dict "geholt" 
            shipName = SHIP_NAMES[shipId]
            # wird den Wert von "shipId" zugeordnet
            size = shipId

            # falls die Größe kleiner als 1 oder 1 ist, dann wird sie automatisch
            # die Größe 2 zugeordnet 
            if size <= 1:
                size = 2

            # ships ist dict
            # Schlüssel ist der Id des Schiffes und Wert ist der Schiff-Objekt selbst
            self.ships[shipId] = Ship(shipId, shipName, size)

    # diese Methode dient zur Inkremtierung des Scores
    def incrementScore(self):
        self.setScore(self.getScore()+1)
    
    def markSurroundingAsUsed(self, shipPlace):
        # diese Methode markiert alle Plätze im Feld, 
        # die ein Schiff umgeben als nicht verfügbar
        # und gibt die zurück
        
        places = set(shipPlace)
        field = set(self.getField().getPositions().keys())
        for place in shipPlace:
            x, y = Field.decodePosition(place)

            # rechts von einem Platz
            if Field.encodePosition(x+1, y) in field:
                places.add(Field.encodePosition(x+1, y))
            
            # Links
            if Field.encodePosition(x-1, y) in field:
                places.add(Field.encodePosition(x-1, y))

            # unter
            if Field.encodePosition(x, y+1) in field:
                places.add(Field.encodePosition(x, y+1))

            # oben
            if Field.encodePosition(x, y-1) in field:
                places.add(Field.encodePosition(x, y-1))

        return set(places)

    def placeShipsAuto(self):

        # save the used positions in a set
        used = set()

        # save the keys of the "getPositions dictionary" "getField dictionary" to the set 
        field = set(self.getField().getPositions().keys())

        # die For-Schleife geht alle Schiffe (die 'values' in der dic) von CPU durch
        for ship in self.ships.values():

            # possible starting positions are added to a list
            # starting position are all positions in a field without the used places
            options = list(field - used)

            # randomly pick a starting position from possible options
            pos = random.choice(options)

            # each ship has a list of not possible starting places, (therefore)
            # create a set that contains the list of impossible starting points
            notPossible = set()

            # the initial status of each ship is not placed
            placed = False

            # from a starting position it can go left ('l'), right ('r'), up ('u'), or down ('d')
            directions = set(['l', 'r', 'u', 'd'])

            # (convert the postion from text to x and y coordinates)
            # ! convert von Referenzen (bsp: A1) to X- und Y-Koordinate (bsp: 'A1' = (x=0, y=0))
            # (A1 => x=0, y=0)
            x, y = Field.decodePosition(pos)

            # Solange ein Schiff keine Position hat, wird die While-Schleife durchgeführt
            while not placed:

                # adds possible places from starting point (if a ship is not placed 
                # next to the staring point) and saves it to a list
                possiblePlaces = list()

                # randomly pick a direction and remove it from directions list
                # a dirction will be randoml picked, because directions is a set() (set are not ordered)
                d = directions.pop()

                # if the chosen direction is right
                if d == 'r':
                    start = pos
                    end = Field.encodePosition(x + ship.size - 1, y)
                    # if the field end does fit in the grid
                    if end in field:
                        possiblePlaces = getBetween(start, end)

                # the same  logic for other directions
                elif d == 'l':
                    start = pos
                    end = Field.encodePosition(x - ship.size + 1, y)
                    if end in field:
                        possiblePlaces = getBetween(start, end)

                elif d == 'u':
                    start = pos
                    end = Field.encodePosition(x, y - ship.size + 1)
                    if end in field:
                        possiblePlaces = getBetween(start, end)

                elif d == 'd':
                    start = pos
                    end = Field.encodePosition(x, y + ship.size - 1)
                    if end in field:
                        possiblePlaces = getBetween(start, end)

                # if the algorithm found a possible place for the ship
                if len(possiblePlaces) > 0:
                    # if the place contains a used position, ignore this "place" and
                    # start over in other direction
                    if len(set(possiblePlaces) & used) > 0:
                        possiblePlaces.clear()
                    # if the possible places don't include used places
                    # then place this ship here
                    # and mark this place and places around it as used too
                    else:
                        # place the ship here
                        for p in possiblePlaces:
                            #
                            self.getField().setValueByRef(p, ship)

                        self.ships[ship.id].setPosition(possiblePlaces)
                        # show me the result
                        # print('{} in {}'.format(ship.id, possiblePlaces))

                        used = used.union(
                            self.markSurroundingAsUsed(possiblePlaces))
                        # mark the ship as placed
                        placed = True
                # if the algorithm didn't find any place for the ship

                # if all direction are tried
                # add this starting position
                # then pick another random position
                if len(directions) == 0 and not placed:
                    # it is impossible to place this ship in the
                    # field starting from this pos
                    # so add pos to (the set of) not possible starting points
                    notPossible.add(pos)

                    # pick a new starting point
                    options = list(set(options) - notPossible)
                    pos = random.choice(options)

                    # re-assign directions for the new starting point
                    directions = set(['l', 'r', 'u', 'd'])
                    x, y = Field.decodePosition(pos)

                if placed:
                    break

# Klasse Computer "irbt" von Klasse Player, da Klasse Computer die "Eigenschaften/Methoden " von Klasse
# Player irbt (as well as Attribute/andere Methoden (Zeilen 72, 90, 98, 115))
class Computer(Player):

    # ... und die Anzahl von Schiffen initializieren (numShips=6)
    def __init__(self, name='CPU', numShips=6):
        super().__init__(name, numShips)
        self.lastSuccess = ''
        self.played = set()
        self.memory = dict()

    def shoot(self, placesList):

        # options beinhaltet alle Plätze im Feld außer die benuztze Plätze
        options = list(set(placesList) - self.played)
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

    def success(self, ref):
        # cpu wird mit dieser Methode hingewiesen, dass sein Wurf erflogreich war,
        # sodass, er sich an diesem Punk errinert, und im Memory die Refrenz als Schlüssel und 
        # und Die Referenzen der umgebenden Plätze als Wert speichert
        self.lastSuccess = ref

        next = self.markSurroundingAsUsed([ref])

        self.memory[ref] = set(next - self.played)

    def markSurroundingAsUsed(self, shipPlace):
        # diese Methode markiert alle Plätze im Feld, 
        # die ein Schiff umgeben als nicht verfügbar
        # und gibt die zurück
        
        places = set(shipPlace)
        field = set(self.getField().getPositions().keys())
        for place in shipPlace:
            x, y = Field.decodePosition(place)

            # rechts von einem Platz
            if Field.encodePosition(x+1, y) in field:
                places.add(Field.encodePosition(x+1, y))
            
            # Links
            if Field.encodePosition(x-1, y) in field:
                places.add(Field.encodePosition(x-1, y))

            # unter
            if Field.encodePosition(x, y+1) in field:
                places.add(Field.encodePosition(x, y+1))

            # oben
            if Field.encodePosition(x, y-1) in field:
                places.add(Field.encodePosition(x, y-1))

        return set(places)

    def placeShips(self):

        # save the used positions in a set
        used = set()

        # save the keys of the "getPositions dictionary" "getField dictionary" to the set 
        field = set(self.getField().getPositions().keys())

        # die For-Schleife geht alle Schiffe (die 'values' in der dic) von CPU durch
        for ship in self.ships.values():

            # possible starting positions are added to a list
            # starting position are all positions in a field without the used places
            options = list(field - used)

            # randomly pick a starting position from possible options
            pos = random.choice(options)

            # each ship has a list of not possible starting places, (therefore)
            # create a set that contains the list of impossible starting points
            notPossible = set()

            # the initial status of each ship is not placed
            placed = False

            # from a starting position it can go left ('l'), right ('r'), up ('u'), or down ('d')
            directions = set(['l', 'r', 'u', 'd'])

            # (convert the postion from text to x and y coordinates)
            # ! convert von Referenzen (bsp: A1) to X- und Y-Koordinate (bsp: 'A1' = (x=0, y=0))
            # (A1 => x=0, y=0)
            x, y = Field.decodePosition(pos)

            # Solange ein Schiff keine Position hat, wird die While-Schleife durchgeführt
            while not placed:

                # adds possible places from starting point (if a ship is not placed 
                # next to the staring point) and saves it to a list
                possiblePlaces = list()

                # randomly pick a direction and remove it from directions list
                # a dirction will be randoml picked, because directions is a set() (set are not ordered)
                d = directions.pop()

                # if the chosen direction is right
                if d == 'r':
                    start = pos
                    end = Field.encodePosition(x + ship.size - 1, y)
                    # if the field end does fit in the grid
                    if end in field:
                        possiblePlaces = getBetween(start, end)

                # the same  logic for other directions
                elif d == 'l':
                    start = pos
                    end = Field.encodePosition(x - ship.size + 1, y)
                    if end in field:
                        possiblePlaces = getBetween(start, end)

                elif d == 'u':
                    start = pos
                    end = Field.encodePosition(x, y - ship.size + 1)
                    if end in field:
                        possiblePlaces = getBetween(start, end)

                elif d == 'd':
                    start = pos
                    end = Field.encodePosition(x, y + ship.size - 1)
                    if end in field:
                        possiblePlaces = getBetween(start, end)

                # if the algorithm found a possible place for the ship
                if len(possiblePlaces) > 0:
                    # if the place contains a used position, ignore this "place" and
                    # start over in other direction
                    if len(set(possiblePlaces) & used) > 0:
                        possiblePlaces.clear()
                    # if the possible places don't include used places
                    # then place this ship here
                    # and mark this place and places around it as used too
                    else:
                        # place the ship here
                        for p in possiblePlaces:
                            #
                            self.getField().setValueByRef(p, ship)

                        self.ships[ship.id].setPosition(possiblePlaces)
                        # show me the result
                        # print('{} in {}'.format(ship.id, possiblePlaces))

                        used = used.union(
                            self.markSurroundingAsUsed(possiblePlaces))
                        # mark the ship as placed
                        placed = True
                # if the algorithm didn't find any place for the ship

                # if all direction are tried
                # add this starting position
                # then pick another random position
                if len(directions) == 0 and not placed:
                    # it is impossible to place this ship in the
                    # field starting from this pos
                    # so add pos to (the set of) not possible starting points
                    notPossible.add(pos)

                    # pick a new starting point
                    options = list(set(options) - notPossible)
                    pos = random.choice(options)

                    # re-assign directions for the new starting point
                    directions = set(['l', 'r', 'u', 'd'])
                    x, y = Field.decodePosition(pos)

                if placed:
                    break

# diese Methode gibt alle Plätze in einem Feld zwischen start und Ende
# zB: getBetween('A1', 'A6') ==> ['A1','A2','A3','A4','A5','A6']
def getBetween(start, end):

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
