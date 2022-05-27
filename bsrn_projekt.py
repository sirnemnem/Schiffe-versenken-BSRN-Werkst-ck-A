# -*- coding: utf-8 -*-
r"""
Modul, welches das Spiel Schiffe Versenken enthält.

Um das Spiel zu starten, muss der Befehl

python schiffe_versenken.py

ausgeführt werden. Hierbei müssen die Pfade zu python 
(z. B. C:\Python\python.exe) und zum Skript angepasst werden.

Um das Spiel abzubrechen, einfach die Konsole schließen oder CTRL + C
drücken. Um ein neues Spiel zu starten, muss das Skript neu gestartet werden.
"""

from enum import Enum
import numpy as np
import sys
import getopt

import os


def clear_console():
    """
    Hilfsfunktion, um die Konsole zu leeren.
    """
    os.system('cls' if os.name=='nt' else 'clear')
    

###############################################################################
# Enumerations                                                                #
###############################################################################


class Spielstatus(int, Enum):
    """
    Enumeration für den Spielstatus.
    """
    
    ZUG_SPIELER_1 = 1
    """
    Spieler 1 ist am Zug.
    """
    
    ZUG_SPIELER_2 = 2
    """
    Spieler 2 ist am Zug.
    """
    
    WARTE_SPIELER_1 = 4
    """
    Wartebildschirm vor Spieler 1 (nur für Spieler vs. Spieler). Ermöglicht
    es dem Spieler, der nicht dran ist, wegzuschauen.
    """

    WARTE_SPIELER_2 = 8
    """
    Wartebildschirm vor Spieler 2 (nur für Spieler vs. Spieler). Ermöglicht
    es dem Spieler, der nicht dran ist, wegzuschauen.
    """

    GAMEOVER = 16
    """
    Spiel ist zuende.
    """
    
    MODUS_SELECTION = 32
    """
    Spielmodus wird ausgewählt.
    """
    
    
class Spielmodus(int, Enum):
    """
    Enumeration für den Spielmodus.
    """
    
    SPIELER_V_COMPUTER = 1
    """
    Spieler gegen Computer. Spieler hat den ersten Zug.
    """
    
    SPIELER_V_SPIELER = 2
    """
    Spieler gegen Spieler.
    """

    EXIT = 3
    """
    Spiel beenden
    """

class Feldstatus(int, Enum):
    """
    Enumeration für den Status eines Feldes. Wird sowohl für das eigene
    als auch das gegnerische Feld verwendet.
    """
    
    LEER = 1
    """
    Leer unbesetzt (eigenes Feld) oder unbekannt (gegnerisches Feld).
    """
    
    SCHIFF_KEIN_TREFFER = 2
    """
    Auf dem Feld ist ein Schiff, welches noch nicht getroffen wurde (nur
    eigenes Feld).
    """
    
    SCHIFF_TREFFER = 4
    """
    Auf dem Feld ist ein Schiff, welches getroffen wurde (eigenes und
    gegnerisches Feld).
    """
    
    SCHUSS_DANEBEN = 8
    """
    Auf das Feld wurde geschossen, aber kein Treffer (eigenes Feld und
    gegnerisches Feld).
    """
    
    GESPERRT = 16
    """
    Feld ist gesperrt (da in einem Nachbarfeld ein Schiff beginnt oder
    endet, nur eigenes Feld).
    """
    
    @classmethod
    def get_char(cls, val, length=2):
        """
        Wandelt den Feldstatus in ein Zeichen um. Wird für die Darstellung
        verwendet.
        
        
        Parameters
        ----------
        val : Feldstatus
            Status, welcher dargestellt werden soll.
            
        length : int
            Anzahl der Zeichen, die zurückgegeben werden sollen. Damit kann 
            die Breite der Spalte gesteuert werden.
        """
        if(val == cls.LEER):
            # leeres Feld
            return length*" "
        elif(val == cls.SCHIFF_KEIN_TREFFER):
            # Schiff - noch nicht getroffen
            return length*"S"
        elif(val == cls.SCHIFF_TREFFER):
            # Schuss des Gegners
            return length*"X"
        elif(val == cls.GESPERRT):
            # Spielfeld gesperrt
            return length*"+"
        elif(val == cls.SCHUSS_DANEBEN):
            # Schuss daneben
            return length*"/"
        else:
            raise ValueError(f"Unknown value: {val}")

    
class ErgebnisSchuss(int, Enum):
    """
    Enumeration für das Ergebnis eines Schusses auf das gegnerische Feld.
    """
    
    DANEBEN = 1
    """
    Kein Treffer.
    """
    
    TREFFER = 2
    """
    Treffer, aber Schiff nicht versenkt.
    """
    
    VERSENKT = 4
    """
    Treffer und Schiff versenkt.
    """
    
    BEREITS_GESCHOSSEN = 8
    """
    Auf das Feld wurde bereits geschossen.
    """


###############################################################################
# Spielklassen                                                                #
###############################################################################
    

