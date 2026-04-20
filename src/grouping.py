import pandas as pd
# hier legen wir fest wie aus den CSV-Zeilen eine Ausfüllung wird
# also wir bündeln einzelne Antworten zu einer zusammenhängenden Ausfüllung eines Fragebogens
# mit diesen Bündelungen können später die Scores berechnet werden

# eine Ausfüllung wird bei mir definiert durch:
    # id_patient
    # questionnaire_title
    # das Datum (hier beachten wir nur den Tag)



# diese Funktion filtert irrelevante Zeilen raus
# d.h. nur relevante Fragebögen, und Zeilen die NOT_STARTED oder IN_PROGRESS sind raus
# csv ist in Form eines DataFrames, relevant_questionnaires ist eine Liste
#
def filter_relevante_zeilen(csv_df, relevant_questionnaires):
    filtered_df = csv_df[
            csv_df["questionnaire_title"].isin(relevant_questionnaires)
            & ~csv_df["questionnaire_reply_status"].isin(["NOT_STARTED","IN_PROGRESS"])
    ].copy()
    # wir machen eine copy vom gefilterten DataFrame, weil das für pandas empfohlen wird
    return filtered_df


def filter_relevant_rows(csv_df, relevant_questionnaires):
    return filter_relevante_zeilen(csv_df, relevant_questionnaires)



# diese Funktion macht aus den einzelnen Antwortzeilen(eines DataFrames) eine zusammenhängende Ausfüllung (pro Tag)
def group_responses(csv_df):

    # wir gruppieren den dataframe nach Patient, Fragebogen und Tag
    groups = csv_df.groupby(["id_patient", "questionnaire_title", "answer_day"])
    # mit groupby bekommt man dann den Gruppenschlüssel also (id_patient, questionnaire_title, answer_day) 
    # und die zugehörige Teiltabelle(group) (also die Zeilen die zu diesem Schlüssel gehören)

    # hier speichern wir die fertigen Ausfüllungen
    # gruppiert nach Patient, Fragebogen und Tag
    # jede Ausfüllung ist ein Dictionary mit daten zur Ausfüllung 
    # und einer answers-Liste, die einzelne Fragebeantwortungen als Dictionaries enthält.
    alleAntworten = [] 

    # wir iterieren über die Gruppen
    for (id_patient, questionnaire_title, answer_day), group in groups:
        sessionAntworten = []
        # wir iterieren über die Zeilen der Gruppe, um die Antworten zu sammeln
        # iterrows gibt uns zeilen zurück
        # mit jedem Durchlauf bauen wir für eine Antwortzeile ein Dictionary
        for index, row in group.iterrows():
            antwort = {
                "question_title": row["questionnaire_question"],
                "value": row["questionnaire_answer_value"],
                "type": row["questionnaire_answer_type"],
                "reply_status": row["questionnaire_reply_status"],
            }
            sessionAntworten.append(antwort)
        

        alleAntworten.append(
            # hier ist jeweils eine Ausfüllung
            {
                "id_patient": id_patient,
                "questionnaire_title": questionnaire_title,
                "date": answer_day,
                "answers": sessionAntworten,
            }
        )

    return alleAntworten

# also wir geben die csv data frame ein, dann gruppieren wir über die Spalten patient,fragebogentitel und Tag 
# d.h. jede Gruppe hat eindeutige Werte für Patient, Fragebogen, Titel
# und jede Gruppe ist eine Teiltabelle, die diesen Werten entspricht
# dann teilen wir das dataframe (d.h. die Teiltabelle) in zeilen auf mit iterrows
# bzw. wir iterieren damit durch die zeilen des dataframes
# und für jede Zeile erstellen wir eine Antwort Dictionary(antwort), die für jede Antwort der Gruppe Informationen speichert die wir später fürs scoring brauchen
# die antworten (in Form von dictionnaires) zu einer Ausfüllung speichern wir dann in einer Liste (sessionAntworten)
# dann fügen wir die Sammlung der Antworten und die Daten dieser Gruppe zu einer großen Liste(alleAntworten) hinzu.
# # in der Liste speichern wir dann immer eine Ausfüllung (die annahme war ja das ein Fragebögen max. einmal täglich ausgefüllt werden kann)
# und dort können wir nach Patient, Fragebogen und Datum identifizieren, und dann haben wir dazu jeweils zugriff auf die gespeicherten Antworten 