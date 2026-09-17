# main.py
import queue
import threading
import tkinter as tk
import sys
import traceback
from pathlib import Path
from tkinter import messagebox
from config import LOG_FILE_PATHS, KEYWORDS
from file_watcher import MultiFileWatcher as FileWatcher
from filter_module import analyze_line
from gui_module import LogWatcherGUI
from popup_module import show_critical_alert

class LogWatcherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.log_queue = queue.Queue()
        
        # Watcher initialisieren
        self.watcher = FileWatcher(
            LOG_FILE_PATHS,
            self.on_new_line,
            self.on_watcher_status,
        )
        
        # GUI initialisieren
        self.gui = LogWatcherGUI(self.root, self.stop_app)
        
        # Worker-Thread für das Einlesen der Datei starten
        self.watcher_thread = threading.Thread(target=self.watcher.start, daemon=True)
        self.watcher_thread.start()

        # Regelmäßiges Prüfen der Queue starten (Polling im Tkinter-Hauptthread)
        self.root.after(100, self.process_queue)

        for path in LOG_FILE_PATHS:
            self.gui.append_log(f"Überwachung gestartet: {path}")

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

    def on_watcher_status(self, status):
        self.root.after(0, self.gui.set_status, status)

    def stop_app(self):
        self.watcher.stop()

    def run(self):
        self.root.mainloop()

def _write_startup_error(error):
    if getattr(sys, "frozen", False):
        error_path = Path(sys.executable).resolve().with_name("log_watcher_error.log")
    else:
        error_path = Path(__file__).resolve().with_name("log_watcher_error.log")
    error_path.write_text(traceback.format_exc(), encoding="utf-8")
    return error_path


if __name__ == "__main__":
    try:
        app = LogWatcherApp()
        app.run()
    except Exception as error:
        error_path = _write_startup_error(error)
        try:
            messagebox.showerror(
                "Log Watcher konnte nicht gestartet werden",
                f"{error}\n\nDetails: {error_path}",
            )
        except tk.TclError:
            pass