class Spielwelt():
    """
    Hauptklasse des Spiels. Hier wird die ganze Spiellogik gesteuert.
    
    
    Parameters
    ----------
    dim : tuple, (int, int)
        Dimensionen des Spielfeldes. Die Dimensionen werden hier nicht
        mehr geprüft (sondern nur in der main() Methode). Damit kann füt
        Testzwecke ein kleines Feld erstellt werden.
        
    laenge_schiffe : list of int
        Länge der Schiffe, welche gesetzt werden müssen. Die Namen der 
        Schiffe (U-Boot, Kreuzer, ...) werden in der Klasse :class:`Schiff`
        gesetzt.
    """

    
    def __init__(self, dim, laenge_schiffe):
        self.dim = dim
        """
        Dimensionen des Spielfeldes.
        """
        
        self.laenge_schiffe = laenge_schiffe
        """
        Länge der Schiffe.
        """
        
        self.spielstatus = Spielstatus.MODUS_SELECTION
        """
        Aktueller Spielstatus. Definiert die Anzeige auf dem Bildschirm.
        """
        
        clear_console()

    
    def reset(self, spielmodus):
        """
        Setzt die Spielwelt zurück und startet ein neues Spiel - abhängig
        vom Spielmodus.
        
        
        Parameters
        ----------
        spielmodus : Spielmodus
            Spielmodus, in welchem das Spiel gestartet werden soll.
        """
        
        # 1. Definiere Variablen abhängig vom Spielmodus
        if(spielmodus == Spielmodus.SPIELER_V_COMPUTER):
            ist_computer1 = False
            ist_computer2 = True
            
            name1 = "Spieler"
            name2 = "Computer"

        elif(spielmodus == Spielmodus.SPIELER_V_SPIELER):
            ist_computer1 = False
            ist_computer2 = False

            name1 = "Spieler 1"
            name2 = "Spieler 2"

        elif(spielmodus == Spielmodus.EXIT):
            ist_computer1 = False
            ist_computer2 = False

            name1 = "Spieler 1"
            name2 = "Spieler 2"
            
        else:
            raise ValueError(f"Unbekannter Wert für spielmodus: {spielmodus}")

        
        # 2. Erzeuge Spieler
        # 2.1. Erzeuge Spieler 1 (beginnt immer)
        self.spieler1 = Spieler(name=name1,
            ist_computer=ist_computer1, dim=self.dim, 
            laenge_schiffe=self.laenge_schiffe)
        
        # 2.2. Erzeuge Spieler 2 (beginnt immer)
        self.spieler2 = Spieler(name=name2,
            ist_computer=ist_computer2, dim=self.dim, 
            laenge_schiffe=self.laenge_schiffe)
        
        # 3. Setze Schiffe
        # 3.1. Falls Spieler gegen Spieler: gebe Spieler 2 Möglichkeit 
        # wegzuschauen. Falls Spiel gegen Computer, nicht notwendig
        if(spielmodus == 3):
            clear_console()
            
            print("Spieler 1 gibt nun die Positionen der Schiffe an.")
            print("Spieler 2 bitte wegschauen.")
            print("Zum Fortfahren Enter drücken...")
            input()
        
        # 3.2. Spieler 1 setzt Schiffe. Falls Spieler 1 Computer ist, werden
        # die Schiffe automatisch gesetzt.
        self.spieler1.platziere_schiffe()
        
        # 3.3. Falls Spieler gegen Spieler: gebe Spieler 1 Möglichkeit
        # wegzuschauen. Falls Spiel gegen Computer, nicht notwendig
        if(spielmodus == 3):
            clear_console()
            
            print("Spieler 2 gibt nun die Positionen der Schiffe an.")
            print("Spieler 1 bitte wegschauen.")
            print("Zum Fortfahren Enter drücken...")
            input()
        
        # 3.4. Spieler 2 setzt Schiffe. Falls Spieler 2 Computer ist,
        # werden Schiffe automatisch gesetzt.
        self.spieler2.platziere_schiffe()
        
        # 4. Setzte aktuellen Spieler. Spieler 1 beginnt immer.
        self.aktueller_spieler = 1
        if(spielmodus == 3):
            # Falls Spieler gegen Spieler: gebe Spieler 2 die Möglichkeit
            # wegzuschauen
            self.spielstatus = Spielstatus.WARTE_SPIELER_1
        else:
            self.spielstatus = Spielstatus.ZUG_SPIELER_1
        

    def start(self):
        """
        Startet das Spiel. Hauptschleife.
        """
        
        # Schleife wird bis zum Abbruch fortgeführt.
        while(self.spielstatus is not Spielstatus.GAMEOVER):
            # 1. Prüfe Modus Auswahl des Spiels
            if(self.spielstatus == Spielstatus.MODUS_SELECTION):
                # 1.1. Eingabe vom Benutzer
                print("Wilkommen bei Schiffe Versenken.")
                print()
                print("Bitte Modus auswählen!")
                print()
                print("{} - Spieler vs. Computer".format(Spielmodus.SPIELER_V_COMPUTER))
                print("{} - Spieler vs. Spieler".format(Spielmodus.SPIELER_V_SPIELER))
                print()
                spielmodus = input("Spielmodus: ")
                
                # 1.2. Verarbeite Eingabe - Wandle in Integer um
                try:
                    spielmodus = int(spielmodus)
                    
                except Exception():
                    clear_console()
                    print("Ungültige Eingabe!")
                    
                # 1.3. Prüfe, ob gültiger Modus eingegeben wurde.
                if(spielmodus not in [1, 2, 3]):
                    clear_console()
                    print("Ungültige Eingabe!")
                    
                # 1.4. Eingabe ok, starte Spiel
                self.reset(spielmodus=spielmodus)
                
            
            # 2. Definiere für den aktuellen Zug den Spieler und den Gegner.
            if(self.aktueller_spieler == 1):
                spieler = self.spieler1
                gegner = self.spieler2
                i_spieler = 1
                i_gegner = 2
                zeichenmodus = 2
            else:
                spieler = self.spieler2
                gegner = self.spieler1
                i_spieler = 2
                i_gegner = 1
                zeichenmodus = 4

            # 3. Zeige Wartebildschirm, damit der Spieler, welcher nicht 
            # am Zug ist, wegschauen kann.
            if(self.spielstatus in [Spielstatus.WARTE_SPIELER_1, 
                                    Spielstatus.WARTE_SPIELER_2]):
                # 3.1. Zeige Wartebildschirm
                clear_console()
                print("Spieler {} ist am Zug. Spieler {} bitte wegschauen."
                      .format(i_spieler, i_gegner))
                print("Zum Fortfahren Enter drücken...")
                input()
                
                # 3.2. Setze Spielstatus
                clear_console()
                
                if(self.aktueller_spieler == 1):
                    self.spielstatus = Spielstatus.ZUG_SPIELER_1
                else:
                    self.spielstatus = Spielstatus.ZUG_SPIELER_2
            
            # 4. Führe Zug durch
            if(spieler.ist_computer):
                # 4.1. Spieler ist Computer - Führe automatischen Zug durch
                
                # 4.1.1. Suche Schussposition
                zeile, spalte = spieler.suche_schusspos_auto()
                
                # 4.1.2. Ermittle Ergebnis des Schusses
                res, xy_status_list = (
                    gegner.ergebnis_schuss_auf_eigen(zeile, spalte))
                
                # 4.1.3. Update Felder
                spieler.update_feld(xy_status_list, eigenes_feld=False)
                gegner.update_feld(xy_status_list, eigenes_feld=True)
                
            else:
                # 4.2. (Menschlicher) Spieler ist am Zug
                clear_console()
                
                print("Spieler {} ist an der Reihe".format(self.aktueller_spieler))
                print()
                
                # 4.2.1. Zeige aktuelles Spielfeld
                spieler.zeichne(zeichenmodus)
                
                # 4.2.2. Zeige Statistik
                a1, a2 = spieler.get_statistik()
                a3, a4 = gegner.get_statistik()
                print()
                print('--------------------------------------')
                print("Statistik eigene Schiffe:")
                print("..Versenkt:       {}".format(a1))
                print("..Nicht Versenkt: {}".format(a2))
                print("Statistik gegnerische Schiffe:")
                print("..Versenkt:       {}".format(a3))
                print("..Nicht Versenkt: {}".format(a4))
                print('--------------------------------------')
                print()
                
                # 4.2.3. Spieler gibt Position ein, wo Schuss gesetzt werden
                # soll
                anzahl_zeilen = spieler.dim[0]
                anzahl_spalten = spieler.dim[1]
                
                i_col = input("Spalte eingeben: ")
                i_row = input("Zeile eingeben: ")
                
                # 4.2.4. Prüfe, ob Eingabe gültig ist
                # Prüfe, ob integer Werte eingegeben wurden
                try:
                    i_col = int(i_col)
                    i_row = int(i_row)
                except Exception:
                    clear_console()
                    print("Ungültige Eingabe")
                    print("Zum Wiederholen Enter drücken...")
                    input()
                    continue
                
                # prüfe, ob valider Bereich angegeben wurde
                # python ist 0-Index-Basiert
                if(not (0 <= i_row < anzahl_zeilen)
                    or not (0 <= i_col < anzahl_spalten)):
                    print("Ungültige Eingabe")
                    print("Zum Wiederholen Enter drücken...")
                    input()
                    continue
                
                # 4.2.5. Ermittle Ergebnis des Schusses
                res, xy_status_list = (
                    gegner.ergebnis_schuss_auf_eigen(i_row, i_col))
                
                # 4.2.6. Zeige Ergebnis auf dem Bildschirm
                if(res == ErgebnisSchuss.BEREITS_GESCHOSSEN):
                    print("Ergebnis des Feldes bereits bekannt!")
                    print("Zum Wiederholen Enter drücken...")
                    input()
                    continue
                elif(res == ErgebnisSchuss.TREFFER):
                    print("Treffer!")
                elif(res == ErgebnisSchuss.DANEBEN):
                    print("Daneben!")
                elif(res == ErgebnisSchuss.VERSENKT):
                    print("Versenkt!")
                
                # 4.2.7. Update Felder
                spieler.update_feld(xy_status_list, eigenes_feld=False)
                gegner.update_feld(xy_status_list, eigenes_feld=True)
                
                # 4.2.8. Pausiere Programm, damit Spieler das Ergebnis 
                # lesen kann
                print("Zum Fortfahren Enter drücken...")
                input()
            
            # 5. Prüfe. ob Gegner alle Schiffe versenkt hat
            if(gegner.alle_eigenen_schiffe_versenkt()):
                clear_console()
                
                print("Spieler {} hat gewonnen!".format(self.aktueller_spieler))
                self.spielstatus = Spielstatus.GAMEOVER
                
                print()
                print("Feld Spieler 1")
                self.spieler1.zeichne(modus=1)
                print()
                print("Feld Spieler 2")
                self.spieler2.zeichne(modus=1)
                
                print("Zum Fortfahren Enter drücken...")
                input()
                
                # Spiel ist vorbei. Beende ausführung des Programms.
                # Alternativ: setze self.spielstatus auf
                # Spielstatus.MODUS_SELECTION, um von vorne zu beginnen
                return
            
            # 6. Setze nächsten Spieler
            if(self.aktueller_spieler == 1):
                self.aktueller_spieler = 2
                
                # falls Spieler vs Spieler: Wartebildschirm
                if(self.spieler1.ist_computer or self.spieler2.ist_computer):
                    self.spielstatus = Spielstatus.ZUG_SPIELER_2
                else:
                    self.spielstatus = Spielstatus.WARTE_SPIELER_2
            
            else:
                self.aktueller_spieler = 1
        
                # falls Spieler vs Spieler: Wartebildschirm
                if(self.spieler1.ist_computer or self.spieler2.ist_computer):
                    self.spielstatus = Spielstatus.ZUG_SPIELER_1
                else:
                    self.spielstatus = Spielstatus.WARTE_SPIELER_1

    
