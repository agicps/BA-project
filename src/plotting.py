import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.transforms import blended_transform_factory


def create_line_chart(
	messpunkte,
	questionnaire_title,
	y_axis_label,
	y_min,
	y_max,
	cutoff,
	cutoff_label,
	output_path,
	max_points=8,
):
	def get_point_date(point):
		return _parse_entry_date(point["date"])
	
	sorted_points = sorted(messpunkte, key=get_point_date)

	if len(sorted_points) > max_points:
		sorted_points = sorted_points[-max_points:]

	x_values = list(range(1, len(sorted_points) + 1))
	x_labels = [point["date"] for point in sorted_points]
	y_values = [point["score"] for point in sorted_points]

	fig, ax = plt.subplots()
	ax.plot(x_values, y_values, marker="o", linestyle="-")

	ax.set_title(questionnaire_title, fontsize=16)
	ax.set_xlabel("")
	ax.set_ylabel(y_axis_label)
	ax.set_ylim(y_min, y_max)
	ax.set_xticks(x_values)
	ax.set_xticklabels(x_labels)
	ax.set_xlim(0.5, max(len(sorted_points), 1) + 0.5)

	ax.axhline(y=cutoff, linestyle="--", label=cutoff_label)
	ax.legend()

	ax.tick_params(axis="x", rotation=30)

	fig.tight_layout()
	fig.savefig(output_path, format="png")
	plt.close(fig)


def get_questionnaire_plot_title(questionnaire_title):
	title_map = {
		"FACIT-Erschöpfung": "FACIT Fatigue Score",
		"OMDQ": "OMDQ Score",
		"PG-SGA SF | Patientenbezogenes Ernährungsassesment": "PG-SGA Score",
		"Übelkeit/Erbrechen": "Übelkeit Score",
	}
	return title_map.get(questionnaire_title, questionnaire_title)


def interpret_facit(score):
	if score <= 21:
		return {
			"cutoff": 21,
			"color": "#d62728",
			"text": "Bitte informieren Sie bei Ihrem nächsten Termin hierzu das Behandlungsteam, wenn der Wert unter 22 liegt",
		}
	if score <= 30:
		return {
			"cutoff": 30,
			"color": "#ff7f0e",
			"text": "Bitte informieren Sie bei Ihrem nächsten Termin hierzu das Behandlungsteam, wenn der Wert unter 31 liegt",
		}
	if score <= 40:
		return {
			"cutoff": 40,
			"color": "#aba640",
			"text": "Information an APN und Patient, wenn der der Wert unter 41 liegt",
		}
	return {
		"cutoff": 41,
		"color": "#2e7d32",
		"text": "Keine Intervention, wenn der Wert über 40 liegt",
	}


def interpret_omdq(score):
	if score >= 3:
		return {
			"cutoff": 3,
			"color": "#d62728",
			"text": "Wir empfehlen Ihnen zeitnah das Behandlungsteam zu kontaktieren, wenn der Wert bei 3 oder höher liegt",
		}
	if score >= 2:
		return {
			"cutoff": 2,
			"color": "#ff7f0e",
			"text": "Information an APN und Patient, wenn der Wert bei 2 oder höher liegt",
		}
	return {
		"cutoff": 1,
		"color": "#2e7d32",
		"text": "Keine Intervention bei einem Wert bis 1",
	}


def interpret_pgsga(score):
	if score >= 9:
		return {
			"cutoff": 9,
			"color": "#d62728",
			"text": "Wir empfehlen Ihnen zeitnah das Behandlungsteam zu kontaktieren, wenn der Wert bei 9 oder höher liegt",
		}
	if score >= 4:
		return {
			"cutoff": 4,
			"color": "#ff7f0e",
			"text": "Bitte informieren Sie bei Ihrem nächsten Termin hierzu das Behandlungsteam, wenn der Wert bei 4 oder höher liegt",
		}
	if score >= 2:
		return {
			"cutoff": 2,
			"color": "#aba640",
			"text": "Information an APN und Patient, wenn der Wert bei 2 oder höher liegt",
		}
	return {
		"cutoff": 1,
		"color": "#2e7d32",
		"text": "Keine Intervention bei einem Wert bis 1",
	}


