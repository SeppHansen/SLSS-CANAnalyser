# SLSS-CANAnalyser
CAN-Bus Analysesoftware für Windows. Als zusätzliche Hardware wird ein Arduino (Uno) Micro-Controller und ein MCP2515 CAN-COntrollerboard oder CAN-Shield benötigt.

SLSS CANAnalyser ist eine in C# programmierte Software um CAN-Bus Signale anzuzeigen, aufzuzeichnen und zu analysieren. Das einzige was man dazu benötigt ist ein Windows PC, einen Arduino Micro-Controller und ein daran angeschlossenes CAN-Controllerboard oder CAN-Shield. Das Hauptziel dieser Software soll es sein, die Handhabung und den Umgang mit CAN-Bus Daten ohne den Einsatz von teuerer Software oder Hardware zu ermöglichen.


## Funktionen

- Anzeige eingehender CAN-Daten
- Aufnahme eingehender CAN-Daten
- Filterfuntion um nicht gewünschte oder benötigte CAN-IDs auszublenden
- gelesene und aufgezeichnete CAN-Daten können in eine Excel-Datei exportiert werden
- gelesene und aufgezeichnete CAN-Daten können in eine SLSS CANAnalyser spezifische Datei gespeichert und von dort aus wieder geladen werden
- eingehende CAN-Daten können anhand eines einstellbaren Suchrasters Bit- oder Byteweise durchsucht werden (1. Schritt - Reverse Engineering)
- gefundene Übereinstimmungen können in einer Ergebnisliste angezeigt und gespeichert / geladen werden
- CAN-DBC Dateien können erstellt, geladen, editiert und gespeichert werden (nur eingehende Daten in Version 1.0.0.0)
- komplette Projekte (gesetzte Einstellungen und DBC Liste, falls vorhanden) können, für einen schnellen Wechsel zwischen mehreren Projekten, geladen und gespeichert werden.  


## Installation

- dSLSS CANAnalyser und Micro-Controller Code für den Arduino herunterladen 
- Die Geräte-ID kann in der Micro-Controller Software zur besseren Unterscheidung bei der Verwendung mehrerer CAN-Boards geändert werden
- Die richtige Takt-Frequenz in der Micro-Controller Software muss je nach verbautem Schwingquartz des CAN-Boards gewählt werden  
- den Code anschließend auf den angeschlossenen Arduino hochladen
- SLSS CANAnalyser auf dem Windows PC installieren
- SLSS CANAnalyser ausführen und den COM-Port, mit welchem der Arduino an den PC angeschlossen ist auswählen (Hinweis: bitte den seriellen Monitor der Arduino IDE schließen, da der SLSS CANAnalyser ansonsten keine Verbindung zum Board herstellen kann!) 
- Falls der Port unbekannt ist, kann über die Modulsuche das CAN-Board automatisch gesucht werden 
- Nach erfolgreich hergestellter Verbindung werden die eingehenden CAN-Daten im Tab "Aktuell eingehende CAN-Daten" Unterhalb der Bedienelemente angezeigt


## Hinweis

Die Software befindet sich aktuell noch in er Entwicklung. Einige Funktionen können deshalb noch fehlerhaft oder ohne Funktion sein. Für das Melden von Fehlern wäre ich sehr dankbar und würde diese zeitnah mit einem Versionshub beheben.


## Haftungsausschluss

Die hier veröffentlichte Software wurde auf mehreren Systemen fehlerfrei getestet. Dennoch kann für evtl. Beschädigungen, Instabilitäten oder sonstige Beeinträchtigungen, welche unmittelbar durch die Installation, Nutzung, oder in sonstiger Weise in Zusammenhang stehend mit der hier zum Download angebotenen Software auftreten keinerlei Haftung übernommen werden. Der Download, die Installation und Nutzung geschehen auf eigenes Risiko! Bei Problemen wenden sie sich bitte an info@langer-sebastian.de!


## Zusatz zur Nutzung im Bereich der StVO / StVZO

Die angebotene Software ist ausschließlich für den Bereich des Prototyping gedacht und die Nutzung somit ausschließlich abseits des öffentlichen Verkehrsraum gestattet! Von einer Nutzung während der Fahrt wird ausdrücklich abgeraten. 




# SLSS-CANAnalyser (english)
Windows CAN-Bus-Analysis-Software to use with Arduino Micro-Controller in combination with MCP2515-CAN Boards.  

SLSS CANAnalyser is an in C# written Software to track, analyse and reverse engineer CAN-Bus systems. The only thing you need is a Windows PC, an Arduino compatible Micro-Controller with an connected CAN-Controllerboard or CAN-Shield. The GUI of this software is completely in german, an english version will be released when the developement is completely done, or  the demand of an english version is huge. 


## Features

- have a look on incoming CAN-data
- record incomming CAN-data 
- set filters to hide undesirable / not needed CAN-IDs (also possible for recording)
- export recorded and shown CAN-data to Excel-file
- save and load recording to files in SLSS CANAnalyser format
- automatically search for adjustable bit or byte changings in one or all incoming CAN-Ids
- publish changings in separate resultlist (also load- and saveable)
- create, open, edit and save CAN-DBC files (only incoming-data supported on version 1.0.0.0)  
- showing DBC-data values on an extra tab called DBC-Signalliste
- save and load complete projects (all settings and DBC-data will be stored) for fast switch of different projects   


## Installation

- download SLSS CANAnalyser and µC codefile for Arduino 
- Configure device-ID in Arduino Code to distinguish multiple connected boards
- choose the right oscillator-frequency for your CAN-Board by set / comment out the right values on top of the code (8MHz or 16Mhz)
- Upload the Arduino Code to your Arduino Board 
- install SLSS CANAnalyser to your Windows Computer
- start SLSS CANAnalyer and select com-port the controller is connected to (note: please close Arduino terminal connection if still present. Otherwise SLSS CANAnalyser can't find your Controllerboard!) 
- if you don't know to which com-port your Arduinoboard is connected, you can use the modul-search function. (click on "Modulsuche" button)
- if connection is established you can see all incomming CAN data in the first tab underneath the control-buttons.


## Note

This Software is actually still in development. Some functions might be faulty or not usable. Please reply errors or bug, to give me the opportunity the fix that with the next version.


## Disclaimer of liability

This software was tested on multiple systems without any problems or issues. Nevertheless, no liability can be assumed for any damage, instability or other impairments occuring directly or passively through the installation, usage or in any other kind of usage with these software offered here for download. Download, installation and usage is completely 
on your own risk! If you have any further problems, please contact info@langer-sebastian.de!


## Usage on public streets or roads

The software is intended for prototyping and should not be used in public traffic areas! A possible violation of the traffic law can occur. 