class Spieler():
    """
    Klasse für den Spieler. Diese Klasse deckt sowohl einen menschlichen
    Spieler als auch einen Computerspieler ab.
    
    Parameters
    ----------
    ist_computer : bool
        Definiert, ob es ein menschlicher oder Computer-Spieler ist.
        Wenn ``True``, dann ist es ein Computer, sont ein menschlicher 
        Spieler.
        
    dim : tuple, (int, int)
        Dimensionen des Spielfeldes.
        
    laenge_schiffe : list of int
        Liste der Schiffslängen.
        
    name : str
        Beliebiger Name des Spielers. Wird für die Anzeige benötigt.
    """
    
    def __init__(self, ist_computer, dim, laenge_schiffe, name):
        
        # 1. Speichere Attribute
        self.ist_computer = ist_computer
        """
        Coputer oder Mensch.
        """
        
        self.dim = dim
        """
        Dimensionen des Spielfeldes
        """
        
        self.spielfeld_eigen = np.zeros(dim, dtype=int) + Feldstatus.LEER
        """
        Eigenes Spielfeld. Status vollständig bekannt.
        """
        
        self.spielfeld_gegner = np.zeros_like(self.spielfeld_eigen) + Feldstatus.LEER
        """
        Gegnerisches Spielfeld. Nur die Felder bekannt, auf die geschossen
        wurde (und die sich automatisch ergeben).
        """
        
        self.name = name
        """
        Name des Spielers.
        """
        
        # 2. Erzeuge Schiffe (Position wird später festgelegt)
        self.schiff_liste = []
        """
        Liste der Schiffe.
        """
        for laenge in laenge_schiffe:
            schiff = Schiff(laenge)
            self.schiff_liste.append(schiff)
            
    def platziere_schiffe(self):
        """
        Methode zum Platzieren der Schiffe.
        """
        
        if(self.ist_computer):
            self._platziere_schiffe_auto()
        else:
            self._platziere_schiffe_manuell()
        
    def _platziere_schiffe_auto(self):
        """
        Methoden zum automatischen Platzieren der Schiffe.
        """
        
        # 1. Ermittle Anzahl der Zeilen und Spalten
        anzahl_zeilen = self.dim[0]
        anzahl_spalten = self.dim[1]

        # 2. iteriere über jedes Schiff.
        for schiff in self.schiff_liste:
            valide_position = False
            
            # 2.1. Führe Schleife so lange durch, bis valide Position 
            # gefunden wurde
            while(not valide_position):
                # 2.1.1. erzeuge zufällige position und Orientierung
                x0 = np.random.randint(0, anzahl_zeilen, 1)
                y0 = np.random.randint(0, anzahl_spalten, 1)
                ist_waagerecht = np.random.randint(0, 2, 1, dtype=bool)
                
                # 2.1.2. Setze Eigenschaften
                schiff.setze_pos(x0, y0, ist_waagerecht)
                
                # 2.1.3. Prüfe, ob Position valide ist
                if(schiff.pruefe_position(self.spielfeld_eigen)):
                    # 2.1.4. Position ok, fülle das Spielfeld
                    schiff.setze_schiff(self.spielfeld_eigen)
                    valide_position = True
        
    def _platziere_schiffe_manuell(self):
        """
        Methode zum manuellen Platzieren der Schiffe.
        """
        
        # 1. Frage, ob manuelle oder automatische Platzierung
        clear_console()
        
        print()
        print("{} platziert Schiffe".format(self.name))
        
        print()
        res = input("Manuell (0) | Automatisch (1): ")
        
        # 2. Setze Schiffe
        if(res == "1"):
            # 2.1. Automatisches Setzen
            self._platziere_schiffe_auto()
            return
        
        
        for schiff in self.schiff_liste:
            # 2.2. Manuelles Setzen
            valide_position = False
            
            clear_console()
            
            # 2.2.1. Iteriere über jedes Schiff
            while(not valide_position):
                print("{} platziert Schiffe".format(self.name))
                print()
                
                # 2.2.1.1. Zeichen aktuelles Spielfeld (nur eigenes Spielfeld)
                self.zeichne(modus=1)
                
                # 2.2.1.2. Zeige Infos zum aktuellen Schiff
                schiff_name = schiff.get_name()
                
                print()
                print("Platziere {} (Länge {})".format(schiff_name, schiff.laenge))
                print()
                
                # 2.2.1.3. Nutzer gibt Position und Orientierung an
                i_col = input("Spalte eingeben: ")
                i_row = input("Zeile eingeben: ")
                ist_waagerecht = input("Ist Senkrecht (0) | Ist Waagerecht (1): ") == "1"
                
                # 2.2.1.4. Prüfe, ob Eingaben valide waren
                # Überprüfung auf korrekten Bereich wird im Schiff
                # durchgeführt
                try:
                    i_col = int(i_col)
                    i_row = int(i_row)
                except Exception:
                    print("Invalide Position. Neu Eingeben!")
                    print(ist_waagerecht)
                    valide_position = False
                    continue
                    
                # 2.2.1.5. Setze Position
                schiff.setze_pos(i_row, i_col, ist_waagerecht)
                
                # # 2.2.1.6. Prüfe, ob Position valide ist
                if(schiff.pruefe_position(self.spielfeld_eigen)):
                    # Position ist valide, speichere Position
                    schiff.setze_schiff(self.spielfeld_eigen)
                    valide_position = True
                    
                else:
                    # Position invalide
                    # Mögliche Gründe:
                    #  - Überlappung zu bereits vorhandenen Schiffen
                    #  - Schiff geht über Rand hinaus
                    clear_console()
                    print("Invalide Position. Neu Eingeben!")
                    valide_position = False
    
    def zeichne(self, modus):
        """
        Methode zum Zeichnen des Spielfeldes.
        
        
        Parameters
        ----------
        modus : int
            Modus für das Zeichnen. Mögliche Werte sind:
                - 1: nur eigenes Spielfeld wird gezeichnet.
                - 2: eigenes Spielfeld wird links gezeichnet, Spielfeld
                     des Gegners rechts (für Spieler 1)
                - 3: eigenes Spielfeld wird rechts gezeichnet, Spielfeld
                     des Gegners links (für Spieler 2)
        """
        
        # 1. Bereite Variablen vor
        anzahl_zeilen = self.dim[0]
        anzahl_spalten = self.dim[1]
        
        if(modus == 1):
            spielfeld_links = self.spielfeld_eigen
            spielfeld_rechts = None
            
        elif(modus == 2):
            spielfeld_links = self.spielfeld_eigen
            spielfeld_rechts = self.spielfeld_gegner
            s_left = "Eigenes Feld"
            s_right = "Gegner"
        
        elif(modus == 4):
            spielfeld_links = self.spielfeld_gegner
            spielfeld_rechts = self.spielfeld_eigen
            s_left = "Gegner"
            s_right = "Eigenes Feld"
            
        else:
            raise ValueError("Unbekannter Modus.")
        
        
        # Trennzeichen zwischen den Spielfeldern
        s_delim = "    H    "
        
        # Trenner einer Tabellenreihe
        s_tabellenreihe = "  " + (3*anzahl_spalten + 1) * "-"
        laenge1 = len(s_tabellenreihe)
        if(modus in [2, 4]):
            s_tabellenreihe = s_tabellenreihe + s_delim + (3*anzahl_spalten + 1) * "-"
        
        # 2. Zeichne
        # 2.1. Zeiche Überschrift
        if(modus in [2,4]):
            s_format = "{:<" + str(laenge1) + "}"
            s_top = s_format.format(s_left) + s_delim + s_format.format(s_right)
            print(s_top)
        
        # 2.2. Zeichne erste Zeile, wo die Spaltennummern stehen
        s = "  "
        for i_col in range(anzahl_spalten):
            s = s + "|{:02d}".format(i_col)
        s = s + "|" 
        if(modus in [2, 4]):
            s = s + s_delim  
            for i_col in range(anzahl_spalten):
                s = s + "|{:02d}".format(i_col)
            s = s + "|" 
        print(s)
        
        # 2.3. Zeichne Reihen
        for i_row in range(anzahl_zeilen):
            # 2.3.1. Zeichne Trenner
            print(s_tabellenreihe)
            
            # 2.3.2. Zeichne Reihe
            s = "{:02d}".format(i_row)
            for i_col in range(anzahl_spalten):
                val = spielfeld_links[i_row, i_col]
                s_tmp = Feldstatus.get_char(val)
                
                s = s + "|" + s_tmp
            s = s + "|"
            
            # rechtes Feld wird nur für Modus 2, 4 benötigt
            if(modus in [2, 4]):
                s = s + s_delim
                for i_col in range(anzahl_spalten):
                    val = spielfeld_rechts[i_row, i_col]
                    s_tmp = Feldstatus.get_char(val)
                    
                    s = s + "|" + s_tmp
                s = s + "|"
            print(s)
        
        # 2.4. Zeichne abschließenden Trenner
        print(s_tabellenreihe)
            
    def ergebnis_schuss_auf_eigen(self, zeile, spalte):
        """
        Ermittelt das Ergebnis, wenn auf das eigene Feld geschossen wird.
        Eingegebene Position muss valide sein, wird hier nicht geprüft.
        
        Parameters
        ----------
        zeile : int
            Zeile. 
            
        spalte : int
            Spalte.
            
            
        Returns
        -------
        res : ErgebnisSchuss
            Ergebnis des Schusses
            
        update_pos : list
            Positionen, die geupdated werden müssen mit dem entsprechenden
            Wert. Die Liste ist eine Liste von Tupeln, wobei jedes Tupel
            aus den Einträgen (Zeile, Spalte, Status) besteht.
        """
        
        # 1. Prüfe, ob auf Position bereits geschossen wurde
        if(self.spielfeld_eigen[zeile, spalte] in 
           [Feldstatus.SCHIFF_TREFFER, Feldstatus.SCHUSS_DANEBEN]):
            #print("Bereits darauf geschossen.")
            return ErgebnisSchuss.BEREITS_GESCHOSSEN, []
        
        # 2. Prüfe, ob bei einem Schiff ein Treffer gelandet wurde
        for schiff in self.schiff_liste:
            treffer_schiff = schiff.setze_schuss(zeile, spalte)
            
            # 2.1. Treffer gelandet
            if(treffer_schiff):
                # 2.1.1. Prüfe, ob Schiff versenkt wurde.
                versenkt = schiff.ist_versenkt()
                
                if(versenkt):
                    # 2.1.1.1. Schiff wurde versenkt
                    
                    # ermittle Koordinaten
                    res = []
                    
                    koordinaten_schiff = schiff.get_koordinaten_schiff()
                    koordinaten_rand = schiff.get_koordinaten_gesperrt()
                    
                    # Schiffskoordinaten werden alle auf SCHIFF_TREFFER gesetzt
                    for i in range(len(koordinaten_schiff)):
                        x_tmp = koordinaten_schiff[i][0]
                        y_tmp = koordinaten_schiff[i][1]
                        res.append((x_tmp, y_tmp, Feldstatus.SCHIFF_TREFFER))
                        
                    # Randkoordinaten werden auf SCHUSS_DANEBEN gesetzt,
                    # da sich dort kein Schiff befinden kann
                    for i in range(len(koordinaten_rand)):
                        x_tmp = koordinaten_rand[i][0]
                        y_tmp = koordinaten_rand[i][1]
                        res.append((x_tmp, y_tmp, Feldstatus.SCHUSS_DANEBEN))
                        
                    return ErgebnisSchuss.VERSENKT, res
                else:
                    # 2.1.1.2. Schiff wurde nur getroffen. Update nur
                    # das Feld, auf welches geschossen wurde.
                    return (ErgebnisSchuss.TREFFER, 
                            [(zeile, spalte, Feldstatus.SCHIFF_TREFFER)])
        
        #print("Daneben!")
        return ErgebnisSchuss.DANEBEN, [(zeile, spalte, Feldstatus.SCHUSS_DANEBEN)]
    
    def update_feld(self, xy_status_list, eigenes_feld):
        """
        Methode zum updaten von einem Feld.
        
        
        Parameters
        -----------
        xy_status_list : list
            Liste der Felder, welche geupdaten werden müssen. Siehe 
            :meth:`ergebnis_schuss_auf_eigen`. Einträge der List sind Tupel
            mit den Einträgen (zeile, spalte, Status).
            
        eigenes_feld : bool
            Wenn ``True``, wird das eigene Feld aktualisiert, ansonsten
            das gegnerische.
        """
        
        # 1. Ermittle das Feld zum aktualisieren
        if(eigenes_feld):
            spielfeld = self.spielfeld_eigen
        else:
            spielfeld = self.spielfeld_gegner
        
        # 2. update Feld
        for (zeile, spalte, status) in xy_status_list:
            if(0 <= zeile < self.dim[0]
               and 0 <= spalte < self.dim[1]):
                spielfeld[zeile, spalte] = status
                
    def suche_schusspos_auto(self):
        """
        Methode zum Suchen einer Position, auf welche geschossen werden soll.
        
        
        Returns
        -------
        pos : tuple
            Position ((zeile, spalte)), auf welche geschossen werden soll.
        """
        
        # 1. Speichere Hilfsvariablen
        spielfeld = self.spielfeld_gegner
        pos = None
        
        anzahl_zeilen = spielfeld.shape[0]
        anzahl_spalten = spielfeld.shape[1]
        
        # 2. suche nach leerem Feld in der Nähe von Treffern
        for i_row in range(anzahl_zeilen):
            for i_col in range(anzahl_spalten):
                status = spielfeld[i_row, i_col]

                if(status == Feldstatus.SCHIFF_TREFFER):
                    
                    # 2.1 prüfe Feld links / rechts / oben / unten vom Treffer
                    koordinaten = []
                    koordinaten.append((i_row, i_col - 1))
                    koordinaten.append((i_row, i_col + 1))
                    koordinaten.append((i_row - 1, i_col))
                    koordinaten.append((i_row + 1, i_col))
                    
                    for x_tmp, y_tmp in koordinaten:
                        # 2.2. prüfe, ob Index valide ist und Feld leer ist
                        if(0 <= x_tmp < anzahl_zeilen
                           and 0 <= y_tmp < anzahl_spalten
                           and spielfeld[x_tmp, y_tmp] == Feldstatus.LEER):
                            # 2.3. Feld ist leer, wird für Schuss genommen
                            pos = (x_tmp, y_tmp)
                            break
                    
                # Position gefunden, beende innere Schleife    
                if(pos is not None):
                    break
                    
            # Position gefunden, beende äußere Schleife
            if(pos is not None):
                break
                    
        # 3. keine leeres Feld in der Näche von Treffern gefunden
        # wähle zufälliges Feld aus
        while(pos is None):
            x_tmp = np.random.randint(anzahl_zeilen)
            y_tmp = np.random.randint(anzahl_spalten)
            
            if(spielfeld[x_tmp, y_tmp] == Feldstatus.LEER):
                pos = (x_tmp, y_tmp)
        
        return pos
    
    def alle_eigenen_schiffe_versenkt(self):
        """
        Prüft, ob alle eigenen Schiffe versenkt sind.
        
        
        Returns
        -------
        res : bool
            ``True``, wenn alle eigenen Schiffe versenkt wurden,
            ansonsten ``False``.
        """
        
        for schiff in self.schiff_liste:
            if(not schiff.ist_versenkt()):
                # mindestens ein Schiff ist nicht versenkt
                return False
            
        return True
        
    
    def get_statistik(self):
        """
        Gibt die Anzahl der versenkten und noch zu versenkenden Schiffe
        zurück.
        
        
        Returns
        -------
        anzahl_versenkt : int
            Anzahl der bereits versenkten Schiffe
            
        anzahl_nicht_versenkt : int
            Anzahl der noch nicht versenkten Schiffe
        """
        anzahl_versenkt = 0
        
        for schiff in self.schiff_liste:
            if(schiff.ist_versenkt()):
                anzahl_versenkt += 1
                
        anzahl_nicht_versenkt = len(self.schiff_liste) - anzahl_versenkt
        return anzahl_versenkt, anzahl_nicht_versenkt
        

