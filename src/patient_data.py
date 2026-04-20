from pathlib import Path

import pandas as pd


DEFAULT_FIRSTNAME = "Max"
DEFAULT_LASTNAME = "Mustermann"


def load_patient_data(patient_data_path):
    """
    Lädt die Patientendaten aus CSV und gibt ein Dictionary zurück.

    Gibt zurück:
        Dictionary mit {patient_id: (firstname, lastname)}
    """
    try:
        patient_df = pd.read_csv(Path(patient_data_path), dtype=str).fillna("")
        patient_df = patient_df[["id_patient", "patient_firstname", "patient_lastname"]]

        patient_df["patient_firstname"] = patient_df["patient_firstname"].replace("", DEFAULT_FIRSTNAME)
        patient_df["patient_lastname"] = patient_df["patient_lastname"].replace("", DEFAULT_LASTNAME)

        return dict(zip(patient_df["id_patient"], zip(patient_df["patient_firstname"], patient_df["patient_lastname"])))
    except Exception as exception:
        print(f"Warnung: Konnte Patientendaten nicht laden: {exception}")
        return {}