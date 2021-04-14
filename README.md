![alt text](https://github.com/SeppHansen/SLSS-CANAnalyser/blob/main/SLSS%20CANAnalyser_banner.png?raw=true)


SLSS CANAnalyser ist eine Software zum Anzeigen, Aufzeichnen und Auswerten von CAN-Bus Daten. Als Hardware zur Verbindung mit dem Bus-System kommt ein, oder wahlweise auch mehrere Arduino (Uno) Micro-Controller, welche mit einem MCP2515 CAN-Controllerboard oder CAN-Shield bestückt werden, zum Einsatz. Das Hauptziel dieser Software soll es sein, die Handhabung und den Umgang mit CAN-Bus Signalen ohne den Einsatz von teuerer Software oder Hardware zu ermöglichen.

Weitere Informationen siehe [langer-sebastian.de/SLSS-CANAnalyser](https://www.langer-sebastian.de/slss-cananalyser/)
  
## Funktionen

- Anzeigen eingehender CAN-Daten
- Aufnehmen eingehender CAN-Daten
- Filterfuntion um nicht gewünschte oder benötigte CAN-IDs auszublenden
- gelesene und aufgezeichnete CAN-Daten können in eine Excel-Datei exportiert werden
- gelesene und aufgezeichnete CAN-Daten können in eine SLSS CANAnalyser spezifische Datei gespeichert und von dort aus wieder geladen werden
- eingehende CAN-Daten können anhand eines einstellbaren Suchrasters Bit- oder Byteweise durchsucht werden (1. Schritt - Reverse Engineering)
- gefundene Übereinstimmungen können in einer Ergebnisliste angezeigt und gespeichert / geladen werden
- CAN-DBC Dateien können erstellt, geladen, editiert und gespeichert werden (nur eingehende Daten in Version 1.0.0.0)
- komplette Projekte (gesetzte Einstellungen und DBC Liste, falls vorhanden) können, für einen schnellen Wechsel zwischen mehreren Projekten, geladen und gespeichert werden.  
**ab Version 1.0.0.1**
    - Auswertung der CAN Botschaften als ASCII-Textanzeige, um ASCII-Codierte Textübertragung erkennen zu können 
    - Implementierung des SLSS CANData Viewer zum Laden, Sichten und Auswerten von aufgezeichneten CAN-Botschaften 
    - Senden von CAN-Botschaften und Botschaftsabfolgen 

## Installation

### Micro-Controller
- SLSS CANAnalyser Software für Microsoft Windows und Micro-Controller Code für den Arduino herunterladen 
- Die richtige Takt-Frequenz in der Micro-Controller Software muss je nach verbautem Schwingquartz des CAN-Boards gewählt werden. Dazu einfach den richtigen Eintrag im Programmcode wählen, der nicht zutreffende Eintrag muss dann gelöscht, oder auskommentiert werden. 
- [optional] Die Geräte-ID kann in der Micro-Controller Software zur besseren Unterscheidung bei der Verwendung mehrerer CAN-Boards geändert werden  
- den editierten Code via Arduino IDE auf den angeschlossenen Arduino hochladen (zum erfolgereichen Upload ist die Installation der verwendeten MCP-CAN Bibliothek nötig)

### SLSS CANAnalyser for Windows
- SLSS CANAnalyser auf dem Windows PC installieren und ausführen
- nach dem Start den COM-Port, an welchem der Arduino an den PC angeschlossen ist auswählen (Hinweis: bitte, falls geöffnet, den seriellen Monitor der Arduino IDE schließen, da der SLSS CANAnalyser ansonsten keine Verbindung zum Board herstellen kann!)
- nach dem Setzen der Bus-Geschwindigkeit kann die Verbindung zum CAN-Board durch das Klicken auf "verbinden" hergestellt werden
- Falls der Port unbekannt sein sollte, kann über die Modulsuche das CAN-Board automatisch gesucht werden

Nach erfolgreich hergestellter Verbindung werden die eingehenden CAN-Daten im Tab "Aktuell eingehende CAN-Daten" unterhalb der Bedienelemente angezeigt. 
Weitere Informationen zur Bedienung können der Bedienungsanleitung (04.03.2021 - in Erstellung) entnommen werden.


## Hinweis Fehler und Debugging

Die Software befindet sich aktuell noch in er Entwicklung. Einige Funktionen können deshalb noch fehlerhaft oder ohne Funktion sein. Für das Melden von Fehlern wäre ich sehr dankbar und würde diese zeitnah mit einem Versionshub beheben.


## Haftungsausschluss

Die hier veröffentlichte Software wurde auf mehreren Systemen fehlerfrei getestet. Dennoch kann für evtl. Beschädigungen, Instabilitäten oder sonstige Beeinträchtigungen, welche unmittelbar durch die Installation, Nutzung, oder in sonstiger Weise in Zusammenhang stehend mit der hier zum Download angebotenen Software auftreten keinerlei Haftung übernommen werden. Der Download, die Installation und Nutzung geschehen auf eigenes Risiko! Bei Problemen wenden sie sich bitte an info@langer-sebastian.de!


## Zusatz zur Nutzung im Bereich der StVO / StVZO

Die angebotene Software ist ausschließlich für den Bereich des Prototyping gedacht und die Nutzung somit ausschließlich abseits des öffentlichen Verkehrsraum gestattet! Von einer Nutzung während der Fahrt wird ausdrücklich abgeraten. 







# SLSS-CANAnalyser (english)
SLSS CANAnalyser is a for use with Microsoft Windows designed CAN-Bus-Analysis-Software to show, record and evaluate CAN-Bus signals and data. For the connection with an CAN-Bus System, SLSS CANAnalyser uses one or more Arduino Micro-Controller with installed MCP2515-CAN Boards. One of the main intents behind SLSS CANAnalyser was to create a software solution for CAN analysis without the usage of professional equipment. 

Note:The GUI of this software is completely in german, an english version will be released when the developement is completely done, or  the demand of an english version is huge. 

For further informations, please go to [langer-sebastian.de/SLSS-CANAnalyser](https://www.langer-sebastian.de/slss-cananalyser/)

## Features

- Visualize incoming CAN-data
- Record incomming CAN-data 
- Set filters to hide undesirable / not needed CAN-IDs (also possible for recording)
- Export visualized and recorded CAN-data to Excel-file
- Save and load recordings to files in SLSS CANAnalyser format
- Automatically search for adjustable bit or byte changings in one or all incoming CAN-Ids
- Publish changings in separate resultlist (also load- and saveable)
- Create, open, edit and save CAN-DBC files (only incoming-data supported on version 1.0.0.0)  
- Show DBC-data values on an extra tab called DBC-Signalliste
- Save and load complete projects (all settings and DBC-data will be stored) for fast switch of different projects
**from Version 1.0.0.1**
    - Integrated module to evaluate ASCII-based textmessages sended via CAN-Bus 
    - Implementation of SLSS CANData Viewer for loading, showing and evaluating recorded or stored CAN messages 
    - Transmitting single or multiple CAN messages    


## Installation

### Micro-Controller
- Download SLSS CANAnalyser Software for Windows and the codefile for the Arduino based Micro-Controller
- Choose the right oscillator-frequency for your CAN-Board by set / comment out the right values on top of the code (8MHz or 16Mhz)
- [optional] Configure device-ID in Arduino Code to distinguish multiple connected boards
- Upload the Arduino Code to your Arduino Board (the installation of the MCP-CAN library is necessary)

### SLSS CANAnalyser for Windows
- Install SLSS CANAnalyser for Windows on your Windows Computer
- Start SLSS CANAnalyer and select the com-port the Arduino Micro-Controllerboard is connected to (note: please close Arduino serial terminal if still opened, otherwise SLSS CANAnalyser could not create an connection to the board!)
- Set CAN-Bus data-rate and click "verbinden" to establish connection 
- If you don't know to which com-port your Micro-Controllerboard is connected to, use the modul-search function to automatically search for all connected modules. (click on "Modulsuche" button)
- If connection was sucessfully established, you should see all incomming CAN data in the first tab underneath the control-buttons, named "Aktuell eingehende CAN-Daten"

For more informations see the users manual (04.03.2021 - in creation / not available).

## Note for issues, malfunctions and debugging 

This Software is actually still in development. Some functions might be faulty or not usable. Please reply errors or bugs, to give me the chance the fix that with the next version.


## Disclaimer of liability

This software was tested on multiple systems without any problems or issues. Nevertheless, no liability can be assumed for any damage, instability or other impairments occuring directly or passively through the installation, usage or in any other kind of correlation with these software. Download, installation and usage is completely 
at your own risk! For any further problems, please contact info@langer-sebastian.de!


## Usage on public streets or roads

The software is intended for prototyping and should not be used in public traffic areas! A possible violation of the traffic law can occur. 


