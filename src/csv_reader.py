import pandas as pd


def load_csv(csv_path, required_columns):
    
    # Fehler falls die Datei nicht gefunden wird
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found")

    # die Spalte mit dem Zeitstempel (in String Format) wird eine datetime Spalte
    # also wir formatieren es so dass es zum Datum Datentyp wird
    df["questionnaire_answer_date"] = pd.to_datetime(
        df["questionnaire_answer_date"], errors="coerce"
    )
    # eine neue Spalte, die nur das Datum enthält (und ohne Uhrzeit), damit wir später nach dem Tag gruppieren können
    df["answer_day"] = df["questionnaire_answer_date"].dt.date

    return df
