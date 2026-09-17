# Log Watcher

Der Log Watcher ist ein kleines GUI-Tool zum Live-Anzeigen von Logdateien im Stil eines Tail-Views. Er überwacht in Echtzeit die Ausgaben von zwei Monitoring-Projekten und zeigt neue Einträge direkt in einer Tkinter-Oberfläche an.

## Kurzbeschreibung

Das ist ein einfacher Tail-Viewer für die Logdateien von:
- system_monitor
- network_monitor

Er verfolgt neue Einträge aus den laufenden Logs dieser Monitor-Tools und zeigt sie sofort in einer Übersicht an. So lässt sich der Betrieb schnell überwachen, ohne die Logdateien manuell im Terminal zu öffnen.

## Zweck

Dieser Watcher dient als Tail für:
- system_monitor
- netzwerk_monitor

Er liest die Logdateien dieser beiden Tools kontinuierlich aus und fasst relevante Einträge visuell zusammen. Dadurch lässt sich schnell erkennen, ob Fehler, Warnungen oder kritische Meldungen im laufenden Betrieb auftreten.

## Funktionalität

- Überwachung mehrerer Logdateien gleichzeitig
- Echtzeit-Anzeige neuer Zeilen
- Farbige Kennzeichnung nach Log-Level:
  - INFO
  - WARNING
  - ERROR
- Filterung nach Schlüsselwörtern wie ERROR, CRITICAL, WARNING, Exception und FAIL
- Popup-Warnung bei kritischen Einträgen
- Kompakte GUI mit Scrollbereich für die Log-Ausgabe

## Verwendete Logdateien

Der Watcher sucht nach den Logs in den Projektordnern der beiden Monitore. Dabei werden sowohl die normalen Pfade als auch die `dist/`-Pfade der EXE-Versionen berücksichtigt:

- .../system_monitor/system_monitor.log
- .../system_monitor/dist/system_monitor.log
- .../netzwerk_monitor/netzwerk_monitor.log
- .../netzwerk_monitor/dist/netzwerk_monitor.log

Die Pfade sind in [config.py](config.py) konfigurierbar.

## Projektstruktur

- [main.py](main.py): Einstiegspunkt der Anwendung
- [config.py](config.py): Konfiguration der Logpfade und Filter
- [file_watcher.py](file_watcher.py): Log-Reader mit Tail-ähnlichem Verhalten
- [filter_module.py](filter_module.py): Prüfung auf relevante Schlüsselwörter
- [gui_module.py](gui_module.py): Benutzeroberfläche
- [popup_module.py](popup_module.py): Warnfenster für kritische Einträge

## Starten mit Python

Linux:

```bash
cd .../log_watcher
python3 main.py
```

Windows PowerShell:

```powershell
cd ...\log_watcher
python main.py
```

## Starten mit PyInstaller

Die fertige Anwendung liegt nach dem Build in `dist/`:

- Linux: `dist/main`
- Windows: `dist/main.exe`

Die EXE muss auf dem jeweiligen Zielsystem gebaut werden. Dazu im Projektverzeichnis ausführen:

Linux:

```bash
python3 -m pip install pyinstaller
python3 -m PyInstaller --clean --noconfirm main.spec
./dist/main
```

Windows PowerShell:

```powershell
python -m pip install pyinstaller
python -m PyInstaller --clean --noconfirm main.spec
.\dist\main.exe
```

Der Log-Watcher sollte gestartet werden, nachdem die Monitor-Anwendungen laufen. Angezeigt werden neue Logzeilen ab dem Start des Watchers.

## Beispielausgabe

```text
[system_monitor.log] 2026-09-17 12:00:01 [INFO] Systemstatus normal
[network_monitor.log] 2026-09-17 12:00:02 [WARNING] Verbindung zum Gateway langsam
[system_monitor.log] 2026-09-17 12:00:03 [ERROR] CPU-Temperatur kritisch hoch
```

## Hinweis

Der Log Watcher ist bewusst als Tail-Tool für die Logausgaben von system_monitor und netzwerk_monitor aufgebaut. Er zeigt also nicht selbst Logs an, sondern verfolgt die laufenden Ausgaben dieser Monitor-Programme in Echtzeit.

## Hinweis zur Umgebung

Falls die überwachten Logdateien noch nicht existieren, erzeugt der Watcher diese automatisch beim Start und wartet auf neue Einträge.
