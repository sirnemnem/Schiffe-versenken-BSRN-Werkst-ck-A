from classes.player import Spieler
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

WILKOMMENS_HEADER = 'Schiffe versenken'
WAHL_HEADER = 'Make your Choice'
WILKOMMENS_FOOTER = 'Pfeiltasten zum navigieren benutzen | Entertaste zum auswählen benutzen'

menu1 = ['Spieler vs CPU', 'Spieler 1 vs Spieler 2', 'Zurückkehren zu Windows']
menu2 = ['Automatisch', 'Manuell']
menu3 = ['Ja', 'Nein']

def MinFensterGröße():
    # Terminal Größe zurückgeben
    msg = 'Min terminal Größe ist {} x {}'.format(MIN_WIDTH, MIN_HEIGHT)

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


def DisplayErstellen(header=WILKOMMENS_HEADER, footer=WILKOMMENS_FOOTER):
    # sicherstellen, dass Terminal die min. Größe und Breite erfüllt
    MinFensterGröße()

    # *** erstellt ein Window-Objekt, welches der ganzen Komanndozeile repräsentiert
    window = curses.initscr()

    #  Ablesen der Höhe und Breite der Kommandozeile
    height, width = window.getmaxyx()

    # Die Kopfzeile soll ganz oben stehen
    y_cor = 0
    # Die Kopfzeile soll in der Mitte stehen
    x_cor = width//2 - len(WILKOMMENS_HEADER)//2

    # Die Farbe 2 (Schwarz auf Red) wird eingeschaltet
    window.attron(curses.color_pair(2))
    # Kopfzeile wird in der Mitte geschriebn
    window.addstr(y_cor, x_cor, WILKOMMENS_HEADER)

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
def NachrichtZeigen(msg=''):

    window, subwin = DisplayErstellen()

    height, width = window.getmaxyx()

    y = max(height // 2, 0)
    x = max(width // 2 - len(msg) // 2, 0)

    subwin.addstr(y, x, msg)

    window.refresh()
    subwin.refresh()

    window.getch()

    del subwin
    del window


def getSpielerName(spieler=1, msg=''): 

    name = ''
    footer = 'Geben Sie ihren Namen ein: '

    # echo Methode einschalten
    curses.echo()
    # Mauszeiger einschalten, sodass man sehen kann, wo man eintippt
    curses.curs_set(1)

    while 1:
        # Erstellung von zwei Fenster-Objekte
        window, subwin = DisplayErstellen(footer=footer)

        # gibt ein Tuple zurück (Höhe, Breite)
        height, width = window.getmaxyx()

        # String ab dem Punk (y=1,x=1) im Subwin schreiben, der den Name des Spielers zurückgibt
        subwin.addstr(
            1, 1, '{}Geben Sie einen Namen für Spieler Nummer {} an'.format(msg, spieler))

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
def FeldZiehen(SpielerFeld, footer, hideSchiffe=True, alignment='center'):

    # Erstellung von Window und Subwin
    window, subwin = DisplayErstellen(footer=footer)
    height, width = window.getmaxyx()
    h, w = subwin.getmaxyx()

    # Höhe und Breite von Feld erstellen
    gridHeight = SpielerFeld.getHeight() * 2
    gridWidth = SpielerFeld.getWidth() * 4

    # '' wo wir den Feld platzieren in der subwin
    grid_begin_y = h//2 - gridHeight//2
    grid_begin_x = w//2 - gridWidth//2

    # ''* bein. wo das Feld im subwin platziert wird
    if alignment.lower() == 'rechts':
        grid_begin_x = w - gridWidth - 2
    elif alignment.lower() == 'links':
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

            posRef = SpielerFeld.encodePosition(x//4, y//2)
            value = SpielerFeld.getValueByRef(posRef)

            # hideSchiffe == True
            # ' falls die Schiffe nicht im Feld gezeigt werden sollen
            if hideSchiffe:
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


def PositionsCheck(SpielerFeld, x, y):

    # diese Methode prüft, ob ein Punkt im Feld als Ziel
    # gültig sein kann

    w = SpielerFeld.getWidth()
    h = SpielerFeld.getHeight()

    # ' Prüft ob x und y im Spielfeld liegen
    if x not in range(0, w) or y not in range(0, h):
        return False

    # ein freier Platz hat immer den Wert 'O'
    # Falls diese Bedingung nicht erfüllt ist, dann False zurückgeben
    if SpielerFeld.getValueByCor(x, y) != 'O':
        return False

    # Prüfen ob ein Schiff in der Umgebung vorliegt
    # falls ja, False zurückgeben
    if x + 1 < w:
        if SpielerFeld.getValueByCor(x+1, y) != 'O':
            return False
    if x - 1 >= 0:
        if SpielerFeld.getValueByCor(x-1, y) != 'O':
            return False
    if y + 1 < h:
        if SpielerFeld.getValueByCor(x, y+1) != 'O':
            return False
    if y - 1 >= 0:
        if SpielerFeld.getValueByCor(x, y-1) != 'O':
            return False
    # dieser Platz ist möglich
    return True


def checkSchiffsPlatz(SpielerFeld, start, end, Größe):

    # ob Start und Ende aus min 2 Buchstaben und max 3 Buchstaben bestehen
    # wenn ja, nächste Bedingung prüfen
    # wenn nein, False zurückgeben
    if len(start) not in range(2, 4) or len(end) not in range(2, 4):
        return False

    # prüfen ob ein Platz-Referenz vorkommt, zB: A1 in ['A1','A3','C4']
    if start in SpielerFeld.getPositions() and end in SpielerFeld.getPositions():

        # Platzreferenz auf x- und y-koordinaten abbilden
        start_x, start_y = SpielerFeld.decodePosition(start)
        end_x, end_y = SpielerFeld.decodePosition(end)

        # wenn es um eine Spalte geht, ist die X-Koordinate konstant
        if start_x == end_x:

            # sicherstellen, dass der kleinste Wert im Start und größte Wert im Ende steht
            if end_y < start_y:
                tmp = end_y
                end_y = start_y
                start_y = tmp

            # Ob der Platzbereich für ein Schiff ausreicht
            # 1 von Schiffgröße substrahieren, weil wir von 0 anfangen
            if end_y - start_y == Größe - 1:
                for y in range(start_y, end_y + 1):
                    # alle Plätze im Bereich püfen
                    # ob die Plätze schon vergeben sind
                    if(not PositionsCheck(SpielerFeld, start_x, y)):
                        return False
                return True

        # wenn es um eine Zeile angeht, die Y-Koordinate ist konstant
        elif start_y == end_y:

            if end_x < start_x:
                tmp = end_x
                end_x = start_x
                start_x = tmp

            if end_x - start_x == Größe - 1:
                for x in range(start_x, end_x + 1):
                    if not PositionsCheck(SpielerFeld, x, start_y):
                        return False
                return True
    # Falls keine Bedingung erfüllt wurde
    return False
    

def SchiffePlatzieren(spieler):

    # echo, sodass Spieler sehen kann, was er eingibt
    curses.echo()
    # Schaltet Mousezeigen ein, sodass der Spieler sehen kann, wo er text eingibt
    curses.curs_set(1)

    # Die Schiffe von diesem Spieler in playerSchiffe speichern
    # Schiffe sind in einem Python dict gespeichert, wo Schlüssel
    # die Id des Schiffes uns der Wert das Schiff selbst
    SpielerSchiffe = spieler.getSchiffe().values()
    # alle schiffe durchgehen
    for schiff in SpielerSchiffe:
        footer = 'Geben Sie die Position für das Schiff ein (bsp.: A1:A4 = von A1 bis A4): '

        while 1:
            # das akktualisierte Feld des Spielers abrufen und in playerFeld
            SpielerFeld = spieler.getField()

            # das Spielfield, wo der Spieler seine Schiffe plazieren kann, uaf dem Bildschirm zeigen
            window, subwin, grid = FeldZiehen(
                SpielerFeld, footer, False, 'rechts')

            # Groeße von Kommandozeile ermitteln
            height, width = window.getmaxyx()

            # Zeigen welches Schiff plazieren werden soll
            subwin.addstr(
                1, 1, 'Spieler: {}, platzieren Sie ihr Schiff im Feld.'.format(spieler.getName()))
            subwin.addstr(2, 1, 'Schiffs ID: {}'.format(schiff.getId()))
            subwin.addstr(3, 1, 'Schiffsname: {}'.format(schiff.getName()))
            subwin.addstr(4, 1, 'Schiffsgröße: {}'.format(schiff.getGröße()))

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
                if checkSchiffsPlatz(SpielerFeld, start, end, schiff.getGröße()):

                    start_x, start_y = SpielerFeld.decodePosition(start)
                    end_x, end_y = SpielerFeld.decodePosition(end)
                    # sicher stellen dass Ausgangpunkt kleiner als Endepunkt
                    if end_y < start_y:
                        tmp = end_y
                        end_y = start_y
                        start_y = tmp

                    if end_x < start_x:
                        tmp = end_x
                        end_x = start_x
                        start_x = tmp

                    # Platze mit diesem Schiff besetzen
                    for x in range(start_x, end_x + 1):
                        for y in range(start_y, end_y + 1):
                            # Wert der Postion mit Schiff Objekt ersetzen
                            spieler.getField().setValueByCor(x, y, schiff)
                            # das Schiff mit diser Id in diesem Platz legen
                            spieler.getSchiffe()[schiff.getId()].SchiffPlatzieren(
                                SpielerFeld.encodePosition(x, y))

                    break

            # Fehlermeldung Ergänzen
            footer = 'Position ist nicht valide! Geben Sie die Position für das Schiff ein (bsp.: A1:A4 = von A1 bis A4): '

    curses.noecho()
    curses.curs_set(0)

    window, subwin, grid = FeldZiehen(
        spieler.getField(), "Drücken Sie eine Taste um fortzufahren.", True, 'rechts')

    y = 1
    subwin.addstr(y, 1, 'Spieler: {}'.format(spieler.getName()))

    # Schiffe und ihre Positionen zeigen
    for schiff in spieler.getSchiffe().values():
        y += 1
        subwin.addstr(y, 1, 'Schiffsname: {}, Position: {}:{}'.format(
            schiff.getName(), schiff.getPosition()[0], schiff.getPosition()[-1]))

    window.refresh()
    subwin.refresh()

    window.getch()

    subwin.clear()
    window.clear()

    del window
    del subwin
    del grid


def SpielStarten(ListeVonSpielern):

    currentSpielerIdx = 0
    nächsterSpielerIdx = 1

    while True:

        currentSpielerIdx = currentSpielerIdx % 2
        nächsterSpielerIdx %= 2

        currentSpieler = ListeVonSpielern[currentSpielerIdx]
        nächsterSpieler = ListeVonSpielern[nächsterSpielerIdx]

        # 'Der CurrentPlayer (Spieler der gerade spielt) schießt auf dem Feld vom nächsterSpieler (nächter Spieler)

        # Das Spielfeld vom anderen Spieler wird gezeigt
        SpielerFeld = nächsterSpieler.getField()

        # 'Feld im Zentrum des Fenster ausgeben, da Attribute 'alignment' von FeldZiehen
        # nicht weitergegeben wurde
        window, subwin, grid = FeldZiehen(
            SpielerFeld, footer='Geben Sie die Schusskoordinaten an: ')

        curses.echo()
        curses.curs_set(1)

        h, w = subwin.getmaxyx()

        SpielerLinks = ListeVonSpielern[0]
        SpielerRechts = ListeVonSpielern[1]

        subwin.addstr(1, 2, 'Spieler 1:')
        subwin.addstr(2, 2, SpielerLinks.getName())
        subwin.addstr(3, 2, 'Punktzahl: {}'.format(SpielerLinks.getPunktzahl()))

        # alle Schiffe durchlaufen und ausgeben
        for idx, (schiffId, schiff) in enumerate(SpielerLinks.getSchiffe().items()):
            subwin.addstr(
                idx+4, 2, 'Schiffs Id {} - Treffer {}/{}'.format(schiffId, schiff.Treffer, schiff.Größe))

        x = w - max(len(SpielerRechts.getName()), len('Schiffs Id 1 - Treffer 6/6'))

        subwin.addstr(1, x-2, 'Spieler 2:')
        subwin.addstr(2, x-2, SpielerRechts.getName())
        subwin.addstr(3, x-2, 'Punktzahl: {}'.format(SpielerRechts.getPunktzahl()))

        for idx, (schiffId, schiff) in enumerate(SpielerRechts.getSchiffe().items()):
            subwin.addstr(
                idx+4, x-2, 'Schiffs Id {} - Treffer {}/{}'.format(schiffId, schiff.Treffer, schiff.Größe))

        subwin.addstr(h-2, 2, '{} spielt gerade.'.format(currentSpieler.getName()))

        window.refresh()
        subwin.refresh()
        grid.refresh()

        w_height, w_width = window.getmaxyx()

        # prüfen ob ein Mensch oder Cpu dran ist
        if type(currentSpieler) == Spieler:
            # Falls Mensch, dann wird auf Eingabe des Benutzers gewartet
            goal = window.getstr(3).decode().strip().upper()
        else:
            # Falls Cpu dran ist
            # dann Schießziel wird zufällig ausgesucht
            goal = currentSpieler.Schießen(
                list(SpielerFeld.getPositions().keys()))

            NachrichtZeigen('CPU spielt gerade')

        window.clear()
        subwin.clear()
        grid.clear()

        # wird dazu verwendet, um zu wissen, ob ein Schoß gültig war
        Erfolg = False

        # prüfen ob Ziel gültig ist
        # 1. Bedingung:
        #  Länge des Zeilpunktes ist min 2 und max 3 Buchstaben
        if len(goal) in range(2, 4) and goal != curses.KEY_RESIZE:
            # 2. Bedingung:
            # Punktreferenz kommt im Spielfeld vor
            if goal in nächsterSpieler.getField().getPositions():
                # 3. Bedungung
                # Auf diesem Punkt wurde noch nie gespielt 
                if nächsterSpieler.getField().getValueByRef(goal) not in ['#', 'X']:
                    # es wird davon ausgegangen, dass kein Schif getroffen wurde
                    txt = 'VERFEHLT'

                    if nächsterSpieler.getField().getValueByRef(goal) == 'O':
                        # falls echt kein Schiff getroffen wurde
                        # dann Wert von diesem Punkt im Feld mit '#' ersetzen
                        nächsterSpieler.getField().setValueByRef(goal, '#')
                    else:
                        # falls ein Schif getroffen wurde
                        # 'Anzahl von Schläge dieses Schiffes inkeremtieren
                        nächsterSpieler.getField().getValueByRef(goal).gotdirektTreffer()
                        # Wert von diesem Punkt im Feld mit 'X' ersetzen
                        nächsterSpieler.getField().setValueByRef(goal, 'X')
                        # Wert von txt mit 'HIT' ersetzen, weil ein Schif getroffen wurde
                        txt = 'GETROFFEN'
                        # Punktzahl des Spielers, wer dran ist und ein Schiff vom Gegner getroffen hat,
                        # wird um 1 inkrementiert
                        currentSpieler.incrementPunktzahl()

                        # falls Cpu der Spieler ist, der dran ist
                        if type(currentSpieler) == Computer:
                            # Computer wird darauf hingewiesen, dass er ein Treffer in diesem Punkt hatte
                            # Sodass er beim nächsten Spiel in der Umgebung von diesem Platz spielt
                            currentSpieler.Erfolg(goal)

                    # Zeigen ob man ein Schiff getroffen hat oder nicht
                    window, subwin, grid = FeldZiehen(
                        nächsterSpieler.getField(), 'Drücken Sie eine Taste um fortzufahren')

                    h, w = subwin.getmaxyx()
                    subwin.addstr(h-2, 2, '{}'.format(txt))

                    # Um Änderungen zu sehen
                    window.refresh()
                    subwin.refresh()
                    grid.refresh()

                    # pausieren bis Benutzen reagiert
                    window.getch()

                    # 'Falls alle Bedingungen erfüllt wurden sind
                    # hinweisen dass Erfolgreiche Versuche durchgeführt wurden sind
                    Erfolg = True

        # Falls eine Versuch erfolgreich war
        if Erfolg == True:
            currentSpielerIdx = currentSpielerIdx + 1
            nächsterSpielerIdx += 1

        window.clear()
        subwin.clear()
        grid.clear()

        curses.noecho()
        curses.curs_set(0)

        del subwin
        del window
        del grid

        if SpielVorbei(nächsterSpieler.getSchiffe()):
            NachrichtZeigen('{} hat gewonnen !!'.format(currentSpieler.getName()))
            break


def SpielVorbei(SpielerSchiffe):
    # 'durchlauft alle Schiffe, die ein Spieler hat
    # 'und prüft ob alle zerstört sind
    for schiff in SpielerSchiffe.values():
        # falls nur ein Schiff noch nicht zerstört ist, dann Spiel soll weiter laufen
        if schiff.getStatus() == True:
            return False

    # Alle Schiffe vom Spieler sind zerstört
    # Game is Over
    return True


def SpielerVsSpieler():

    SpielerName = getSpielerName()

    # Spieler Objekt wird erzeugt
    spieler1 = Spieler(SpielerName)

    # Namen des 2. Spielers soll unterschiedlich von Namen des 1. Spielers sein
    while SpielerName == spieler1.getName():
        SpielerName = getSpielerName(2, 'Spieler 2 sollte anders heißen als Spieler 1. ')

    # Spieler Objekt wird erzeugt
    spieler2 = Spieler(SpielerName)

    # Spieler 1 soll seine Schiffe in seinem Field platzieren
    NachrichtZeigen('Spieler 1, wollen Sie Ihre Schiffe automatisch oder manuell platzieren?')
    choice = MenüAnzeigen(menu2)
    if choice == "automatisch":
        spieler1.SchiffePlatzierenAuto()
        NachrichtZeigen('Ihre Schiffe wurden platziert')
    elif choice == "manuell":
        NachrichtZeigen('Spieler 2, bitte weggucken')
        SchiffePlatzieren(spieler1)

    NachrichtZeigen('Spieler 2, wollen Sie Ihre Schiffe automatisch oder manuell platzieren?')
    choice = MenüAnzeigen(menu2)
    if choice == "automatisch":
        spieler2.SchiffePlatzierenAuto()
        NachrichtZeigen('Ihre Schiffe wurden platziert')
    elif choice == "manuell":
        NachrichtZeigen('Spieler 1, bitte weggucken')
        SchiffePlatzieren(spieler2)

    # startet das Spiel zwischen zwei Spieler
    SpielStarten([spieler1, spieler2])


def SpielerVsCpu():
    NachrichtZeigen('Sie wollen gegen den CPU spielen')
    
    SpielerName = getSpielerName()
    # einen Namen außer CPU und Computer aussuchen
    while SpielerName in ['CPU', 'COMPUTER']:
        SpielerName = getSpielerName(
            2, 'Spieler NAME sollte anders sein als. {}'.format(SpielerName))
    
    NachrichtZeigen('Wollen Sie Ihre Schiffe automatisch oder manuell platzieren?')
    spieler = Spieler(SpielerName)
    choice = MenüAnzeigen(menu2)
    if choice == "automatisch":
        spieler.SchiffePlatzierenAuto()
        NachrichtZeigen('Ihre Schiffe wurden platziert')
    elif choice == "manuell":
        SchiffePlatzieren(spieler)
    # Spieler Objekt erzeugen
    

    # Anzahl der Schiffe ist auf 6 festgelegt
    # Die Große des Feldes is automatisch 10x10

    # Spieler anfordern, die Schiffe in seinem Feld zu platzieren

    # Computer Object erzeugen
    cpu = Computer()

    # CPU den Befehl geben, die Schiffe in seinem Feld zu platzieren
    cpu.SchiffePlatzieren()

    window, subwin, grid = FeldZiehen(
        spieler.getField(), "Drücken Sie eine Taste um fortzufahren.", True, 'rechts')

    y = 1
    subwin.addstr(y, 1, 'Spieler: {} platziert seine Schiffe'.format(cpu.getName()))
    y+=1 
    subwin.addstr(y, 1, 'Drücken Sie eine Taste um fortzufahren')
    # Die For-Schleife unten wurde während Debuging benutzt, um
    # ' zu sehen, ob der CPU seine Schiffe korrekt im Feld positioniert hat
    # Bitte 'uncomment' die Zeilen um zu sehen

    # for schiff in cpu.getSchiffe().values():
    #     y += 1
    #     subwin.addstr(y, 1, 'Schiff name: {}, place: {}'.format(
    #         schiff.getName(), schiff.getPosition()))

    window.refresh()
    subwin.refresh()

    window.getch()

    subwin.clear()
    window.clear()

    SpielStarten([spieler, cpu])


def SpielBeenden():
    # Falls der Benutzer Exit aussucht, soll die untrige Nachricht angezeigt werden
    NachrichtZeigen('Sind Sie sicher, dass Sie das Spiel beenden wollen?')
    choice = MenüAnzeigen(menu3)
    if choice == "ja":
            # Spiel wird mit Exit Funktion beendet
        exit()
    elif choice == 'nein':
            # Spieler kehrt zum Hauptmenü zurück
        ()

def MenüAnzeigen(menuvar):

    currentIndex = 0

    while 1:

        # Erstellung von Zwei Window Objekte
        # Window hat Kopf- und Fußzeile
        window, subwin = DisplayErstellen()

        # Schreiben der Menuelemente vertikal ab der Zeile 1 und Spalte 1,
        # weil der Rand der Subwin die erste Zeile und Spalte besitzt

        for index, element in enumerate(menuvar):

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
        elif key == curses.KEY_DOWN and currentIndex < len(menuvar) - 1:
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

    return menuvar[currentIndex].lower()

def main(stdscr):

    #' blinkende Mousezeiger ausschalten
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)

    while 1:
        # unendliche Schleife, weil das Programm nur dann aufhören soll, wenn der Benutzer "Exit" auswählt

        # Diese Methode ermöglicht dem Benutzer einen Spielmodus auszuwählen
        # Der Rückgabewert (String) wird klein geschrieben
        choice = MenüAnzeigen(menu1)

        if choice == "spieler vs cpu":
            # Abruf der Methode, die für den "Spieler vs Cpu"-Spielmodus zuständig ist
            SpielerVsCpu()
        elif choice == 'spieler 1 vs spieler 2':
            # Abruf der Methode, die für den "Player1 vs Player2"-Spielmodus zuständig ist
            SpielerVsSpieler()
        elif choice == 'zurückkehren zu windows':
            # Abruf der Methode, die für das Beenden des Spieles zuständig ist
            SpielBeenden()

        


if __name__ == "__main__":
    # 'the wrapper() function takes a callable object and 
    # does the initializations described above, also initializing colors if 
    # color support is present. wrapper() then runs your provided callable. 
    # Once the callable returns, wrapper() will restore the original state of the terminal.
    curses.wrapper(main)
