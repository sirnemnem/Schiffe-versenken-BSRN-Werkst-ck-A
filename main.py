from classes.player import Player
from classes.player import Computer
import curses


# window.subwin(begin_y, begin_x)
# window.subwin(nlines, ncols, begin_y, begin_x)
# Return a sub-window, whose upper-left corner is at (begin_y, begin_x), and whose width/height is ncols/nlines.
# By default, the sub-window will extend from the specified position to the lower right corner of the window.


# window.derwin(begin_y, begin_x)
# window.derwin(nlines, ncols, begin_y, begin_x)
# An abbreviation for “derive window”, derwin() is the same as calling subwin(),
# except that begin_y and begin_x are relative to the origin of the window,
# rather than relative to the entire screen. Return a window object for the derived window.



MIN_HEIGHT = 30
MIN_WIDTH = 90

WELCOME_HEADER = 'Schiffe versenken'
CHOICE_HEADER = 'Make your Choice'
WELCOME_FOOTER = 'arrow keys to navigate | enter to select'

menu = ['Player vs CPU', 'Player 1 vs Player 2', 'Exit to Windows']
menu2 = ['Automatically', 'Manually']

def forceMinWindowSize():
    # Terminal Größe zurückgeben
    msg = 'Min terminal size is {} x {}'.format(MIN_WIDTH, MIN_HEIGHT)

    while 1:

        window = curses.initscr()
        window.clear()
        # Größe der x- und y-Achse des Terminals berechnen
        height, width = window.getmaxyx()
        # Mitte des Terminals berechnen
        y_pos, x_pos = max(height//2, 0), max(width//2 - len(msg)//2, 0)

        # Falls die Größe großer als das min ist, (kann man mit dem Spiel anfangen)
        if height >= MIN_HEIGHT and width >= MIN_WIDTH:
            break
        
        # Wenn die Terminalgröße kleiner als das min ist,
        # dann wird in der Mitte des Terminals die Nachricht (msg) ausgegeben
        window.addstr(y_pos, x_pos, msg)
        window.refresh()
        window.getch()
        window.clear()
        del window

    window.clear()
    del window

    return True


def createDisplay(header=WELCOME_HEADER, footer=WELCOME_FOOTER):
    # sicherstellen, dass Terminal die min. Größe und Breite erfüllt
    forceMinWindowSize()

    # *** erstellt ein Window-Objekt, welches der ganzen Komanndozeile repräsentiert
    window = curses.initscr()

    #  Ablesen der Höhe und Breite der Kommandozeile
    height, width = window.getmaxyx()

    # Die Kopfzeile soll ganz oben stehen
    y_cor = 0
    # Die Kopfzeile soll in der Mitte stehen
    x_cor = width//2 - len(WELCOME_HEADER)//2

    # Die Farbe 2 (Schwarz auf Red) wird eingeschaltet
    window.attron(curses.color_pair(2))
    # Kopfzeile wird in der Mitte geschriebn
    window.addstr(y_cor, x_cor, WELCOME_HEADER)

    #  Die Farbe 2 (Schwarz auf Red) wird ausgeschaltet
    window.attroff(curses.color_pair(2))

    # Die Fußzeile soll in der letzten Zeile geschrieben werden
    window.addstr(height-1, 0, footer)

    # Erstellen einer Fenster-Objekt, der von größten Window-Objekt abgeleitet wird
    # Sub win soll 2 Zeilen und 2 Spalten kleiner als Window- Objekt sein
    subwin = window.derwin(height-2, width-2, 1, 1)
    subwin.box()
    # window und subwin zurückgeben
    return (window, subwin)

def createDisplay2(header=CHOICE_HEADER, footer=WELCOME_FOOTER):
    # sicherstellen, dass Terminal die min. Größe und Breite erfüllt
    forceMinWindowSize()

    # *** erstellt ein Window-Objekt, welches der ganzen Komanndozeile repräsentiert
    window = curses.initscr()

    #  Ablesen der Höhe und Breite der Kommandozeile
    height, width = window.getmaxyx()

    # Die Kopfzeile soll ganz oben stehen
    y_cor = 0
    # Die Kopfzeile soll in der Mitte stehen
    x_cor = width//2 - len(CHOICE_HEADER)//2

    # Die Farbe 2 (Schwarz auf Red) wird eingeschaltet
    window.attron(curses.color_pair(2))
    # Kopfzeile wird in der Mitte geschriebn
    window.addstr(y_cor, x_cor, CHOICE_HEADER)

    #  Die Farbe 2 (Schwarz auf Red) wird ausgeschaltet
    window.attroff(curses.color_pair(2))

    # Die Fußzeile soll in der letzten Zeile geschrieben werden
    window.addstr(height-1, 0, footer)

    # Erstellen einer Fenster-Objekt, der von größten Window-Objekt abgeleitet wird
    # Sub win soll 2 Zeilen und 2 Spalten kleiner als Window- Objekt sein
    subwin = window.derwin(height-2, width-2, 1, 1)
    subwin.box()
    # window und subwin zurückgeben
    return (window, subwin)

# '' diese Methode sorgt dazu, dass der abgegebene Text in der mitte vom fenster steht
def showMsg(msg=''):

    window, subwin = createDisplay()

    height, width = window.getmaxyx()

    y = max(height // 2, 0)
    x = max(width // 2 - len(msg) // 2, 0)

    subwin.addstr(y, x, msg)

    window.refresh()
    subwin.refresh()

    window.getch()

    del subwin
    del window


def getPlayerName(player=1, msg=''): 

    name = ''
    footer = 'Enter your name here: '

    # echo Methode einschalten
    curses.echo()
    # Mauszeiger einschalten, sodass man sehen kann, wo man eintippt
    curses.curs_set(1)

    while 1:
        # Erstellung von zwei Fenster-Objekte
        window, subwin = createDisplay(footer=footer)

        # gibt ein Tuple zurück (Höhe, Breite)
        height, width = window.getmaxyx()

        # String ab dem Punk (y=1,x=1) im Subwin schreiben, der den Name des Spielers zurückgibt
        subwin.addstr(
            1, 1, '{}Enter a name for player number {}'.format(msg, player))

        # Akktualisierung um die Änderungen zu sehen
        window.refresh()
        subwin.refresh()

        # Die Eingabe gesteht in der Fußzeile
        y = height-1
        # '' Da die Fußzeile schon beschriften wurde, soll das Program
        # die Beschriftung ausweichen
        x = len(footer)

        # Alle Buchstaben (Zeichenkette) vor der Eingabe der Enter-Taste lesen
        name = window.getstr(y, x).decode().strip().upper()

        # Fenster-Obkjekte sauber machen
        window.clear()
        subwin.clear()

        # Die Objekte löschen
        del window
        del subwin

        # der Name darf nicht leer sein
        # Schleife so lange wiederholen lassen, bis der eingegebene Name gültig ist
        if len(name) > 0 and name != curses.KEY_RESIZE:
            break

    # echoing ausschalten
    curses.noecho()
    # Mauszeiger aussschalten, wird nicht mehr sichtbar
    curses.curs_set(0)

    return name


# diese Methode dient zur "Grafischen Darstellung" des Spiels
def drawField(playerField, footer, hideShips=True, alignment='center'):

    # Erstellung von Window und Subwin
    window, subwin = createDisplay(footer=footer)
    height, width = window.getmaxyx()
    h, w = subwin.getmaxyx()

    # Höhe und Breite von Feld erstellen
    gridHeight = playerField.getHeight() * 2
    gridWidth = playerField.getWidth() * 4

    # '' wo wir den Feld platzieren in der subwin
    grid_begin_y = h//2 - gridHeight//2
    grid_begin_x = w//2 - gridWidth//2

    # ''* bein. wo das Feld im subwin platziert wird
    if alignment.lower() == 'right':
        grid_begin_x = w - gridWidth - 2
    elif alignment.lower() == 'left':
        grid_begin_x = 2

    #'  Erstellung eines Feldes in sder
    grid = subwin.derwin(gridHeight, gridWidth, grid_begin_y, grid_begin_x)

    gridHeight, gridWidth = grid.getmaxyx()

    #' Jede 4 Spalte beginnen von der 3 Spalte ist ein '|'
    for x in range(3, gridWidth - 1, 4):
        grid.vline(0, x, '|', gridHeight - 1)

    # 'Jede 2 Zeile beginnen von der 1 Zeile ist ein '-'
    for y in range(1, gridHeight - 1, 2):
        grid.hline(y, 0, '-', gridWidth)

    # Die (erste) For-Schleife dient zur "Stelleneingabe" des Fields
    # in jeder 4 Stelle soll die Referenz ausgegeben werden
    for x in range(0, gridWidth - 1, 4):
        for y in range(0, gridHeight - 1, 2):

            posRef = playerField.encodePosition(x//4, y//2)
            value = playerField.getValueByRef(posRef)

            # hideShips == True
            # ' falls die Schiffe nicht im Feld gezeigt werden sollen
            if hideShips:
                # ' während des Spiels werden die Positionen von Schiff nie gezeigt
                # Referenz (zB: 'A10'), 'X' oder '#' ausgeben
                txt = posRef
                if value in ['X', '#']:
                    txt = value

            # ' falls die Schiffe ins Feld gezeigt werden sollen
            else:
                # falls kein Schiff vorliegt
                if value in ['O', 'X', '#']:
                    # Referenz ausgeben
                    txt = posRef

                #falls Schiff vorliegt
                else:
                    # Id zeigen
                    txt = value.getId()

            # 3 Plätze für txt reservieren
            # zB: 'A1' oder 'A10'
            grid.addstr(y, x, '%3s' % txt)
    
    # # Feld mit Farbe Cyan verferben
    grid.bkgd(' ', curses.color_pair(2))

    return (window, subwin, grid)


def checkPosition(playerField, x, y):

    # diese Methode prüft, ob ein Punkt im Feld als Ziel
    # gültig sein kann

    w = playerField.getWidth()
    h = playerField.getHeight()

    # ' Prüft ob x und y im Spielfeld liegen
    if x not in range(0, w) or y not in range(0, h):
        return False

    # ein freier Platz hat immer den Wert 'O'
    # Falls diese Bedingung nicht erfüllt ist, dann False zurückgeben
    if playerField.getValueByCor(x, y) != 'O':
        return False

    # Prüfen ob ein Schiff in der Umgebung vorliegt
    # falls ja, False zurückgeben
    if x + 1 < w:
        if playerField.getValueByCor(x+1, y) != 'O':
            return False
    if x - 1 >= 0:
        if playerField.getValueByCor(x-1, y) != 'O':
            return False
    if y + 1 < h:
        if playerField.getValueByCor(x, y+1) != 'O':
            return False
    if y - 1 >= 0:
        if playerField.getValueByCor(x, y-1) != 'O':
            return False
    # dieser Platz ist möglich
    return True


def checkShipPlace(playerField, start, end, size):

    # ob Start und Ende aus min 2 Buchstaben und max 3 Buchstaben bestehen
    # wenn ja, nächste Bedingung prüfen
    # wenn nein, False zurückgeben
    if len(start) not in range(2, 4) or len(end) not in range(2, 4):
        return False

    # prüfen ob ein Platz-Referenz vorkommt, zB: A1 in ['A1','A3','C4']
    if start in playerField.getPositions() and end in playerField.getPositions():

        # Platzreferenz auf x- und y-koordinaten abbilden
        start_x, start_y = playerField.decodePosition(start)
        end_x, end_y = playerField.decodePosition(end)

        # wenn es um eine Spalte geht, ist die X-Koordinate konstant
        if start_x == end_x:

            # sicherstellen, dass der kleinste Wert im Start und größte Wert im Ende steht
            if end_y < start_y:
                tmp = end_y
                end_y = start_y
                start_y = tmp

            # Ob der Platzbereich für ein Schiff ausreicht
            # 1 von Schiffgröße substrahieren, weil wir von 0 anfangen
            if end_y - start_y == size - 1:
                for y in range(start_y, end_y + 1):
                    # alle Plätze im Bereich püfen
                    # ob die Plätze schon vergeben sind
                    if(not checkPosition(playerField, start_x, y)):
                        return False
                return True

        # wenn es um eine Zeile angeht, die Y-Koordinate ist konstant
        elif start_y == end_y:

            if end_x < start_x:
                tmp = end_x
                end_x = start_x
                start_x = tmp

            if end_x - start_x == size - 1:
                for x in range(start_x, end_x + 1):
                    if not checkPosition(playerField, x, start_y):
                        return False
                return True
    # Falls keine Bedingung erfüllt wurde
    return False
    

def placeShips(player):

    # echo, sodass Spieler sehen kann, was er eingibt
    curses.echo()
    # Schaltet Mousezeigen ein, sodass der Spieler sehen kann, wo er text eingibt
    curses.curs_set(1)

    # Die Schiffe von diesem Spieler in playerShips speichern
    # Schiffe sind in einem Python dict gespeichert, wo Schlüssel
    # die Id des Schiffes uns der Wert das Schiff selbst
    playerShips = player.getShips().values()
    # alle schiffe durchgehen
    for ship in playerShips:
        footer = 'Enter ship place (example: A1:A4 = from A1 to A4): '

        while 1:
            # das akktualisierte Feld des Spielers abrufen und in playerFeld
            playerField = player.getField()

            # das Spielfield, wo der Spieler seine Schiffe plazieren kann, uaf dem Bildschirm zeigen
            window, subwin, grid = drawField(
                playerField, footer, False, 'right')

            # Groeße von Kommandozeile ermitteln
            height, width = window.getmaxyx()

            # Zeigen welches Schiff plazieren werden soll
            subwin.addstr(
                1, 1, 'Player: {}, place your ship in the field.'.format(player.getName()))
            subwin.addstr(2, 1, 'Ship ID: {}'.format(ship.getId()))
            subwin.addstr(3, 1, 'Ship name: {}'.format(ship.getName()))
            subwin.addstr(4, 1, 'Ship size: {}'.format(ship.getSize()))

            window.refresh()
            subwin.refresh()
            grid.refresh()

            # nur höchstens 7 Buchstaben einzugeben erlauben
            coordinates = window.getstr(
                height - 1, len(footer), 7).decode().strip().upper()

            window.clear()
            subwin.clear()
            grid.clear()

            del grid
            del subwin
            del window

            # prüfen ob der eingebene Text ':' beinhaltet und min Länge 5 ist
            # wenn ja die nächsten Bedingungen prüfen
            # wenn nein Fehlermeldung zeigen
            if(':' in coordinates and len(coordinates) > 4):

                # Text bei dem ':' in 2 Teile teilen, das Likne Teil ist der Start
                # und das rechte ist End des Bereiches
                start, end = tuple(coordinates.split(':', 1))

                # prüfen ob die Regeln für Plazierung eingehalten wurden
                # wenn ja, Schiff da stellen
                # wenn nein, diese Platze ignorieren, und Fehlermeldun zeigen
                if checkShipPlace(playerField, start, end, ship.getSize()):

                    start_x, start_y = playerField.decodePosition(start)
                    end_x, end_y = playerField.decodePosition(end)
                    # sicher stellen dass Ausgangpunkt kleiner als Endepunkt
                    if end_y < start_y:
                        tmp = end_y
                        end_y = start_y
                        start_y = tmp

                    if end_x < start_x:
                        tmp = end_x
                        end_x = start_x
                        start_x = tmp

                    # Platze mit diesem Shiff besetzen
                    for x in range(start_x, end_x + 1):
                        for y in range(start_y, end_y + 1):
                            # Wert der Postion mit Ship Objekt ersetzen
                            player.getField().setValueByCor(x, y, ship)
                            # das Schiff mit diser Id in diesem Platz legen
                            player.getShips()[ship.getId()].placeShip(
                                playerField.encodePosition(x, y))

                    break

            # Fehlermeldung Ergänzen
            footer = 'Place is not valid! Enter ship place (example: A1:A4 = from A1 to A4): '

    curses.noecho()
    curses.curs_set(0)

    window, subwin, grid = drawField(
        player.getField(), "press any key to continue.", True, 'right')

    y = 1
    subwin.addstr(y, 1, 'Player: {}'.format(player.getName()))

    # Schiffe und ihre Positionen zeigen
    for ship in player.getShips().values():
        y += 1
        subwin.addstr(y, 1, 'Ship name: {}, place: {}:{}'.format(
            ship.getName(), ship.getPosition()[0], ship.getPosition()[-1]))

    window.refresh()
    subwin.refresh()

    window.getch()

    subwin.clear()
    window.clear()

    del window
    del subwin
    del grid


def startGame(listOfPlayers):

    currentPlayerIdx = 0
    nextPlayerIdx = 1

    while True:

        currentPlayerIdx = currentPlayerIdx % 2
        nextPlayerIdx %= 2

        currentPlayer = listOfPlayers[currentPlayerIdx]
        nextPlayer = listOfPlayers[nextPlayerIdx]

        # 'Der CurrentPlayer (Spieler der gerade spielt) schießt auf dem Feld vom nextplayer (nächter Spieler)

        # Das Spielfeld vom anderen Spieler wird gezeigt
        playerField = nextPlayer.getField()

        # 'Feld im Zentrum des Fenster ausgeben, da Attribute 'alignment' von drawfield
        # nicht weitergegebem wurde
        window, subwin, grid = drawField(
            playerField, footer='Enter a shooting coordinates: ')

        curses.echo()
        curses.curs_set(1)

        h, w = subwin.getmaxyx()

        playerLeft = listOfPlayers[0]
        playerRight = listOfPlayers[1]

        subwin.addstr(1, 2, 'Player 1:')
        subwin.addstr(2, 2, playerLeft.getName())
        subwin.addstr(3, 2, 'Score: {}'.format(playerLeft.getScore()))

        # alle Schiffe durchlaufen und ausgeben
        for idx, (shipId, ship) in enumerate(playerLeft.getShips().items()):
            subwin.addstr(
                idx+4, 2, 'Ship id {} - hits {}/{}'.format(shipId, ship.hits, ship.size))

        x = w - max(len(playerRight.getName()), len('Ship id 1 - hits 6/6'))

        subwin.addstr(1, x-2, 'Player 2:')
        subwin.addstr(2, x-2, playerRight.getName())
        subwin.addstr(3, x-2, 'Score: {}'.format(playerRight.getScore()))

        for idx, (shipId, ship) in enumerate(playerRight.getShips().items()):
            subwin.addstr(
                idx+4, x-2, 'Ship id {} - hits {}/{}'.format(shipId, ship.hits, ship.size))

        subwin.addstr(h-2, 2, '{} is playing.'.format(currentPlayer.getName()))

        window.refresh()
        subwin.refresh()
        grid.refresh()

        w_height, w_width = window.getmaxyx()

        # prüfen ob ein Mensch oder Cpu dran ist
        if type(currentPlayer) == Player:
            # Falls Mensch, dann wird auf Eingabe des Benutzers gewartet
            goal = window.getstr(3).decode().strip().upper()
        else:
            # Falls Cpu dran ist
            # dann Schießziel wird zufällig ausgesucht
            goal = currentPlayer.shoot(
                list(playerField.getPositions().keys()))

            showMsg('CPU is playing')

        window.clear()
        subwin.clear()
        grid.clear()

        # wird dazu verwendet, um zu wissen, ob ein Schoß gültig war
        success = False

        # prüfen ob Ziel gültig ist
        # 1. Bedingung:
        #  Länge des Zeilpunktes ist min 2 und max 3 Buchstaben
        if len(goal) in range(2, 4) and goal != curses.KEY_RESIZE:
            # 2. Bedingung:
            # Punktreferenz kommt im Spielfeld vor
            if goal in nextPlayer.getField().getPositions():
                # 3. Bedungung
                # Auf diesem Punkt wurde noch nie gespielt 
                if nextPlayer.getField().getValueByRef(goal) not in ['#', 'X']:
                    # es wird davon ausgegangen, dass kein Schif getroffen wurde
                    txt = 'MISS'

                    if nextPlayer.getField().getValueByRef(goal) == 'O':
                        # falls echt kein Schiff getroffen wurde
                        # dann Wert von diesem Punkt im Feld mit '#' ersetzen
                        nextPlayer.getField().setValueByRef(goal, '#')
                    else:
                        # falls ein Schif getroffen wurde
                        # 'Anzahl von Schläge dieses Schiffes inkeremtieren
                        nextPlayer.getField().getValueByRef(goal).gotDirectHit()
                        # Wert von diesem Punkt im Feld mit 'X' ersetzen
                        nextPlayer.getField().setValueByRef(goal, 'X')
                        # Wert von txt mit 'HIT' ersetzen, weil ein Schif getroffen wurde
                        txt = 'HIT'
                        # Score des Spielers, wer dran ist und ein Schiff vom Gegner getroffen hat,
                        # wird um 1 inkrementiert
                        currentPlayer.incrementScore()

                        # falls Cpu der Spieler ist, der dran ist
                        if type(currentPlayer) == Computer:
                            # Computer wird darauf hingewiesen, dass er ein Treffer in diesem Punkt hatte
                            # Sodass er beim nächsten Spiel in der Umgebung von diesem Platz spielt
                            currentPlayer.success(goal)

                    # Zeigen ob man ein Schiff getroffen hat oder nicht
                    window, subwin, grid = drawField(
                        nextPlayer.getField(), 'Press any key to continue')

                    h, w = subwin.getmaxyx()
                    subwin.addstr(h-2, 2, ' IT IS A {}'.format(txt))

                    # Um Änderungen zu sehen
                    window.refresh()
                    subwin.refresh()
                    grid.refresh()

                    # pausieren bis Benutzen reagiert
                    window.getch()

                    # 'Falls alle Bedingungen erfüllt wurden sind
                    # hinweisen dass Erfolgreiche Versuche durchgeführt wurden sind
                    success = True

        # Falls eine Versuch erfolgreich war
        if success == True:
            currentPlayerIdx = currentPlayerIdx + 1
            nextPlayerIdx += 1

        window.clear()
        subwin.clear()
        grid.clear()

        curses.noecho()
        curses.curs_set(0)

        del subwin
        del window
        del grid

        if isGameOver(nextPlayer.getShips()):
            showMsg('{} has won !!'.format(currentPlayer.getName()))
            break


def isGameOver(playerShips):
    # 'durchlauft alle Schiffe, die ein Spieler hat
    # 'und prüft ob alle zerstört sind
    for ship in playerShips.values():
        # falls nur ein SChiff noch nicht zerstört ist, dann Spiel soll weiter laufen
        if ship.getState() == True:
            return False

    # Alle Schiffe vom Spieler sind zerstört
    # Game is Over
    return True


def playerVsPlayer():

    playerName = getPlayerName()

    # Spieler Objekt wird erzeugt
    player1 = Player(playerName)

    # Namen des 2. Spielers soll unterschiedlich von Namen des 1. Spielers sein
    while playerName == player1.getName():
        playerName = getPlayerName(2, 'Player 2 should be different. ')

    # Spieler Objekt wird erzeugt
    player2 = Player(playerName)

    # Spieler 1 soll seine Shiffe in seinem Field platzieren
    showMsg('Player 1, do you want to set the boats automatically or manually?')
    choice = print_menu2()
    if choice == "automatically":
        player1.placeShipsAuto()
        showMsg('Your Ships have been placed')
    elif choice == "manually":
        showMsg('Player 2, please look away')
        placeShips(player1)

    showMsg('Player 2, do you want to set the boats automatically or manually?')
    choice = print_menu2()
    if choice == "automatically":
        player2.placeShipsAuto()
        showMsg('Your Ships have been placed')
    elif choice == "manually":
        showMsg('Player 1, please look away')
        placeShips(player2)

    # startet das Spiel zwischen zwei Spieler
    startGame([player1, player2])


def playerVsCpu():
    showMsg('You want to play vs CPU')
    
    playerName = getPlayerName()
    # einen Namen außer CPU und Computer aussuchen
    while playerName in ['CPU', 'COMPUTER']:
        playerName = getPlayerName(
            2, 'Player NAME should be different from. {}'.format(playerName))
    
    showMsg('Do you want to set the boats automatically or manually?')
    player = Player(playerName)
    choice = print_menu2()
    if choice == "automatically":
        player.placeShipsAuto()
        showMsg('Your Ships have been placed')
    elif choice == "manually":
        placeShips(player)
    # Spieler Objekt erzeugen
    

    # Anzahl der Schiffe ist auf 6 festgelegt
    # Die Große des Feldes is automatisch 10x10

    # Spieler anfordern, die Schiffe in seinem Feld zu platzieren

    # Computer Object erzeugen
    cpu = Computer()

    # CPU den Befehl geben, die Schiffe in seinem Feld zu platzieren
    cpu.placeShips()

    window, subwin, grid = drawField(
        player.getField(), "press any key to continue.", True, 'right')

    y = 1
    subwin.addstr(y, 1, 'Player: {} is placing his ships'.format(cpu.getName()))
    y+=1 
    subwin.addstr(y, 1, 'click to continue')
    # Die For-Schleife unten wurde während Debuging benutzt, um
    # ' zu sehen, ob der CPU seine Schiffe korrekt im Feld positioniert hat
    # Bitte 'uncomment' die Zeilen um zu sehen

    # for ship in cpu.getShips().values():
    #     y += 1
    #     subwin.addstr(y, 1, 'Ship name: {}, place: {}'.format(
    #         ship.getName(), ship.getPosition()))

    window.refresh()
    subwin.refresh()

    window.getch()

    subwin.clear()
    window.clear()

    startGame([player, cpu])


def endGame():
    # Falls der Benutzer Exit aussucht, soll die untrige Nachricht angezeigt werden
    showMsg('you want to end the game')


def print_menu():

    currentIndex = 0

    while 1:

        # Erstellung von Zwei Window Objekte
        # Window hat Kopf- und Fußzeile
        window, subwin = createDisplay()

        # Schreiben der Menuelemente vertikal ab der Zeile 1 und Spalte 1,
        # weil der Rand der Subwin die erste Zeile und Spalte besitzt

        for index, element in enumerate(menu):

            # 'das ausgewählte Element soll mit der Farbe (Schwarz auf Weiß) geschrieben werden

            if index == currentIndex:
                # Farbe an
                subwin.attron(curses.color_pair(1))
                # 'ausgewälte element mit farbe schreiben
                subwin.addstr(index + 1, 1, element)
                # Farbe aus
                subwin.attroff(curses.color_pair(1))
            else:
                # die nicht ausgewählte Menu-Elemente bekommen keine Farbe
                subwin.addstr(index + 1, 1, element)

        # Aktualisierung um die Änderungen zu sehen
        window.refresh()
        subwin.refresh()

        # Eingabe der Benutzer ablesen
        key = window.getch()

        window.clear()
        subwin.clear()

        if key == curses.KEY_UP and currentIndex > 0:
            # Falls der Benutzer 'Pfeil-nach-oben' Taste gedrückt hat
            # Currentindex inkrementieren solange das erste Element nicht erreicht wurde
            currentIndex = currentIndex - 1
        elif key == curses.KEY_DOWN and currentIndex < len(menu) - 1:
            # Falls der Benutzer Pfeil-nach-unten Taste gedrückt hat
            # Currentindex inkrementieren solange das letzte Element nicht erreicht wurde
            currentIndex = currentIndex + 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # Falls der Benutzer 'Eingabe-Taste' gedrückt hat
            window.clear()
            subwin.clear()

            window.refresh()
            subwin.refresh()

            break

    del subwin
    del window

    return menu[currentIndex].lower()

def print_menu2():

    currentIndex = 0

    while 1:

        # Erstellung von Zwei Window Objekte
        # Window hat Kopf- und Fußzeile
        window, subwin = createDisplay2()

        # Schreiben der Menuelemente vertikal ab der Zeile 1 und Spalte 1,
        # weil der Rand der Subwin die erste Zeile und Spalte besitzt

        for index, element in enumerate(menu2):

            # 'das ausgewählte Element soll mit der Farbe (Schwarz auf Weiß) geschrieben werden

            if index == currentIndex:
                # Farbe an
                subwin.attron(curses.color_pair(1))
                # 'ausgewälte element mit farbe schreiben
                subwin.addstr(index + 1, 1, element)
                # Farbe aus
                subwin.attroff(curses.color_pair(1))
            else:
                # die nicht ausgewählte Menu-Elemente bekommen keine Farbe
                subwin.addstr(index + 1, 1, element)

        # Aktualisierung um die Änderungen zu sehen
        window.refresh()
        subwin.refresh()

        # Eingabe der Benutzer ablesen
        key = window.getch()

        window.clear()
        subwin.clear()

        if key == curses.KEY_UP and currentIndex > 0:
            # Falls der Benutzer 'Pfeil-nach-oben' Taste gedrückt hat
            # Currentindex inkrementieren solange das erste Element nicht erreicht wurde
            currentIndex = currentIndex - 1
        elif key == curses.KEY_DOWN and currentIndex < len(menu2) - 1:
            # Falls der Benutzer Pfeil-nach-unten Taste gedrückt hat
            # Currentindex inkrementieren solange das letzte Element nicht erreicht wurde
            currentIndex = currentIndex + 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # Falls der Benutzer 'Eingabe-Taste' gedrückt hat
            window.clear()
            subwin.clear()

            window.refresh()
            subwin.refresh()

            break

    del subwin
    del window

    return menu2[currentIndex].lower()


def main(stdscr):

    #' blinkende Mousezeiger ausschalten
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)

    while 1:
        # unendliche Schleife, weil das Programm nur dann aufhören soll, wenn der Benutzer "Exit" auswählt

        # Diese Methode ermöglicht dem Benutzer einen Spielmodus auszuwählen
        # Der Rückgabewert (String) wird klein geschrieben
        choice = print_menu()

        if choice == "player vs cpu":
            # Abruf der Methode, die für den "Player vs Cpu"-Spielmodus zuständig ist
            playerVsCpu()
        elif choice == 'player 1 vs player 2':
            # Abruf der Methode, die für den "Player1 vs Player2"-Spielmodus zuständig ist
            playerVsPlayer()
        elif choice == 'exit':
            # Abruf der Methode, die für das Beenden des Spieles zuständig ist
            endGame()
            break

        


if __name__ == "__main__":
    # 'the wrapper() function takes a callable object and 
    # does the initializations described above, also initializing colors if 
    # color support is present. wrapper() then runs your provided callable. 
    # Once the callable returns, wrapper() will restore the original state of the terminal.
    curses.wrapper(main)
