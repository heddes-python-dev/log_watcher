# config.py

# Pfad zur zu überwachenden Logdatei (Standard: eine lokale Test-Logdatei)
LOG_FILE_PATH = [
    "/home/dell/Schreibtisch/system_monitor/system_monitor.log",
    "/home/dell/Schreibtisch/netzwerk_monitor/netzwerk_monitor.log"
]

# Zu überwachende Schlüsselwörter / Muster
KEYWORDS = ["ERROR", "CRITICAL", "WARNING", "Exception", "FAIL"]

# Abfrage-Intervall in Sekunden für den Dateizugriff
POLL_INTERVAL = 0.5