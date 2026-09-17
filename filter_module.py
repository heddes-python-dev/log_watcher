# filter_module.py

def analyze_line(line, keywords):
    """Prüft, ob eine Zeile ein Keyword enthält und gibt den Status zurück."""
    for kw in keywords:
        if kw in line:
            # Bestimme den Level basierend auf dem Keyword
            if kw in ["ERROR", "CRITICAL", "Exception", "FAIL"]:
                return True, "ERROR", kw
            else:
                return True, "WARNING", kw
    return False, "INFO", None