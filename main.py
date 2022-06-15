from classes.spieler import Spieler
from classes.spieler import Computer
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
WILKOMMENS_FOOTER = 'Pfeiltasten zum navigieren benutzen | Entertaste zum auswählen benutzen'

menu1 = ['Spieler vs CPU', 'Spieler 1 vs Spieler 2', 'Schließe das Spiel']
menu2 = ['Automatisch', 'Manuell']
menu3 = ['Ja', 'Nein']

def MinFensterGröße():
    # Mindestgröße von Terminal wird User angezeigt
    msg = 'Min terminal Größe ist {} x {}'.format(MIN_WIDTH, MIN_HEIGHT)

    while 1:

        window = curses.initscr()
        window.clear()
        # x- und y-Achse der Terminalgröße wird  berechnt
        height, width = window.getmaxyx()
        # Mitte des Terminals berechnen
        y_pos, x_pos = max(height//2, 0), max(width//2 - len(msg)//2, 0)

        # Wenn Terminalgröße ausreichend ist, kann man Spiel ausführen
        if height >= MIN_HEIGHT and width >= MIN_WIDTH:
            break
        
        # Wenn die Mindestgröße nicht erreicht wurde,
        # wird in der Mitte des Terminals die Nachricht (msg) ausgegeben
        window.addstr(y_pos, x_pos, msg)
        window.refresh()
        window.getch()
        window.clear()
        del window

    window.clear()
    del window

    return True


def DisplayErstellen(header=WILKOMMENS_HEADER, footer=WILKOMMENS_FOOTER):
    # sicherstellen, dass Mindestgröße für Terminal erfüllt ist
    MinFensterGröße()

    # erstellt ein Window-Objekt, welches der ganzen Kommandozeile repräsentiert
    window = curses.initscr()

    # Ablesen der Höhe und Breite der Kommandozeile
    height, width = window.getmaxyx()

    # Kopfzeile steht ganz oben
    y_cor = 0
    # Kopfzeile soll mittig ausgegeben werden
    x_cor = width//2 - len(WILKOMMENS_HEADER)//2

    # Farbe 2(Schwarz auf Grün) wird eingeschaltet
    window.attron(curses.color_pair(2))
    # Kopfzeile wird in der Mitte ausgegeben
    window.addstr(y_cor, x_cor, WILKOMMENS_HEADER)

    # Farbe 2 (Schwarz auf Grün) wird ausgeschaltet
    window.attroff(curses.color_pair(2))

    # Fußzeile soll in der letzten Zeile, ganz unten, ausgegeben werden
    window.addstr(height-1, 0, footer)

    # Erstellen eines Fenster-Objekt, welches vom größten Window-Objekt abgeleitet wird
    # Sub win soll 2 Zeilen und 2 Spalten kleiner als das Window- Objekt sein
    subwin = window.derwin(height-2, width-2, 1, 1)
    subwin.box()
    # window und subwin werden zurückgeliefert
    return (window, subwin)


# diese Methode sorgt dafür, dass der vorher angegebene Text in der Mitte des Fenster ausgegeben wird
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

    # echo Methode wird eingeschaltet, sodass User sehen kann, was eingetippt wird
    curses.echo(1)
    # Mauszeiger wird eingeschaltet, sodass User sehen kann, wo eingetippt wird
    curses.curs_set(1)

    while 1:
        # zwei Fenster-Objekte werden erstellt
        window, subwin = DisplayErstellen(footer=footer)

        # gibt ein Tuple zurück (Höhe, Breite)
        height, width = window.getmaxyx()

        # String ab dem Punkt x,y=(1|1) im Subwin schreiben, welcher den Namen des Spielers zurückliefert
        subwin.addstr(
            1, 1, '{}Geben Sie einen Namen für Spieler {} an'.format(msg, spieler))

        # Aktualisierung des Fensters um Änderungen sehen zu können
        window.refresh()
        subwin.refresh()

        # Die Eingabe steht in der Fußzeile
        y = height-1
        # Da die Fußzeile schon beschriftet wurde, soll das Program
        # die Beschriftung ausweichen
        x = len(footer)

        # Alle Buchstaben (Zeichenkette) vor der Eingabe der Enter-Taste lesen
        name = window.getstr(y, x).decode().strip().upper()

        # Fenster-Objekte leer machen
        window.clear()
        subwin.clear()

        # Objekte werden gelöscht
        del window
        del subwin

        # Name des Users darf nicht leer sein
        # Schleife so lange laufen lassen, bis der eingegebene Name des Users gültig ist
        if len(name) > 0 and name != curses.KEY_RESIZE:
            break

    # echo wird ausgeschaltet
    curses.noecho()
    # Mauszeiger wird ausgeschaltet, nicht mehr sichtbar für User
    curses.curs_set(0)

    return name


# "Grafische Darstellung" des Spiels für den User wird in dieser Methode festgelegt
def FeldZiehen(SpielerFeld, footer, hideSchiffe=True, alignment='center'):

    # Erstellung von Window und Subwin
    window, subwin = DisplayErstellen(footer=footer)
    height, width = window.getmaxyx()
    h, w = subwin.getmaxyx()

    # Höhe und Breite von Feld wird festgelegt
    gridHeight = SpielerFeld.getHeight() * 2
    gridWidth = SpielerFeld.getWidth() * 4

    # wo das Feld im subwin platziert wird
    grid_begin_y = h//2 - gridHeight//2
    grid_begin_x = w//2 - gridWidth//2

    # wo das Feld im subwin platziert wird nach Abfrage links oder rechts
    if alignment.lower() == 'rechts':
        grid_begin_x = w - gridWidth - 2
    elif alignment.lower() == 'links':
        grid_begin_x = 2

    # Erstellung eines Feldes im sder
    grid = subwin.derwin(gridHeight, gridWidth, grid_begin_y, grid_begin_x)

    gridHeight, gridWidth = grid.getmaxyx()

    # Alle 4 Spalten beginnt von der 3. Spalte ein '|'
    for x in range(3, gridWidth - 1, 4):
        grid.vline(0, x, '|', gridHeight - 1)

    # Alle 2 Zeilen beginnt von der 1. Zeile ein '-'
    for y in range(1, gridHeight - 1, 2):
        grid.hline(y, 0, '-', gridWidth)

    # Die (erste) For-Schleife dient zur "Stelleneingabe" des Feldes
    # in jeder 4 Stelle soll die Referenz ausgegeben werden
    for x in range(0, gridWidth - 1, 4):
        for y in range(0, gridHeight - 1, 2):

            posRef = SpielerFeld.encodePosition(x//4, y//2)
            value = SpielerFeld.getValueByRef(posRef)

            # hideSchiffe == True
            # falls die Schiffe nicht im Feld angezeigt werden sollen
            if hideSchiffe:
                # ' während des Spiels werden die Positionen von den Schiffen nicht gezeigt
                # Referenz (zB: 'A10'), 'X' oder '#' wird ausgegeben, falls Treffer oder nicht
                txt = posRef
                if value in ['X', '#']:
                    txt = value

            # falls die Schiffe im Feld angezeigt werden sollen
            else:
                # falls kein Schiff vorliegt
                if value in ['O', 'X', '#']:
                    # Referenz ausgeben
                    txt = posRef

                # falls ein Schiff vorliegt
                else:
                    # Id zeigen
                    txt = value.getId()

            # 3 Plätze für txt reservieren
            # zB: 'A1' oder 'A10'
            grid.addstr(y, x, '%3s' % txt)
    
    # Feld in Farbe Grün ausgeben
    grid.bkgd(' ', curses.color_pair(2))

    return (window, subwin, grid)


def PositionsCheck(SpielerFeld, x, y):

    # diese Methode prüft, ob der Schusspunkt des Zieles im Feld liegt

    w = SpielerFeld.getWidth()
    h = SpielerFeld.getHeight()

    # Prüft ob X- und Y-Koordinaten im Spielfeld liegen
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
    # falls nein ist der Platz möglich und somit besetzbar
    return True


def checkSchiffsPlatz(SpielerFeld, start, end, Größe):

    # ob Start und Ende der Eingabe aus min 2 Buchstaben und max 3 Buchstaben bestehen
    # falls ja, nächste Bedingung überprüfen
    # falls nein, false zurückgeben
    if len(start) not in range(2, 4) or len(end) not in range(2, 4):
        return False

    # prüfen ob eine Platz-Referenz vorkommt, zB: A1 in ['A1','A3','C4']
    if start in SpielerFeld.getPositions() and end in SpielerFeld.getPositions():

        # Platzreferenz auf X- und Y-Koordinaten abbilden auf dem Feld
        start_x, start_y = SpielerFeld.decodePosition(start)
        end_x, end_y = SpielerFeld.decodePosition(end)

        # wenn es um eine Spalte geht, ist die X-Koordinate konstant
        if start_x == end_x:

            # sicherstellen, dass der kleinste Wert im Start und größte Wert im Ende steht
            if end_y < start_y:
                tmp = end_y
                end_y = start_y
                start_y = tmp

            # überprüfen ob der Platzbereich für ein Schiff ausreicht
            # 1 von Schiffsgröße substrahieren, weil wir von 0 anfangen
            if end_y - start_y == Größe - 1:
                for y in range(start_y, end_y + 1):
                    # überprüfen ob Plätze im Bereich frei oder besetzt sind
                    if(not PositionsCheck(SpielerFeld, start_x, y)):
                        return False
                return True

        # wenn es um eine Zeile geht, die Y-Koordinate ist konstant
        elif start_y == end_y:

            # sicherstellen, dass der kleinste Wert im Start und größte Wert im Ende steht
            if end_x < start_x:
                tmp = end_x
                end_x = start_x
                start_x = tmp

            # überprüfen ob der Platzbereich für ein Schiff ausreicht
            # 1 von Schiffsgröße substrahieren, weil wir von 0 anfangen
            if end_x - start_x == Größe - 1:
                for x in range(start_x, end_x + 1):
                    # überprüfen ob Plätze im Bereich frei oder besetzt sind
                    if not PositionsCheck(SpielerFeld, x, start_y):
                        return False
                return True
    # Falls keine Bedingung erfüllt wurde false
    return False
    

def SchiffePlatzieren(spieler):

    # echo Methode wird eingeschaltet, sodass User sehen kann, was eingetippt wird
    curses.echo()
    # Mauszeiger wird eingeschaltet, sodass User sehen kann, wo eingetippt wird
    curses.curs_set(1)

    # Schiffe vom Spieler in SpielerSchiffe speichern
    # Id des Schiffes und der Wert des Schiffes selbst werden in einem Python dict gespeichert

    SpielerSchiffe = spieler.getSchiffe().values()
    # alle Schiffe durchgehen
    for schiff in SpielerSchiffe:
        footer = 'Geben Sie die Position für das Schiff ein (bsp.: E4:E8 = von E4 bis E8): '

        while 1:
            # das aktualisierte Feld des Spielers abrufen und in SpielerFeld anzeigen
            SpielerFeld = spieler.getFeld()

            # das Spielfeld, wo der Spieler seine Schiffe plazieren kann, auf dem Bildschirm ausgeben
            window, subwin, grid = FeldZiehen(
                SpielerFeld, footer, False, 'rechts')

            # Größe von Kommandozeile ermitteln
            height, width = window.getmaxyx()

            # Schiffsdaten von Schiffen, welche platziert werden sollen, anzeigen 
            subwin.addstr(
                1, 1, 'Spieler: {}, platzieren Sie ihr Schiff im Feld.'.format(spieler.getName()))
            subwin.addstr(2, 1, 'Schiffs ID: {}'.format(schiff.getId()))
            subwin.addstr(3, 1, 'Schiffsname: {}'.format(schiff.getName()))
            subwin.addstr(4, 1, 'Schiffsgröße: {}'.format(schiff.getGröße()))

            window.refresh()
            subwin.refresh()
            grid.refresh()

            # Eingabe von höchstens 7 Buchstaben erlaubt
            coordinates = window.getstr(
                height - 1, len(footer), 7).decode().strip().upper()

            window.clear()
            subwin.clear()
            grid.clear()

            del grid
            del subwin
            del window

            # überprüfen ob der eingebene Text ':' beinhaltet und Mindestlänge 5 ist
            # falls ja nächste Bedingungen überprüfen
            # falls nein Fehlermeldung anzeigen
            if(':' in coordinates and len(coordinates) > 4):

                # Text ab dem ':' in 2 Teile teilen, der linke Teil ist der Start
                # und der rechte das Ende des Bereiches
                start, end = tuple(coordinates.split(':', 1))

                # prüfen ob die Bedingungen für Plazierung eingehalten wurden
                # falls ja, Schiff platzieren
                # falls nein, diese Platze ignorieren, und Fehlermeldung zeigen
                if checkSchiffsPlatz(SpielerFeld, start, end, schiff.getGröße()):

                    start_x, start_y = SpielerFeld.decodePosition(start)
                    end_x, end_y = SpielerFeld.decodePosition(end)
                    # sicherstellen, dass Ausgangspunkt kleiner ist als Endpunkt
                    if end_y < start_y:
                        tmp = end_y
                        end_y = start_y
                        start_y = tmp

                    if end_x < start_x:
                        tmp = end_x
                        end_x = start_x
                        start_x = tmp

                    # Plätze mit diesem Schiff belegen
                    for x in range(start_x, end_x + 1):
                        for y in range(start_y, end_y + 1):
                            # Wert des Platzes mit Schiff-Objekt ersetzen
                            spieler.getFeld().setValueByCor(x, y, schiff)
                            # Schiff mit besagter Id auf diesen Platz setzen
                            spieler.getSchiffe()[schiff.getId()].SchiffPlatzieren(
                                SpielerFeld.encodePosition(x, y))

                    break

            # Fehlermeldung, falls Eingabe falsch ist
            footer = 'Position ist nicht valide! Geben Sie die Position für das Schiff ein (bsp.: A1:A4 = von A1 bis A4): '

    curses.noecho()
    curses.curs_set(0)

    window, subwin, grid = FeldZiehen(
        spieler.getFeld(), "Drücken Sie eine Taste um fortzufahren.", True, 'rechts')

    y = 1
    subwin.addstr(y, 1, 'Spieler: {}'.format(spieler.getName()))

    # nach Eingabe Schiffe und ihre Positionen anzeigen
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

        # CurrentSpieler (Spieler der gerade spielt) schießt auf das Feld von nächsterSpieler (nächster Spieler)

        # Spielfeld von nächsterSpieler wird angezeigt
        SpielerFeld = nächsterSpieler.getFeld()

        # Feld in der Mitte des Fensters anzeigen, weil Attribut 'alignment' von FeldZiehen()
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

        # alle Schiffe durchlaufen und anzeigen
        for idx, (schiffId, schiff) in enumerate(SpielerLinks.getSchiffe().items()):
            subwin.addstr(
                idx+4, 2, 'Treffer {}/{} - {}'.format(schiff.Treffer, schiff.Größe, schiff.getName()))

        x = w - max(len(SpielerRechts.getName()), len('Treffer 6/6 - Schiffsname K-573 Нов'))

        subwin.addstr(1, x-2, 'Spieler 2:')
        subwin.addstr(2, x-2, SpielerRechts.getName())
        subwin.addstr(3, x-2, 'Punktzahl: {}'.format(SpielerRechts.getPunktzahl()))

        for idx, (schiffId, schiff) in enumerate(SpielerRechts.getSchiffe().items()):
            subwin.addstr(
                idx+4, x-2, 'Treffer {}/{} - {}'.format(schiff.Treffer, schiff.Größe, schiff.getName()))

        subwin.addstr(h-2, 2, '{} spielt gerade.'.format(currentSpieler.getName()))

        window.refresh()
        subwin.refresh()
        grid.refresh()

        w_height, w_width = window.getmaxyx()

        # Überprüfung, ob ein menschlicher Spieler oder der Computer dran ist
        if type(currentSpieler) == Spieler:
            # Wenn menschlicher Spieler dran ist, wird auf die Eingabe des Spielers gewartet
            goal = window.getstr(3).decode().strip().upper()
        else:
            # Wenn Computer dran ist, wird Schießziel zufällig ausgewählt
            goal = currentSpieler.Schießen(
                list(SpielerFeld.getPositions().keys()))

            NachrichtZeigen('CPU spielt gerade')

        window.clear()
        subwin.clear()
        grid.clear()

        # Abfrage ob Schuss gültig war
        Erfolg = False

        # Überprüfung der Gültigkeit des Zieles
        # 1. Bedingung:
        # Länge des Zielpunktes ist min 2 und max 3 Buchstaben lang
        if len(goal) in range(2, 4) and goal != curses.KEY_RESIZE:
            # 2. Bedingung:
            # Angabe des Punktes liegt im Spielfeld
            if goal in nächsterSpieler.getFeld().getPositions():
                # 3. Bedungung
                # besagter Punkt wurde noch nicht beschossen
                if nächsterSpieler.getFeld().getValueByRef(goal) not in ['#', 'X']:
                    # Annahme, dass kein Schiff getroffen wurde getroffen
                    # +Wert von txt mit 'VERFEHLT' besetzen, da kein Schiff getroffen wurde
                    txt = 'VERFEHLT'

                    if nächsterSpieler.getFeld().getValueByRef(goal) == 'O':
                        # wenn wirklich kein Schiff getroffen wurde
                        # wird Wert von diesem Punkt im Spielfeld mit '#' besetzt
                        nächsterSpieler.getFeld().setValueByRef(goal, '#')
                    else:
                        # wenn ein Schiff getroffen wurde
                        # Anzahl von Treffern auf dieses Schiffes erhöhen
                        nächsterSpieler.getFeld().getValueByRef(goal).gotdirektTreffer()
                        # wird Wert von diesem Punkt im Spielfeld mit 'X' besetzt
                        nächsterSpieler.getFeld().setValueByRef(goal, 'X')
                        # +Wert von txt mit 'GETROFFEN' besetzen, da ein Schiff getroffen wurde
                        txt = 'GETROFFEN'
                        # Punktzahl des Spielers, welcher dran ist und ein Schiff des Gegner getroffen hat,
                        # wird um 1 erhöht
                        currentSpieler.incrementPunktzahl()

                        # wenn Computer an der Reihe ist
                        if type(currentSpieler) == Computer:
                            # Computer wird darauf hingewiesen, auf welcher Position ein Treffer war
                            # Dadurch wird dieser beim nächsten Spielzug in diese Umgebung schießen
                            currentSpieler.Erfolg(goal)

                    # Zeigen ob ein Schiff getroffen wurde oder nicht
                    window, subwin, grid = FeldZiehen(
                        nächsterSpieler.getFeld(), 'Drücken Sie eine Taste um fortzufahren')

                    h, w = subwin.getmaxyx()
                    subwin.addstr(h-2, 2, '{}'.format(txt))

                    # Änderungen sichtbar
                    window.refresh()
                    subwin.refresh()
                    grid.refresh()

                    # pausieren bis User reagiert
                    window.getch()

                    # Wenn alle Bedingungen eingetroffen sind
                    # darauf hinweisen, dass erfolgreicher Versuch durchgeführt wurde
                    Erfolg = True

        # Wenn ein Versuch erfolgreich war
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
            NachrichtZeigen('{} hat gewonnen !!!'.format(currentSpieler.getName()))
            break


def SpielVorbei(SpielerSchiffe):
    # durchläuft alle Schiffe, die ein Spieler hat
    # und prüft ob alle zerstört wurdens
    for schiff in SpielerSchiffe.values():
        # wenn ein Schiff noch übrig ist, läuft Spiel weiter
        if schiff.getStatus() == True:
            return False

    # Ansonten, wenn alle Schiffe vom Spieler zerstört wurden, ist das Spiel vorbei
    return True


def SpielerVsSpieler():

    SpielerName = getSpielerName()

    # Spieler Objekt für Spieler1 wird generiert
    spieler1 = Spieler(SpielerName)

    # Namen des 2. Spielers sollte nicht wie der Name des 1. Spielers sein
    while SpielerName == spieler1.getName():
        SpielerName = getSpielerName(2, 'Spieler 2 sollte anders heißen als Spieler 1. ')

    # Spieler Objekt für Spieler2 wird generiert
    spieler2 = Spieler(SpielerName)

    # Spieler 1 wird gefragt, ob seine Schiffe in seinem Spielfeld automatisch oder manuell
    # platziert werden sollen
    NachrichtZeigen('Spieler 1, wollen Sie Ihre Schiffe automatisch oder manuell platzieren?')
    choice = MenüAnzeigen(menu2)
    # Schiffe werden automatisch platziert
    if choice == "automatisch":
        spieler1.SchiffePlatzierenAuto()
        NachrichtZeigen('Ihre Schiffe wurden platziert')
    # Schiffe werden manuell vom Spieler platziert
    elif choice == "manuell":
        NachrichtZeigen('Spieler 2, bitte weggucken')
        SchiffePlatzieren(spieler1)

    # Spieler 2 wird gefragt, ob seine Schiffe in seinem Spielfeld automatisch oder manuell
    # platziert werden sollen
    NachrichtZeigen('Spieler 2, wollen Sie Ihre Schiffe automatisch oder manuell platzieren?')
    choice = MenüAnzeigen(menu2)
    # Schiffe werden automatisch platziert
    if choice == "automatisch":
        spieler2.SchiffePlatzierenAuto()
        NachrichtZeigen('Ihre Schiffe wurden platziert')
    # Schiffe werden manuell vom Spieler platziert
    elif choice == "manuell":
        NachrichtZeigen('Spieler 1, bitte weggucken')
        SchiffePlatzieren(spieler2)

    # das Spiel zwischen den zwei Spielern beginnt
    SpielStarten([spieler1, spieler2])


def SpielerVsCpu():
    NachrichtZeigen('Sie wollen gegen den CPU spielen')
    
    SpielerName = getSpielerName()
    
    # Spieler Objekt wird erzeugt
    spieler = Spieler(SpielerName)

    # Name sollte nicht 'CPU' oder 'Computer' sein
    while SpielerName in ['CPU', 'COMPUTER']:
        SpielerName = getSpielerName(
            2, 'Spielername sollte nicht {} sein, da der Gegner so heißt. '.format(SpielerName))
    
    # Spieler wird gefragt, ob seine Schiffe in seinem Spielfeld automatisch oder manuell
    # platziert werden sollen
    NachrichtZeigen('Wollen Sie Ihre Schiffe automatisch oder manuell platzieren?')
    choice = MenüAnzeigen(menu2)
    # Schiffe werden automatisch platziert
    if choice == "automatisch":
        spieler.SchiffePlatzierenAuto()
        NachrichtZeigen('Ihre Schiffe wurden platziert')
    # Schiffe werden manuell vom Spieler platziert
    elif choice == "manuell":
        SchiffePlatzieren(spieler)

    
    # Computer Objekt wird erzeugt
    cpu = Computer()

    # CPU platziert automatisch Schiffe in seinem Spielfeld
    cpu.SchiffePlatzieren()

    window, subwin, grid = FeldZiehen(
        spieler.getFeld(), "Drücken Sie eine Taste um fortzufahren.", True, 'rechts')

    y = 1
    subwin.addstr(y, 1, 'Spieler: {} platziert seine Schiffe'.format(cpu.getName()))
    y+=1 
    subwin.addstr(y, 1, 'Drücken Sie eine Taste um fortzufahren')

    window.refresh()
    subwin.refresh()

    window.getch()

    subwin.clear()
    window.clear()

    # Spiel zwischen Spieler und Computer wird gestartet
    SpielStarten([spieler, cpu])


def SpielBeenden():
    # Wenn User Exit wählt, wir die untrige Abfrage angezeigt
    NachrichtZeigen('Sind Sie sicher, dass Sie das Spiel beenden wollen?')
    choice = MenüAnzeigen(menu3)
    if choice == "ja":
            # Spiel wird mit Exit Funktion beendet
        exit()
    elif choice == 'nein':
            # User kehrt zum Hauptmenü zurück
        ()

def MenüAnzeigen(menuvar):

    currentIndex = 0

    while 1:

        # Erstellung von Zwei Window Objekten
        # Window hat eine Kopf- und Fußzeile
        window, subwin = DisplayErstellen()

        # Menü-Elemente werden vertikal ab der 1. Zeile und 1. Spalte geschrieben,
        # da der Rand des Subwin die erste Zeile und Spalte einnimmt

        for index, element in enumerate(menuvar):

            # ein ausgewähltes Menü-Element soll mit der Farbe Schwarz auf Weiß angezeigt werden

            if index == currentIndex:
                # Farbe wird eingeschaltet
                subwin.attron(curses.color_pair(1))
                # ausgewältes Element in besagter Farbe anzeigen
                subwin.addstr(index + 1, 1, element)
                # Farbe wird ausgschaltet
                subwin.attroff(curses.color_pair(1))
            else:
                # nicht ausgewählte Menü-Elemente werden nicht in Farbe angezeigt
                subwin.addstr(index + 1, 1, element)

        # Aktualisierung um die Änderungen anzuzeigen
        window.refresh()
        subwin.refresh()

        # Eingabe des Users lesen
        key = window.getch()

        window.clear()
        subwin.clear()

        if key == curses.KEY_UP and currentIndex > 0:
            # Wenn der User eine der Pfeil-Tasten gedrückt hat
            # currentIndex inkrementieren solange das erste oder letzte Menü-Element nicht erreicht wurde
            currentIndex = currentIndex - 1
        elif key == curses.KEY_DOWN and currentIndex < len(menuvar) - 1:
            currentIndex = currentIndex + 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # Wemn der User die 'Enter-Taste' gedrückt hat
            window.clear()
            subwin.clear()

            window.refresh()
            subwin.refresh()

            break

    del subwin
    del window

    return menuvar[currentIndex].lower()

def main(stdscr):

    # Mauszeiger wird nicht angezeigt
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)

    while 1:
        # unendliche Schleife, da das Programm nur beendet werden soll, wenn der User "Exit" ausgewählt hat

        # User kann Spielmodus auswählen
        # Rückgabewert des Strings wird klein geschrieben
        choice = MenüAnzeigen(menu1)

        if choice == "spieler vs cpu":
            # Wenn "Spieler vs CPU"-Spielmodus ausgewählt wird Abruf von SpielerVsCpu()
            SpielerVsCpu()
        elif choice == 'spieler 1 vs spieler 2':
            # Wenn "Spieler 1 vs Spieler 2"-Spielmodus ausgewählt wird Abruf von SpielerVsSpieler()
            SpielerVsSpieler()
        elif choice == 'schließe das spiel':
            # Wenn "Schließe das Spiel" ausgewählt wurde, Spiel beenden mit SpielBeenden()
            SpielBeenden()

        


if __name__ == "__main__":
    # the wrapper() function takes a callable object and 
    # does the initializations described above, also initializing colors if 
    # color support is present. wrapper() then runs your provided callable. 
    # Once the callable returns, wrapper() will restore the original state of the terminal.
    curses.wrapper(main)
