FACIT_ALL_ITEMS = {
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
}


FACIT_DIRECT_ITEMS = {
	"Ich habe Energie.",
	"Ich bin in der Lage meinen gewohnten Aktivitäten nachzugehen (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).",
}


def calculate_facit_score(group, facit_title):
	if group["questionnaire_title"] != facit_title:
		return None

	item_score_sum = 0
	answered_count = 0

	for answer in group["answers"]:
		question = answer.get("question")
		if question not in FACIT_ALL_ITEMS:
			continue

		try:
			value = int(answer.get("value"))
		except (TypeError, ValueError):
			continue

		if value < 0 or value > 4:
			continue

		if question in FACIT_DIRECT_ITEMS:
			item_score = value
		else:
			item_score = 4 - value

		item_score_sum += item_score
		answered_count += 1

	if answered_count == 0:
		return None

	if answered_count < 13:
		score = item_score_sum * 13 / answered_count
	else:
		score = item_score_sum

	return {
		"date": group["date"],
		"score": score,
	}


def build_facit_patient_scores(groups, facit_title):
	patient_scores = {}

	for group in groups:
		facit_score = calculate_facit_score(group, facit_title)
		if facit_score is None:
			continue

		patient_id = group["id_patient"]
		patient_scores.setdefault(patient_id, {}).setdefault(facit_title, []).append(
			facit_score
		)

	for patient_id in patient_scores:
		patient_scores[patient_id][facit_title].sort(key=lambda entry: entry["date"])

	return patient_scores
