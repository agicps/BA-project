from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def create_patient_pdf(
	patient_id,
	questionnaire_title,
	chart_path,
	interpretation_note,
	output_pdf_path,
):
	pdf = canvas.Canvas(str(output_pdf_path), pagesize=A4)
	page_width, page_height = A4

	left_margin = 50
	right_margin = 50
	top_margin = 60
	content_width = page_width - left_margin - right_margin

	title_y = page_height - top_margin
	patient_y = title_y - 24
	section_y = patient_y - 28

	pdf.setFont("Helvetica-Bold", 18)
	pdf.drawString(left_margin, title_y, "DigiCare Patientenbericht")

	pdf.setFont("Helvetica", 12)
	pdf.drawString(left_margin, patient_y, f"Patient: {patient_id}")

	pdf.setFont("Helvetica-Bold", 13)
	pdf.drawString(left_margin, section_y, questionnaire_title)

	image_top_y = section_y - 20
	bottom_reserved = 130
	max_image_height = image_top_y - bottom_reserved

	image_reader = ImageReader(str(chart_path))
	image_width, image_height = image_reader.getSize()

	width_scale = content_width / image_width
	height_scale = max_image_height / image_height
	scale = min(width_scale, height_scale, 1.0)

	draw_width = image_width * scale
	draw_height = image_height * scale

	image_x = left_margin + (content_width - draw_width) / 2
	image_y = image_top_y - draw_height

	pdf.drawImage(
		image_reader,
		image_x,
		image_y,
		width=draw_width,
		height=draw_height,
		preserveAspectRatio=True,
		mask="auto",
	)

	note_y = image_y - 28
	pdf.setFont("Helvetica", 11)
	pdf.drawString(left_margin, note_y, str(interpretation_note))

	pdf.showPage()
	pdf.save()
