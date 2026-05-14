from pathlib import Path

import pandas as pd


DEFAULT_FIRSTNAME = "Max"
DEFAULT_LASTNAME = "Mustermann"

def load_csv(csv_path, required_columns):
    
    # Fehler falls die Datei nicht gefunden wird
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # die Spalte mit dem Zeitstempel (in String Format) wird eine datetime Spalte
    # also wir formatieren es so dass es zum Datum Datentyp wird
    df["questionnaire_answer_date"] = pd.to_datetime(
        df["questionnaire_answer_date"], errors="coerce"
    )
    # eine neue Spalte, die nur das Datum enthält (und ohne Uhrzeit), damit wir später nach dem Tag gruppieren können
    df["answer_day"] = df["questionnaire_answer_date"].dt.date

    return df

def load_patient_data(patient_data_path):
    try:
        patient_df = pd.read_csv(Path(patient_data_path), dtype=str).fillna("")
        patient_df = patient_df[["id_patient", "patient_firstname", "patient_lastname"]]

        patient_df["patient_firstname"] = patient_df["patient_firstname"].replace("", DEFAULT_FIRSTNAME)
        patient_df["patient_lastname"] = patient_df["patient_lastname"].replace("", DEFAULT_LASTNAME)

        return dict(zip(patient_df["id_patient"], zip(patient_df["patient_firstname"], patient_df["patient_lastname"])))
    except Exception as exception:
        print(f"Warnung: Konnte Patientendaten nicht laden: {exception}")
        return {}