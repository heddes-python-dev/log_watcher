# file_watcher.py
import os
import time

class MultiFileWatcher:
    def __init__(self, paths, callback):
        # Falls versehentlich nur ein String übergeben wurde, in eine Liste packen
        self.filepaths = [paths] if isinstance(paths, str) else paths
        self.callback = callback
        self._running = False
        self.threads = []

    def start(self):
        self._running = True
        import threading
        
        for path in self.filepaths:
            t = threading.Thread(target=self._watch_file, args=(path,), daemon=True)
            self.threads.append(t)
            t.start()

    def _watch_file(self, filepath):
        # Sicherstellen, dass die Datei existiert
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(f"[INFO] Warte auf Datei: {filepath}\n")

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(0, os.SEEK_END)
            
            # Dateinamen für die Kennzeichnung extrahieren (z. B. "system_monitor.log")
            file_name = os.path.basename(filepath)
            
            while self._running:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                # Zeile mit Quellenangabe versehen und an Callback übergeben
                formatted_line = f"[{file_name}] {line.strip()}"
                self.callback(formatted_line)

    def stop(self):
        self._running = False