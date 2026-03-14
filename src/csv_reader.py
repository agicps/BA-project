import pandas as pd


def load_csv(csv_path, required_columns):
    
    # Error if one or more required Spalten are not in the file.
    
    df = pd.read_csv(csv_path)

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[required_columns].copy()

    df["questionnaire_answer_date"] = pd.to_datetime(
        df["questionnaire_answer_date"], errors="coerce"
    )

    df["answer_day"] = df["questionnaire_answer_date"].dt.date

    return df
