# gui_module.py
import tkinter as tk
from tkinter import scrolledtext

class LogWatcherGUI:
    def __init__(self, root, stop_callback):
        self.root = root
        self.root.title("Log Watcher - Admin Tool Suite")
        self.root.geometry("800x500")
        self.stop_callback = stop_callback
        
        # UI Elemente erstellen
        self.create_widgets()
        
        # Schließen-Event abfangen
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Überschrift / Status
        self.label = tk.Label(self.root, text="Echtzeit Log-Überwachung", font=("Arial", 12, "bold"))
        self.label.pack(pady=(5, 0))

        self.status_label = tk.Label(self.root, text="Starte Überwachung ...", anchor="w")
        self.status_label.pack(fill="x", padx=10)

        # Textfeld für Log-Ausgabe (mit Scrollbalken)
        self.log_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', bg="#1e1e1e", fg="#d4d4d4", font=("Courier", 10))
        self.log_display.pack(expand=True, fill='both', padx=10, pady=5)

        # Tags für Farbgebung definieren
        self.log_display.tag_config("ERROR", foreground="#ff5555")
        self.log_display.tag_config("WARNING", foreground="#ffb86c")
        self.log_display.tag_config("INFO", foreground="#50fa7b")

    def append_log(self, text, level="INFO"):
        """Fügt eine neue Log-Zeile farbig in die GUI ein."""
        self.log_display.config(state='normal')
        self.log_display.insert(tk.END, text + "\n", level)
        self.log_display.yview(tk.END)  # Automatisch nach unten scrollen
        self.log_display.config(state='disabled')

    def set_status(self, text):
        self.status_label.config(text=text)

    def on_close(self):
        """Beendet den Hintergrund-Worker beim Schließen des Fensters."""
        self.stop_callback()
        self.root.destroy()