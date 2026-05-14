from pathlib import Path
import sys
# Hier speichern wir alle Daten zum Konfigurieren der Anwendung


def _resolve_base_dir() -> Path:
    exe_dir = Path(sys.executable).resolve().parent
    src_dir = Path(__file__).resolve().parent.parent
    candidates = [exe_dir, exe_dir.parent, Path.cwd(), Path(getattr(sys, "_MEIPASS", ""))] if getattr(sys, "frozen", False) else [src_dir, Path.cwd()]

    return next((p for p in candidates if (p / "Exportdatei").exists()), candidates[0])

BASE_DIR = _resolve_base_dir()
    # BASIS_DIR ist der Pfad zum Verzeichnis, in dem das Projekt liegt
    # Path(__file__) gibt den Pfad von der aktuellen Datei (also config.py) zurück
    # .parent.parent geht zwei Ebenen hoch, d.h. zum Verzeichnis in dem das Projekt liegt
DATEI_DIR   = BASE_DIR / "Exportdatei"
    # DATA_DIR ist der Pfad zum Verzeichnis, in dem die Daten liegen, d.h. die CSV-Datei die wir verarbeiten
    # wir gehen aus dem projektverzeichnis in das data verzeichnis
    # mit / können wir Pfade kombinieren
AUSGABE_DIR = BASE_DIR / "Ausgabe"
    # OUTPUT_DIR ist der Pfad zum Verzeichnis, in dem die generierten PDFs gespeichert werden
    # wir gehen aus dem projektverzeichnis in das output verzeichnis

# CSV datei
INPUT_CSV_PATH = DATEI_DIR / "export.csv"
#BIG_INPUT_CSV_PATH = DATEI_DIR / "export-big.csv"
PATIENT_DATA_PATH = DATEI_DIR / "digicare_patients.csv"

# Verwendete CSV Spalten als Liste
usedSpalten = [
    "id_patient",
    "questionnaire_title",
    "questionnaire_question",
    "questionnaire_answer_date",
    "questionnaire_answer_value",
    "questionnaire_reply_status",
    "questionnaire_answer_type"]

# Alias für konsistente Imports in main.py
REQUIRED_COLUMNS = usedSpalten

# Zu verarbeitende Fragebögen (so wie es in CSV steht)
relevantQuestionnaires = [
    "FACIT-Erschöpfung",
    "PG-SGA SF | Patientenbezogenes Ernährungsassesment",
    "OMDQ",
    "Übelkeit/Erbrechen"]

# In einem Dictionary speichern wir die keys der Fragebögen
questionnaires = {
    "facit": "FACIT-Erschöpfung",
    "pgsga": "PG-SGA SF | Patientenbezogenes Ernährungsassesment",
    "omdq": "OMDQ",
    "uebelkeit": "Übelkeit/Erbrechen"}

# Anzahl der Punkte im Graphen die wir maximal anzeigen wollen
GraphPunkteAnzahl = 8
