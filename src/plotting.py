import matplotlib.pyplot as plt


def create_line_chart(
	messpunkte,
	questionnaire_title,
	y_axis_label,
	y_min,
	y_max,
	cutoff,
	cutoff_label,
	output_path,
	max_points=10,
):
	sorted_points = sorted(messpunkte, key=lambda point: point["date"])

	if len(sorted_points) > max_points:
		sorted_points = sorted_points[-max_points:]

	x_values = [point["date"] for point in sorted_points]
	y_values = [point["score"] for point in sorted_points]

	fig, ax = plt.subplots()
	ax.plot(x_values, y_values, marker="o", linestyle="-")

	ax.set_title(questionnaire_title)
	ax.set_xlabel("Datum")
	ax.set_ylabel(y_axis_label)
	ax.set_ylim(y_min, y_max)
	ax.set_xticks(x_values)
	ax.set_xticklabels(x_values)

	ax.axhline(y=cutoff, linestyle="--", label=cutoff_label)
	ax.legend()

	ax.tick_params(axis="x", rotation=30)

	fig.tight_layout()
	fig.savefig(output_path, format="png")
	plt.close(fig)
