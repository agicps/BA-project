from pathlib import Path

# Directory structure 
BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
CHART_DIR  = OUTPUT_DIR / "charts"

# Input file
INPUT_CSV_PATH = DATA_DIR / "export.csv"

# Required CSV columns
REQUIRED_COLUMNS = [
    "id_patient",
    "questionnaire_title",
    "questionnaire_question",
    "questionnaire_answer_date",
    "questionnaire_answer_value",
    "questionnaire_reply_status",
]

# Questionnaires to process
RELEVANT_QUESTIONNAIRES = [
    "FACIT-Erschöpfung",
    "OMDQ",
    "Übelkeit/Erbrechen",
    "PG-SGA SF | Patientenbezogenes Ernährungsassesment",
]

# FACIT-Fatigue title and cutoff score
FACIT_TITLE  = "FACIT-Erschöpfung"
FACIT_CUTOFF = 26

# Scoring 
MAX_POINTS = 10
