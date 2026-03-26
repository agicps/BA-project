from pathlib import Path
# Hier speichern wir alle Daten zum Konfigurieren der Anwendung


# Verzeichnisstruktur
    # generell ist die Struktur vom Projekt wie folgt:
    # project/
    # ├── data/
    # │   └── export.csv
    # ├── output/
    # │   └── hier sind die generierten PDFs
    # ├── src/
    # │   ├── config.py # hier speichern wir alle Daten zum Konfigurieren der Anwendung
    # │   ...
BASE_DIR = Path(__file__).parent.parent
    # BASE_DIR ist der Pfad zum Verzeichnis, in dem das Projekt liegt
    # Path(__file__) gibt den Pfad von der aktuellen Datei (also config.py) zurück
    # .parent.parent geht zwei Ebenen hoch, d.h. zum Verzeichnis in dem das Projekt liegt
DATA_DIR   = BASE_DIR / "data"
    # DATA_DIR ist der Pfad zum Verzeichnis, in dem die Daten liegen, d.h. die CSV-Datei die wir verarbeiten
    # wir gehen aus dem projektverzeichnis in das data verzeichnis
    # mit / können wir Pfade kombinieren
OUTPUT_DIR = BASE_DIR / "output"
    # OUTPUT_DIR ist der Pfad zum Verzeichnis, in dem die generierten PDFs gespeichert werden
    # wir gehen aus dem projektverzeichnis in das output verzeichnis

# CSV datei
INPUT_CSV_PATH = DATA_DIR / "export.csv"
    # lokal z.b. so gespeichert "C:\Users\agnie\Downloads\export.csv"

# Benötigte CSV Spalten als Liste
REQUIRED_COLUMNS = [
    "id_patient",
    "questionnaire_title",
    "questionnaire_question",
    "questionnaire_answer_date",
    "questionnaire_answer_value",
    "questionnaire_reply_status",
    "questionnaire_answer_type"
]

# Zu verarbeitende Fragebögen (so wie es in CSV steht)
RELEVANT_QUESTIONNAIRES = [
    "FACIT-Erschöpfung",
    "PG-SGA SF | Patientenbezogenes Ernährungsassesment",
    "OMDQ",
    "Übelkeit/Erbrechen"
]

# In einem Dictionary speichern wir die keys der Fragebögen
QUESTIONNAIRES = {
    "facit": "FACIT-Erschöpfung",
    "pgsga": "PG-SGA SF | Patientenbezogenes Ernährungsassesment",
    "omdq": "OMDQ",
    "uebelkeit": "Übelkeit/Erbrechen"
}

'''# FACIT-Fatigue title and cutoff score
FACIT_TITLE  = "FACIT-Erschöpfung"
FACIT_CUTOFF = 26 '''

# Anzahl der Punkte im Graphen die wir maximal anzeigen wollen
MAX_POINTS = 8






