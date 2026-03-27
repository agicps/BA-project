# Facit Fragen
# hier Set gut, weil wir oft einfach einfach nur prüfen
facitCalcQuestions = [
	"Ich bin erschöpft.",
	"Ich fühle mich insgesamt schwach.",
	"Ich fühle mich lustlos (ausgelaugt).",
	"Ich bin müde.",
	"Es fällt mir schwer, etwas anzufangen, weil ich müde bin.",
	"Es fällt mir schwer, etwas zu Ende zu führen, weil ich müde bin.",
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
pgsgaOptionalQuestions = {
	"Wenn Schmerzen, wo?" : 3,
	"Wenn Sonstiges, was?" : 1
} 

omdqQuestionOne = "1. Wie würden Sie Ihre allgemeine Befindlichkeit in den letzten 24 Stunden einschätzen?"
omdqQuestionTwo = "2. Wie stark waren Ihre Mund- und Rachenschmerzen in den letzten 24 Stunden?"
omdqQuestionFour = "4. Wie stark hatten Sie in den letzten 24 Stunden Durchfall?"

omdqQuestionThree = "3. Wie stark schränkte Sie der Mund- und Rachenschmerz in den letzten 24 Stunden bei den folgenden Tätigkeiten ein?"


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
	if session["questionnaire_title"] == "FACIT-Erschöpfung":

		amountAnsweredQuestions = 0
		sum = 0
		for a in session["answers"]:
			if a["question_title"] in facitCalcQuestions:
				sum = sum + 4 - int(a["value"]) #konvertieren string zu int
				amountAnsweredQuestions = amountAnsweredQuestions + 1
			elif a["question_title"] in facitDirectQuestions:
				sum = sum + int(a["value"])
				amountAnsweredQuestions = amountAnsweredQuestions + 1

		if (amountAnsweredQuestions > 0) and (amountAnsweredQuestions < 13):
			sum = (sum * 13) / amountAnsweredQuestions
			sum = round(sum, 2)

		return {"id_patient":session["id_patient"],"questionnaire_title":session["questionnaire_title"],"date":session["date"], "score":sum}
	return None
	


# PGSGA Score Funktion:
def pgsgaScoreCalculator(session):
	if session["questionnaire_title"] == "PG-SGA SF | Patientenbezogenes Ernährungsassesment":
		sum = 0
		for a in session["answers"]:
			if a["question_title"] == "Bei mir traten die folgenden Probleme auf, die mich in den vergangenen zwei Wochen davon abgehalten haben, ausreichend zu essen (alles Zutreffende ankreuzen):" and (a["value"]) == "true":
				sum = sum + int(a["type"])
			elif a["question_title"] in pgsgaMainQuestions: 
				sum = sum + int(a["value"])
			elif a["question_title"] in pgsgaOptionalQuestions and a["value"] != "keine" and a["value"] != "NULL":
				sum = sum + pgsgaOptionalQuestions[a["question_title"]]
		return {"id_patient":session["id_patient"],"questionnaire_title":session["questionnaire_title"],"date":session["date"], "score":sum}
	return None

# OMDQ Score Funktion:
def omdqScoreCalculator(session):
	if session["questionnaire_title"] == "OMDQ":
		sum = 0
		amountAnsweredQuestions = 0

		for a in session["answers"]:
			if a["question_title"] == omdqQuestionOne:
				sum = sum + int(a["value"])
				amountAnsweredQuestions = amountAnsweredQuestions + 1
			elif a["question_title"] == omdqQuestionTwo:
				amountAnsweredQuestions = amountAnsweredQuestions + 1
				if a["value"] == "keineSchmerzen":
					sum = sum + 0
				elif a["value"] == "einWenigSchmerzen":
					sum = sum + 1
				elif a["value"] == "massigeSchmerzen":
					sum = sum + 2
				elif a["value"] == "starkeSchmerzen":
					sum = sum + 3
				elif a["value"] == "extremeSchmerzen":
					sum = sum + 4
			elif a["question_title"] == omdqQuestionThree:
				amountAnsweredQuestions = amountAnsweredQuestions + 1
				if a["value"] == "keineEinschrankung":
					sum = sum + 0
				elif a["value"] == "leichteEinschrankung":
					sum = sum + 1
				elif a["value"] == "massigeEinschrankung":
					sum = sum + 2
				elif a["value"] == "starkeEinschrankung":
					sum = sum + 3
				elif a["value"] == "nichtMoglich":
					sum = sum + 4
			elif a["question_title"] == omdqQuestionFour:
				amountAnsweredQuestions = amountAnsweredQuestions + 1
				if a["value"] == "keinDurchfall":
					sum = sum + 0
				elif a["value"] == "einWenigDurchfall":
					sum = sum + 1
				elif a["value"] == "mssigerDurchfall":
					sum = sum + 2
				elif a["value"] == "starkerDurchfall":
					sum = sum + 3
				elif a["value"] == "extremerDurchfall":
					sum = sum + 4

		if sum != 0:
			sum = sum / amountAnsweredQuestions
			sum = round(sum, 2)
			return {"id_patient":session["id_patient"],"questionnaire_title":session["questionnaire_title"],"date":session["date"], "score":sum}
	
	return None



def mainScoreCalculator(alleAntworten):
	