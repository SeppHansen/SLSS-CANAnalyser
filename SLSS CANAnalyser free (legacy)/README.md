![alt text](https://github.com/SeppHansen/SLSS-CANAnalyser/blob/main/SLSS%20CANAnalyser_banner.png?raw=true)


SLSS CANAnalyser ist eine Software zum Anzeigen, Aufzeichnen und Auswerten von CAN-Bus Daten. Als Hardware zur Verbindung mit dem Bus-System kommt ein, oder wahlweise auch mehrere Arduino (Uno) Micro-Controller, welche mit einem MCP2515 CAN-Controller-Board oder CAN-Shield bestückt werden, zum Einsatz. Das Hauptziel dieser Software soll es sein, die Handhabung und den Umgang mit CAN-Bus Signalen ohne den Einsatz von teurer Software oder Hardware zu ermöglichen.

Weitere Informationen siehe [langer-sebastian.de/SLSS-CANAnalyser](https://www.langer-sebastian.de/slss-cananalyser/)

  
## Funktionen

- Anzeigen eingehender CAN-Daten
- Aufzeichnung eingehender CAN-Daten
- Filterfunktion um nicht gewünschte oder benötigte CAN-IDs auszublenden
- gelesene und aufgezeichnete CAN-Daten können in eine Excel-Datei exportiert werden
- gelesene und aufgezeichnete CAN-Daten können in eine SLSS CANAnalyser spezifische Datei gespeichert und von dort aus wieder geladen werden
- eingehende CAN-Daten können anhand eines einstellbaren Suchrasters Bit- oder Byteweise durchsucht werden (1. Schritt - Reverse Engineering)
- gefundene Übereinstimmungen können in einer Ergebnisliste angezeigt und gespeichert / geladen werden
- CAN-DBC Dateien können erstellt, geladen, editiert und gespeichert werden (nur eingehende Daten in Version 1.1.0.14)
- komplette Projekte (gesetzte Einstellungen und DBC Liste, falls vorhanden) können, für einen schnellen Wechsel zwischen mehreren Projekten, geladen und gespeichert werden.


- **ab Version 1.1.0.14**

    - Alle Softwarekomponenten auf englische Spracheinstellung umstellbar
    - App Installer durch nativen Windows Installer ersetzt
    - TCP Client Interface - Weitergabe eingehender Botschaften an externe Anwendungen per TCP/IP Verbindung
    - Botschaftsänderungszähler in der Anzeige für eingehende CAN-Daten hinzugefügt
    - Byte-Highlighting - Anzeige der Änderungsposition (Byte) bei eingehenden Botschaften (abschaltbar)
    - Eingabe von Hexadezimalwerten im Sendebereich möglich
    - Kontinuierliches Sortieren (auf und absteigend) der Eingangsdaten per Spaltenauswahl umgesetzt
    - Ringpuffergröße des CAN Recorders einstellbar
    - Laden von DBC-Dateien verbessert und Optionen erweitert
  

- **ab Version 1.0.2.0**
    - richtige Darstellung von CAN Botschaften welche kürzer als 8 Byte Länge sind
    - Versionskontrolle des Micro-Controller Programmcodes beim Verbinden mit der Hardware umgesetzt


- **ab Version 1.0.0.1**
    - Auswertung der CAN Botschaften als ASCII-Textanzeige, um ASCII-Codierte Textübertragung erkennen zu können 
    - Implementierung des SLSS CANData Viewer zum Laden, Sichten und Auswerten von aufgezeichneten CAN-Botschaften 
    - Senden von CAN-Botschaften und Botschaftsabfolgen 

## Installation

### Micro-Controller
1. SLSS CANAnalyser Software für Microsoft Windows und Micro-Controller Code für den Arduino herunterladen 
2. Die richtige Takt-Frequenz für die Micro-Controller Software muss je nach verbautem Schwingquarz des CAN-Boards gewählt werden. Dazu den Wert des Schwingquarzes auf dem CAN-Board ablesen und analog dazu einfach den richtigen Programmcode im Ordner auswählen.

3. [optional] Die Geräte-ID kann in der Micro-Controller Software zur besseren Unterscheidung bei der Verwendung mehrerer CAN-Boards geändert werden  
4. den editierten Code via Arduino IDE auf den angeschlossenen Arduino hochladen (zum erfolgreichen Upload ist die Installation der verwendeten MCP-CAN Bibliothek nötig)

### SLSS CANAnalyser for Windows
1. SLSS CANAnalyser auf dem Windows-PC installieren und ausführen
2. Nach dem Start den COM-Port, an welchem der Arduino an den PC angeschlossen ist auswählen.<br><font color="red"><b>Hinweis:</b></font> Bitte, falls geöffnet, den seriellen Monitor der Arduino IDE schließen, da der SLSS CANAnalyser ansonsten keine Verbindung zum Board herstellen kann!
3. Nach dem Setzen der Bus-Geschwindigkeit kann die Verbindung zum CAN-Board durch das Klicken auf "verbinden" hergestellt werden.
4. Falls der COM-Port unbekannt sein sollte, kann über einen Klick auf "Modulsuche" das CAN-Board auch automatisch gesucht werden

Nach erfolgreich hergestellter Verbindung werden die eingehenden CAN-Daten im Tab "Aktuell eingehende CAN-Daten" unterhalb der Bedienelemente angezeigt. 
Weitere Informationen zur Bedienung können der Bedienungsanleitung (04.03.2021 - in Erstellung) entnommen werden.


## Hinweis Fehler und Debugging

Die Software befindet sich aktuell noch in er Entwicklung. Einige Funktionen können deshalb noch fehlerhaft oder ohne Funktion sein. Für das Melden von Fehlern wäre ich sehr dankbar und würde diese zeitnah mit einem Versionshub beheben.


## Haftungsausschluss

Die hier veröffentlichte Software wurde auf mehreren Systemen fehlerfrei getestet. Dennoch kann für evtl. Beschädigungen, Instabilitäten oder sonstige Beeinträchtigungen, welche unmittelbar durch die Installation, Nutzung, oder in sonstiger Weise in Zusammenhang stehend mit der hier zum Download angebotenen Software auftreten keinerlei Haftung übernommen werden. Der Download, die Installation und Nutzung geschehen auf eigenes Risiko! Bei Problemen wenden sie sich bitte an info@langer-sebastian.de!


## Zusatz zur Nutzung im Bereich der StVO / StVZO

Die angebotene Software ist ausschließlich für den Bereich des Prototyping gedacht und die Nutzung somit ausschließlich abseits des öffentlichen Verkehrsraums gestattet! Von einer Nutzung während der Fahrt wird ausdrücklich abgeraten. 







# SLSS-CANAnalyser (english)
SLSS CANAnalyser is a Microsoft Windows based CAN bus analysis software to show, record and evaluate CAN-Bus signals and data. For the connection with an CAN bus system, SLSS CANAnalyser use one or more Arduino microcontroller boards with installed MCP2515 CAN extension. One of the main intents behind SLSS CANAnalyser was to build a software solution for CAN analysis without the usage of professional and mostly expensive equipment. 

<b>Note:</b> The GUI of this software is completely in german, an english version will be released when the development is completely done, or the demand of an english version is huge. 

For further information, please go to [langer-sebastian.de/SLSS-CANAnalyser](https://www.langer-sebastian.de/slss-cananalyser/)

## Features

- visualize incoming CAN-data
- record incoming CAN-data 
- set filters to hide undesirable / not needed CAN-IDs (also possible for recording)
- export visualized and recorded CAN-data to Excel-file
- save and load recordings to files in SLSS CANAnalyser format
- automatically search for adjustable bit or byte changes in one or all incoming CAN-ids
- publish changes in separate result lists (also load- and savable)
- create, open, edit and save CAN-DBC files (only incoming-data supported on version 1.0.0.0)  
- show DBC-data values on an extra tab called "DBC-Signalliste"
- save and load complete projects (all settings and DBC-data will be stored) for fast switch of different projects


- **since version 1.1.0.14**

    - All software components changeable to english language 
    - Replaced app installer with native Windows installer
    - TCP client interface - forwarding of all incoming CAN messages to 3rd party applications via TCP/IP connection
    - Add message change counter for incoming messages inside the CAN data tab
    - Byte-highlighting - visualization of change position (byte) for incoming CAN data (switchable)
    - Input of hexadecimal values inside the send-message tab
    - Implement continuous sort mode (ascending and descending) for incoming data via column selection (switchable)
    - Adjustable buffer size for CAN Recorder
    - Increase loading and saving behaviour for *.dbc files

- **since version 1.0.2.0**
    - correct display of CAN messages shorter than 8 bytes
    - version check of actual flashed µC code



- **since version 1.0.0.1**
    - integrate module to evaluate ASCII-based text messages send via CAN bus 
    - implementation of "SLSS CANData Viewer" for loading, showing and evaluating recorded or stored CAN messages 
    - transmitting single or multiple CAN messages    


## Installation

### Micro-Controller
1. Download SLSS CANAnalyser Software for Windows and the code file for the Arduino based microcontroller
2. choose the correct oscillator-frequency of your CAN board by selecting the right file of microcontroller code (8MHz or 16Mhz)
3. [optional] configure device-ID in Arduino Code to distinguish multiple connected boards
4. upload the Arduino Code to your Arduino Board (the installation of the MCP-CAN library is necessary)

### SLSS CANAnalyser for Windows
1. install SLSS CANAnalyser for Windows on your Windows Computer
2. start SLSS CANAnalyser and select the com-port your Arduino microcontroller board is connected to <br><font color="red"><b>Notice:</b></font> Please close Arduino serial terminal if still opened, otherwise SLSS CANAnalyser could not create a connection to the board!
3. set CAN-Bus data rate and click "verbinden" to establish connection 
4. if you don't know the com port your microController board is connected to, use the modul search function by clicking on "Modulsuche" to automatically search for all connected modules.

- If connection was successfully established, you should see all incoming CAN data in the first tab underneath the control-buttons, named "Aktuell eingehende CAN-Daten"

For more information see the users manual (04.03.2021 - in creation / not available).

## Note for issues, malfunctions and debugging 

This Software is actually still in development. Some functions might be faulty or not usable. Please reply errors or bugs, to give me the chance the fix that with the next version.


## Disclaimer of liability

This software was tested on multiple systems without any problems or issues. Nevertheless, no liability can be assumed for any damage, instability or other impairments occurring directly or passively through the installation, usage or in any other kind of correlation with this software. Download, installation and usage is completely 
at your own risk! For any further problems, please contact info@langer-sebastian.de!


## Usage on public streets or roads

The software is intended for prototyping and should not be used in public traffic areas! A possible violation of the traffic law can occur. 


