import pandas as pd


def load_csv(csv_path, required_columns):
    
    # Error falls die Datei nicht gefunden wird
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found")
    
    # Error falls eine oder mehrere required Spalten nicht in der Datei sind
    missing = []

    for column in required_columns:
        if column not in df.columns:
            missing.append(column)

    # wenn missing nicht leer ist (d.h. wenn es fehlende Spalten gibt), dann werfen wir einen Error 
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # wenn alle notwendigen Spalten da sind, dann nehmen wir nur die und machen eine copy vom DataFrame, damit wir den Original DataFrame nicht verändern
    df = df[required_columns].copy()

    # wir nehmen die spalte mit dem Zeitstempel (in String Format) und machen daraus eine datetime Spalte, damit wir damit arbeiten können
    df["questionnaire_answer_date"] = pd.to_datetime(
        df["questionnaire_answer_date"], errors="coerce"
    )
    # wir machen eine neue Spalte, die nur das Datum enthält (ohne Uhrzeit), damit wir später nach Tag gruppieren können
    df["answer_day"] = df["questionnaire_answer_date"].dt.date

    return df


