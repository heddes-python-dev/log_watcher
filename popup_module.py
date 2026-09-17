# popup_module.py
from tkinter import messagebox

def show_critical_alert(keyword, line):
    """Öffnet ein Warn-Popup bei kritischen Treffern."""
    messagebox.showwarning(
        "Kritischer Log-Eintrag erkannt!",
        f"Schlüsselwort: {keyword}\n\nEintrag:\n{line}"
    )