def interpret_uebelkeit(score):
	if score >= 3:
		return {
			"cutoff": 3,
			"color": "#d62728",
			"text": "Wir empfehlen Ihnen zeitnah das Behandlungsteam zu kontaktieren, wenn der Wert zwischen 3 und 4 liegt",
		}
	if score >= 2:
		return {
			"cutoff": 2,
			"color": "#ff7f0e",
			"text": "Bitte informieren Sie bei Ihrem nächsten Termin hierzu das Behandlungsteam, wenn der Wert bei 2 liegt",
		}
	if score >= 1:
		return {
			"cutoff": 1,
			"color": "#aba640",
			"text": "Information an APN und Patient, wenn der Wert bei 1 liegt",
		}
	return {
		"cutoff": 0,
		"color": "#2e7d32",
		"text": "Keine Intervention bei einem Wert unter 1",
	}


def _parse_entry_date(date_value):
	if isinstance(date_value, datetime):
		return date_value

	if isinstance(date_value, str):
		date_formats = [
			"%Y-%m-%d",
			"%Y-%m-%d %H:%M:%S",
			"%Y-%m-%dT%H:%M:%S",
			"%d.%m.%Y",
			"%d.%m.%Y %H:%M:%S",
		]

		for fmt in date_formats:
			try:
				return datetime.strptime(date_value, fmt)
			except ValueError:
				continue

		try:
			return datetime.fromisoformat(date_value.replace("Z", "+00:00"))
		except ValueError:
			pass

	return date_value


def _sort_entry_by_date(entry):
	return _parse_entry_date(entry["date"])


def _y_achsen_einstellung(questionnaire_title):
	if questionnaire_title == "FACIT-Erschöpfung":
		return 0, 52
	if questionnaire_title == "PG-SGA SF | Patientenbezogenes Ernährungsassesment":
		return 0, 34
	if questionnaire_title == "OMDQ":
		return 0, 6
	if questionnaire_title == "Übelkeit/Erbrechen":
		return 0, 6
	return 0, 10


def _get_plot_size(questionnaire_title):
	if questionnaire_title == "FACIT-Erschöpfung":
		return 16, 5.2
	return 16, 4.2


def plot_patient_questionnaire_scores(patient_id, questionnaire_title, score_entries):
	sorted_entries = sorted(score_entries, key=_sort_entry_by_date)
	if len(sorted_entries) > 8:
		sorted_entries = sorted_entries[-8:]

	x_values = list(range(1, len(sorted_entries) + 1))
	y_values = [entry["score"] for entry in sorted_entries]
	x_labels = [entry["date"] for entry in sorted_entries]

	plot_width, plot_height = _get_plot_size(questionnaire_title)
	fig, ax = plt.subplots(figsize=(plot_width, plot_height))
	ax.plot(x_values, y_values, marker="o", linestyle="-", color="#1f77b4", linewidth=2)

	ax.set_title(get_questionnaire_plot_title(questionnaire_title), fontsize=16)
	ax.set_xlabel("")
	ax.set_ylabel("Score")
	y_min, y_max = _y_achsen_einstellung(questionnaire_title)
	ax.set_ylim(y_min, y_max)
	ax.set_yticks(list(range(y_min, y_max + 1, 2)))
	ax.set_xticks(x_values)
	ax.set_xlim(0.5, max(len(sorted_entries), 1) + 0.5)

	formatted_labels = []
	for date_value in x_labels:
		parsed_date = _parse_entry_date(date_value)
		if isinstance(parsed_date, datetime):
			formatted_labels.append(parsed_date.strftime("%d.%m."))
		else:
			formatted_labels.append(str(date_value))
	ax.set_xticklabels(formatted_labels)
	ax.tick_params(axis="x", rotation=45)

	if questionnaire_title == "FACIT-Erschöpfung":
		reference_score = min(y_values)
		interpretation = interpret_facit(reference_score)
	elif questionnaire_title == "OMDQ":
		reference_score = max(y_values)
		interpretation = interpret_omdq(reference_score)
	elif questionnaire_title == "PG-SGA SF | Patientenbezogenes Ernährungsassesment":
		reference_score = max(y_values)
		interpretation = interpret_pgsga(reference_score)
	elif questionnaire_title == "Übelkeit/Erbrechen":
		reference_score = max(y_values)
		interpretation = interpret_uebelkeit(reference_score)
	else:
		interpretation = {
			"cutoff": y_values[-1],
			"color": "#6c757d",
			"text": "-",
		}

	ax.axhline(
		y=interpretation["cutoff"],
		linestyle="--",
		linewidth=1.8,
		color=interpretation["color"],
	)

	text_transformierung = blended_transform_factory(ax.transAxes, ax.transData)
	ax.text(
		1.01,
		interpretation["cutoff"],
		interpretation["text"],
		transform=text_transformierung,
		va="center",
		ha="left",
		fontsize=9,
		color=interpretation["color"],
	)

	ax.grid(alpha=0.2)
	fig.tight_layout(rect=[0, 0, 0.86, 1])
	return fig
