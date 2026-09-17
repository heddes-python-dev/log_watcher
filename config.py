# config.py
import sys
from pathlib import Path

def _candidate_roots():
    """Liefert mögliche gemeinsame Ordner für Python- und EXE-Starts."""
    if getattr(sys, "frozen", False):
        executable_dir = Path(sys.executable).resolve().parent
        roots = [
            executable_dir,
            executable_dir.parent,
            executable_dir.parent.parent,
        ]
    else:
        roots = [Path(__file__).resolve().parent.parent]

    roots.append(Path.cwd().resolve())
    return list(dict.fromkeys(roots))


def _find_log_files(application, filename):
    """Findet Logs neben dem Quellordner und in dessen dist-Verzeichnis."""
    candidates = []
    for root in _candidate_roots():
        for candidate in (
            root / application / filename,
            root / application / "dist" / filename,
        ):
            if candidate.exists() and candidate not in candidates:
                candidates.append(candidate)

    if candidates:
        return [str(candidate) for candidate in candidates]

    root = _candidate_roots()[0]
    return [str(root / application / filename)]

LOG_FILE_PATHS = [
    path
    for application, filename in (
        ("system_monitor", "system_monitor.log"),
        ("netzwerk_monitor", "netzwerk_monitor.log"),
    )
    for path in _find_log_files(application, filename)
]

KEYWORDS = ["ERROR", "CRITICAL", "WARNING", "Exception", "FAIL"]
POLL_INTERVAL = 0.5



"""
# Pfad zur zu überwachenden Logdatei (Standard: eine lokale Test-Logdatei)
LOG_FILE_PATH = [
    "/home/dell/Schreibtisch/system_monitor/system_monitor.log",
    "/home/dell/Schreibtisch/netzwerk_monitor/netzwerk_monitor.log"
]

# Zu überwachende Schlüsselwörter / Muster
KEYWORDS = ["ERROR", "CRITICAL", "WARNING", "Exception", "FAIL"]

# Abfrage-Intervall in Sekunden für den Dateizugriff
POLL_INTERVAL = 0.5
"""