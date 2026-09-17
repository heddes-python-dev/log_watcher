# main.py
import queue
import threading
import tkinter as tk
from config import LOG_FILE_PATH, KEYWORDS
from file_watcher import MultiFileWatcher as FileWatcher
from filter_module import analyze_line
from gui_module import LogWatcherGUI
from popup_module import show_critical_alert

class LogWatcherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.log_queue = queue.Queue()
        
        # Watcher initialisieren
        self.watcher = FileWatcher(LOG_FILE_PATH, self.on_new_line)
        
        # GUI initialisieren
        self.gui = LogWatcherGUI(self.root, self.stop_app)
        
        # Worker-Thread für das Einlesen der Datei starten
        self.watcher_thread = threading.Thread(target=self.watcher.start, daemon=True)
        self.watcher_thread.start()

        # Regelmäßiges Prüfen der Queue starten (Polling im Tkinter-Hauptthread)
        self.root.after(100, self.process_queue)

    def on_new_line(self, line):
        """Callback vom FileWatcher, wenn eine Zeile reinkommt."""
        is_match, level, keyword = analyze_line(line, KEYWORDS)
        self.log_queue.put((line, level, keyword if is_match else None))

    def process_queue(self):
        """Verarbeitet die Queue im Hauptthread (Thread-sicher für Tkinter)."""
        while not self.log_queue.empty():
            line, level, keyword = self.log_queue.get_nowait()
            self.gui.append_log(line, level)
            
            # Optionales Pop-up bei kritischen Fehlern
            if keyword in ["ERROR", "CRITICAL", "Exception"]:
                show_critical_alert(keyword, line)

        # Nach 100ms erneut aufrufen
        self.root.after(100, self.process_queue)

    def stop_app(self):
        self.watcher.stop()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LogWatcherApp()
    app.run()