class Schiff():
    """
    Klasse für Schiff.
    
    
    Parameters
    ----------
    laenge : int
        Länge des Schiffs.
    """
    
    def __init__(self, laenge):
        self.laenge = laenge
        """
        Länge des Schiffs.
        """
        
        self.treffer = np.zeros(laenge, dtype=bool)
        """
        Numpy array für das Schiff. Wenn ein Feld ``True`` ist, 
        dann wurde dieses Feld des Schiffes getroffen.
        """

        self.zeile0 = None
        """
        Zeile des Feldes links / oben.
        """
        
        self.spalte0 = None
        """
        Spalte des Feldes links / oben.
        """
        
        self.ist_waagerecht = None
        """
        Orientierung.
        """

        
    def setze_pos(self, zeile0, spalte0, ist_waagerecht):
        """
        Setzt die Position und Orientierung des Schiffes.
        
        
        Parameters
        ----------
        zeile0 : int
            Zeile des Feldes links / oben.
            
        spalte0 : int
            Spalte des Feldes links / oben
            
        ist_waagerecht : bool
            Orientierung. Wenn ``True``, dann liegt das Schiff waagerecht,
            ansonsten senkrecht.
        """
        
        self.zeile0 = zeile0
        self.spalte0 = spalte0
        self.ist_waagerecht = ist_waagerecht
        
    def setze_schuss(self, zeile, spalte):
        """
        Prüft, ob der Schuss das Schiff getroffen hat. Aktualisiert das
        entsprechende Feld.
        
        
        Parameters
        ----------
        zeile : int
            Zeile, auf die geschossen wird.
            
        spalte : int
            Spalte, auf die geschossen wird.
            
        
        Returns
        -------
        res : bool
            Ergebnis des Schusses.
        """
        
        koordinaten_schiff = self.get_koordinaten_schiff()
        i_pos = -1
        for (zeile_tmp, spalte_tmp) in koordinaten_schiff:
            i_pos += 1
            if(zeile_tmp == zeile
               and spalte_tmp == spalte
               and self.treffer[i_pos] == False):
                self.treffer[i_pos] = True
                return True
            
        return False
        
    def ist_versenkt(self):
        """
        Prüft, ob Schiff vollständig versenkt wurde.
        
        
        Returns
        -------
        res : bool
            ``True``, wenn auf alle Felder des Schiffes geschossen wurde.
        """
        
        return self.treffer.all()
    
    def pruefe_position(self, spielfeld):
        """
        Prüft, ob die aktuelle Position und Orientierung konform ist. Es wird
        geprüft, ob das Schiff auf das Spielfeld passt und es
        zu keiner Überschneidung mit einem anderen Schiff oder einem
        gesperrten Feld gibt.
        
        Schiff wird in dieser Methode noch nicht auf das Spiielfeld
        gesetzt. Dies geschieht mit :meth:`setze_schiff`.
        
        
        Parameters
        ----------
        spielfeld : array
            Spielfeld, auf welchem das Schiff platziert werden soll.
            
        
        Returns
        ------
        res : bool
            ``True``, wenn das Schiff nur auf leeren Feldern liegt und
            die Ränder an kein anderes Schiff stoßen.
        """
        
        anzahl_zeilen = spielfeld.shape[0]
        anzahl_spalten = spielfeld.shape[1]
        
        # 1. prüfe, ob alle Felder des zu setzenden Schiffes Leer sind
        koordinaten_schiff = self.get_koordinaten_schiff()
        for (zeile_tmp, spalte_tmp) in koordinaten_schiff:
            if(zeile_tmp >= anzahl_zeilen
               or spalte_tmp >= anzahl_spalten
               or spielfeld[zeile_tmp, spalte_tmp] != Feldstatus.LEER):
                
                # Spielfeld ist nicht leer
                return False
            
        # 2. prüfe Ränder
        koordinaten_rand = self.get_koordinaten_gesperrt()
        for(zeile_tmp, spalte_tmp) in koordinaten_rand:
            if(0 <= zeile_tmp < anzahl_zeilen 
               and 0 <= spalte_tmp < anzahl_spalten
               and (spielfeld[zeile_tmp, spalte_tmp] 
                    in [Feldstatus.SCHIFF_KEIN_TREFFER])):
                return False
        
        return True
        
    def setze_schiff(self, spielfeld):
        """
        Setzt das Schiff auf das Spielfeld. Damit werden auf dem Spielfeld
        in den entsprechenden Koordinaten die entsprechenden Werte gesetzt.
        
        Es wird davon ausgegangen, dass die Position valide ist. Dies kann
        vorher mit :meth:`pruefe_position` geprüft werden.
        
        
        Parameters
        ----------
        spielfeld : array
            Spielfeld, auf welchem das Schiff gesetzt werden soll.
        """

        anzahl_zeilen = spielfeld.shape[0]
        anzahl_spalten = spielfeld.shape[1]
        
        # 1. Setze Schiff
        koordinaten_schiff = self.get_koordinaten_schiff()
        for (zeile_tmp, spalte_tmp) in koordinaten_schiff:
            spielfeld[zeile_tmp, spalte_tmp] = Feldstatus.SCHIFF_KEIN_TREFFER
            
        # 2. sperre Ränder
        koordinaten_rand = self.get_koordinaten_gesperrt()
        for(zeile_tmp, spalte_tmp) in koordinaten_rand:
            if(0 <= zeile_tmp < anzahl_zeilen
               and 0 <= spalte_tmp < anzahl_spalten):
                spielfeld[zeile_tmp, spalte_tmp] = Feldstatus.GESPERRT
        
    def get_koordinaten_schiff(self):
        """
        Gibt die Koordinaten des Schiffs zurück.
        
        
        Returns
        -------
        koordinaten : list
            Liste der Koordinaten ((zeile, spalte)) des Schiffs.
        """
        
        koordinaten = []
        
        for i_pos in range(self.laenge):
            if(self.ist_waagerecht):
                zeile_tmp = self.zeile0
                spalte_tmp = self.spalte0 + i_pos
            
            else:
                zeile_tmp = self.zeile0 + i_pos
                spalte_tmp = self.spalte0
                
            koordinaten.append((zeile_tmp, spalte_tmp))
        
        return koordinaten
        
        
    def get_koordinaten_gesperrt(self):
        """
        Gibt die Koordinaten der anliegenden Felder zurück (links/rechts
        bzw. oben/unten).
        
        
        Returns
        -------
        koordinaten : list
            Liste der Koordinaten ((zeile, spalte)) der anliegenden Felder.
            Achtung: die Koordinaten der Felder müssen nicht zwangsweise
            gültig sein und können außerhalb des Spielfeldes liegen.
        """
        
        koordinaten = []

        # 'linkes' / oberes Ende
        if(self.ist_waagerecht):
            zeile_tmp = self.zeile0
            spalte_tmp = self.spalte0 - 1
            
        else:
            zeile_tmp = self.zeile0 - 1
            spalte_tmp = self.spalte0
        
        koordinaten.append((zeile_tmp, spalte_tmp))

        # 'rechtes' / unteres Ende
        if(self.ist_waagerecht):
            zeile_tmp = self.zeile0
            spalte_tmp = self.spalte0 + self.laenge
            
        else:
            zeile_tmp = self.zeile0 + self.laenge
            spalte_tmp = self.spalte0
        
        koordinaten.append((zeile_tmp, spalte_tmp))
        
        return koordinaten
    
    def get_name(self):
        """
        Gibt den Namen des Schiffes anhand der Länge zurück.
        
        
        Returns
        -------
        name : str
            Name des Schiffes.
        """
        
        if(self.laenge == 2):
            return "U-Boot"
        
        elif(self.laenge == 3):
            return "Zerstörer"
        
        elif(self.laenge == 4):
            return "Kreuzer"
        
        elif(self.laenge == 5):
            return "Schlachtschiff"
        
        else:
            # Standardname, falls unbekannte Länge
            return "Schiff"

