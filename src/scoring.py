from config import questionnaires

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


def _normalize_facit_value(raw_value):
	if raw_value is None:
		return None

	if isinstance(raw_value, int):
		return raw_value

	value_str = str(raw_value).strip()
	if value_str.isdigit():
		return int(value_str)

	normalized = value_str.lower().replace(" ", "")
	value_map = {
		"uberhauptnicht": 0,
		"überhauptnicht": 0,
		"einwenig": 1,
		"massig": 2,
		"ziemlich": 3,
		"sehr": 4,
	}
	return value_map.get(normalized)

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
	if session["questionnaire_title"] == questionnaires["uebelkeit"]:
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
	if session["questionnaire_title"] == questionnaires["facit"]:

		answeredQuestions = {}
		for a in session["answers"]:
			value = _normalize_facit_value(a["value"])
			if value is None:
				continue

			if a["question_title"] in facitCalcQuestions:
				answeredQuestions.setdefault(a["question_title"], 4 - value)
			elif a["question_title"] in facitDirectQuestions:
				answeredQuestions.setdefault(a["question_title"], value)

		totalScore = sum(answeredQuestions.values())
		amountAnsweredQuestions = len(answeredQuestions)

		if (amountAnsweredQuestions > 0) and (amountAnsweredQuestions < 13):
			totalScore = (totalScore * 13) / amountAnsweredQuestions
			totalScore = round(totalScore, 2)

		return {"id_patient":session["id_patient"],"questionnaire_title":session["questionnaire_title"],"date":session["date"], "score":totalScore}
	return None
	


# PGSGA Score Funktion:
def pgsgaScoreCalculator(session):
	if session["questionnaire_title"] == questionnaires["pgsga"]:
		sum = 0
		symptomQuestion = "Bei mir traten die folgenden Probleme auf, die mich in den vergangenen zwei Wochen davon abgehalten haben, ausreichend zu essen (alles Zutreffende ankreuzen):"
		for a in session["answers"]:
			if a["question_title"] == symptomQuestion and (a["value"]) == "true":
				sum = sum + int(a["type"])
			elif a["question_title"] in pgsgaMainQuestions:
				# Some exports contain non-numeric placeholders like false/NULL for unanswered items.
				if a["value"] in ("false", "NULL", "", None):
					continue
				sum = sum + int(a["value"])
			elif a["question_title"] in pgsgaOptionalQuestions and a["value"] != "keine" and a["value"] != "NULL":
				sum = sum + pgsgaOptionalQuestions[a["question_title"]]
		return {"id_patient":session["id_patient"],"questionnaire_title":session["questionnaire_title"],"date":session["date"], "score":sum}
	return None


# OMDQ Score Funktion:
def omdqScoreCalculator(session):
	if session["questionnaire_title"] == questionnaires["omdq"]:
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



def mainScoreCalculator(sessions):
	patientScores = {}

	for session in sessions:
		questionnaireTitle = session["questionnaire_title"]

		if questionnaireTitle == questionnaires["facit"]:
			scoreEntry = facitScoreCalculator(session)
		elif questionnaireTitle == questionnaires["uebelkeit"]:
			scoreEntry = uebelkeitScoreCalculator(session)
		elif questionnaireTitle == questionnaires["pgsga"]:
			scoreEntry = pgsgaScoreCalculator(session)
		elif questionnaireTitle == questionnaires["omdq"]:
			scoreEntry = omdqScoreCalculator(session)
		else:
			raise ValueError(f"Nicht unterstützter Fragebogentitel: {questionnaireTitle}")

		if scoreEntry is None:
			raise ValueError(f"Score-Kalkulator für Fragebogen '{questionnaireTitle}' hat None für Patient {session['id_patient']} zurückgegeben")

		patientId = scoreEntry["id_patient"]
		entryQuestionnaireTitle = scoreEntry["questionnaire_title"]

		if patientId not in patientScores:
			patientScores[patientId] = {}

		if entryQuestionnaireTitle not in patientScores[patientId]:
			patientScores[patientId][entryQuestionnaireTitle] = []

		patientScores[patientId][entryQuestionnaireTitle].append(scoreEntry)

	return patientScores


def facitRelevantChange(facitScoreList):
	if len(facitScoreList) < 2:
		return None

	def parseDate(dateValue):
		from datetime import datetime

		if isinstance(dateValue, datetime):
			return dateValue

		if isinstance(dateValue, str):
			dateFormats = [
				"%Y-%m-%d",
				"%Y-%m-%d %H:%M:%S",
				"%Y-%m-%dT%H:%M:%S",
				"%d.%m.%Y",
				"%d.%m.%Y %H:%M:%S",
			]

			for fmt in dateFormats:
				try:
					return datetime.strptime(dateValue, fmt)
				except ValueError:
					continue

			try:
				return datetime.fromisoformat(dateValue.replace("Z", "+00:00"))
			except ValueError:
				return dateValue

		return dateValue

	def get_date(entry):
		return parseDate(entry["date"])

	sortedEntries = sorted(facitScoreList, key=get_date)
	earliestScore = sortedEntries[0]["score"]
	latestScore = sortedEntries[-1]["score"]
	differenz = latestScore - earliestScore

	if differenz >= 8:
		return "Clinically meaningful improvement"
	if 5 <= differenz < 8:
		return "Possible improvement"
	if differenz <= -5:
		return "Worsening"
	return "No relevant change"
	