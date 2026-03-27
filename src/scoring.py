# Facit Fragen
# hier Set gut, weil wir oft einfach einfach nur prüfen
facitCalcQuestions = [
	"Ich bin erschöpft.",
	"Ich fühle mich insgesamt schwach.",
	"Ich fühle mich lustlos (ausgelaugt).",
	"Ich bin müde.",
	"Es fällt mir schwer, etwas anzufangen, weil ich müde bin.",
	"Es fällt mir schwer, etwas zu Ende zu führen, weil ich müde bin.",
	"Ich habe Energie.",
	"Ich bin in der Lage meinen gewohnten Aktivitäten nachzugehen (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).",
	"Ich habe das Bedürfnis, tagsüber zu schlafen.",
	"Ich bin zu müde, um zu essen.",
	"Ich brauche Hilfe bei meinen gewohnten Aktivitäten (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).",
	"Ich bin frustriert, weil ich zu müde bin, die Dinge zu tun, die ich machen möchte.",
	"Ich musste meine sozialen Aktivitäten einschränken, weil ich müde bin.",
]

# hier bei diesen Fragen wird nichts extra aufsummiert
facitDirectQuestions = [
	"Ich habe Energie.",
	"Ich bin in der Lage meinen gewohnten Aktivitäten nachzugehen (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).",
]

# Übelkeit & Erbrechen Fragen
uebelkeitQuestions = ["Häufigkeit: Wie häufig müssen Sie am Tag erbrechen?"]

# PG-SGA SF Fragen
pgsgaMainQuestions = [
	"In den vergangenen zwei Wochen hat sich mein Gewicht:",
	"Im Vergleich zu meiner normalen Nahrungsaufnahme würde ich diese im vergangenen Monat wie folgt bewerten:",
	"Derzeit nehme ich folgende Nahrung auf:",
	"Mein Aktivitätsniveau in den letzten vier  Wochen würde ich allgemein wie folgt bewerten:",
	"Bei mir traten die folgenden Probleme auf, die mich in den vergangenen zwei Wochen davon abgehalten haben, ausreichend zu essen (alles Zutreffende ankreuzen):"
]

# die pgsga Fragen, die den Punkt nur im Fragebogen, aber nicht in d. csv datei haben
pgsgaOptionalQuestions = [
	"Wenn Schmerzen, wo?",
	"Wenn Sonstiges, was?"
] 

omdqMainQuestions = [
	"1. Wie würden Sie Ihre allgemeine Befindlichkeit in den letzten 24 Stunden einschätzen?",
	"2. Wie stark waren Ihre Mund- und Rachenschmerzen in den letzten 24 Stunden?",
	"4. Wie stark hatten Sie in den letzten 24 Stunden Durchfall?"
]

omdqOptionalQuestions = ["3. Wie stark schränkte Sie der Mund- und Rachenschmerz in den letzten 24 Stunden bei den folgenden Tätigkeiten ein?"]


# Die Oberfunktion berrechnet für jede Session einen Score, pflegt für jeden Patienten eine scoreliste für jeden Fragebogen (Datum dabei), dabei wird beachtet, dass maximal GraphPunkteAnzahl scores in der Liste sein dürfen

# jetzt kommen die ganzen Berechnungsfunktionen dran

# Jede Score Funktion kriegt eine Session

# Übelkeit & Erbrechen Funktion:
def uebelkeitScoreCalculator(session):
	if session["questionnaire_title"] == "Übelkeit/Erbrechen":
		answers = session["answers"]
		for a in answers:
			if a["question_title"] in uebelkeitQuestions: # nur wenn es die eine frage ist
				if (a["value"] == "keinErbrechen"):
					return {"id_patient":session["id_patient"],"questionnaire_title":session["questionnaire_title"],"date":session["date"], "score":0}
				elif (a["value"] == "12XProTag"):
					return {"id_patient":session["id_patient"],"questionnaire_title":session["questionnaire_title"],"date":session["date"], "score":1}
				elif (a["value"] == "35XProTag"):
					return {"id_patient":session["id_patient"],"questionnaire_title":session["questionnaire_title"],"date":session["date"], "score":2}
				elif (a["value"] == "6XProTag"): #gibt es in csv export noch nicht also nehmen wir an der value heißt so
					return {"id_patient":session["id_patient"],"questionnaire_title":session["questionnaire_title"],"date":session["date"], "score":3}
	return None


# Facit Score Funktion:
def facitScoreCalculator(session):
	amountAnsweredQuestions = session["answers"].len()
	sum = 0
	for a in session["answers"]:
		if a in facitCalcQuestions:
			sum = sum + 4 - a["value"]
		elif a in facitDirectQuestions:
			sum = sum + a["value"]

	if amountAnsweredQuestions < 13:
		sum = (sum * 13)/amountAnsweredQuestions

	return {"id_patient":session["id_patient"],"questionnaire_title":session["questionnaire_title"],"date":session["date"], "score":sum}


# PGSGA Score Funktion:
def pgsgaScoreCalculator(session):
	