###############################################################################
# Hauptmethode                                                                #
###############################################################################
       
def main_test():
    """
    Hauptmethode - nur fürs Testen
    """

    # Nutze festen Seed, damit reproduzierbare Ergebnisse untersucht werden
    # können - nur für den Testmodus
    np.random.seed(1234)
    
    # Reduziertes Feld für Testmodus
    dim = (4, 4)
    laenge_schiffe = [3, 3]

    # Starte Spiel
    spielwelt = Spielwelt(dim, laenge_schiffe)
    spielwelt.start()

def main(argv):
    """
    Hauptfunktion
    """
    
    zeilen = 10
    spalten = 10
    
    s_help = """
    Erlaubte Optionen:\n
    \n
    --zeilen= : Definiert Anzahl der Zeilen (muss zwischen 7 und 15 sein)\n
    --spalten= : Definiert Anzahl der Spalten (muss zwischen 7 und 15 sein)\n
    """
    
    # parse Optionen
    
    try:
      opts, args = getopt.getopt(argv,"h",["zeilen=","spalten="])
    except getopt.GetoptError:
      print(s_help)
      sys.exit(2)
    
    for opt, arg in opts:
        if(opt in ["-h", "--help"]):
            print(s_help)
            return
        
        elif(opt in ["--zeilen"]):
            zeilen = arg
            
        elif(opt in ["--spalten"]):
            spalten = arg
        
    try:
        zeilen = int(zeilen)
        spalten = int(spalten)
        
    except Exception:
        print("Anzahl der Zeilen und Spalten müssen ganzzahlig sein!")
        return
    
    if(not (7 <= zeilen <= 15)
        or not (7 <= spalten <= 15)):
        print("Anzahl der Zeilen und Spalten muss zwischen 7 und 15 liegen.")
        return
    
    # Definition Dimensionen und Länge der Schiffe
    dim = (zeilen, spalten)
    laenge_schiffe = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]  # Standardkonfiguration
    
    # Starte Spiel
    spielwelt = Spielwelt(dim, laenge_schiffe)
    spielwelt.start()
    
if __name__ == "__main__":
    # für Test
    #main_test()
    
    # für Haupt
    main(sys.argv[1:])
    
    
    


