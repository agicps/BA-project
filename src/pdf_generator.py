from io import BytesIO
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

from config import relevantQuestionnaires

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 45
MARGIN_RIGHT = 45
MARGIN_TOP = 50
MARGIN_BOTTOM = 45
SPACE_BETWEEN_CHARTS = 16
MAX_CHART_HEIGHT = 220
HEADER_TEXT = "DigiCare Patientenbericht"
HEADER_FONT_SIZE = 18
HEADER_INFO_FONT_SIZE = 12

def create_plot_image(patient_id, questionnaire_title, score_entries):
    """
    Erstellt ein Diagramm (Plot) für einen Fragebogen.
    
    Parameter:
        patient_id: Die Patienten-ID
        questionnaire_title: Der Name vom Fragebogen
        score_entries: Die Datenpunkte zum Zeichnen
    
    Gibt zurück:
        Ein Matplotlib-Diagramm
    """
    import plotting

    if hasattr(plotting, "create_questionnaire_plot"):
        return plotting.create_questionnaire_plot(patient_id, questionnaire_title, score_entries)
    
    return plotting.plot_patient_questionnaire_scores(patient_id, questionnaire_title, score_entries)


def convert_plot_to_pdf_image(plot_figure):
    """
    Wandelt ein Matplotlib-Diagramm in einen Bild um, das ins PDF passt.
    
    Parameter:
        plot_figure: Das Matplotlib-Diagramm
    
    Gibt zurück:
        (Das Bild im PDF-Format, Der Speicheruffer)
    """
    image_buffer = BytesIO()
    
    plot_figure.savefig(image_buffer, format="png", dpi=150)
    
    image_buffer.seek(0)
    
    return ImageReader(image_buffer), image_buffer


def draw_page_header(pdf_document, patient_id, position_y, patient_data_dict=None):
    """
    Zeichnet die Kopfzeile auf die Seite.
    Kopfzeile = Titel + Patienteninfo oben auf der Seite
    
    Parameter:
        pdf_document: Das PDF-Dokument zum Zeichnen
        patient_id: Die Patienten-ID
        position_y: Die Y-Position (wie weit oben)
        patient_data_dict: Dictionary mit patient_id -> (firstname, lastname) Mapping
    
    Gibt zurück:
        Die neue Y-Position nach der Kopfzeile
    """
    pdf_document.setFont("Helvetica-Bold", HEADER_FONT_SIZE)
    pdf_document.drawString(MARGIN_LEFT, position_y, HEADER_TEXT)
    
    pdf_document.setFont("Helvetica", HEADER_INFO_FONT_SIZE)
    info_position_y = position_y - 24
    
    if patient_data_dict and patient_id in patient_data_dict:
        firstname, lastname = patient_data_dict[patient_id]
        patient_display = f"{firstname} {lastname}"
    else:
        patient_display = patient_id
    
    pdf_document.drawString(MARGIN_LEFT, info_position_y, f"Patient: {patient_display}")
    
    return info_position_y - 18


def get_questionnaires_in_order(questionnaire_list):
    """
    Sortiert die Fragebögen in der richtigen Reihenfolge.
    
    Zuerst: Die Fragebögen aus der Konfiguration (in dieser Reihenfolge)
    Dann: Alle anderen Fragebögen (alphabetisch)
    
    Parameter:
        questionnaire_list: Eine Liste aller vorhandenen Fragebogennamen
    
    Gibt zurück:
        Die sortierte Liste
    """
    sorted_questionnaires = []
    
    for title in relevantQuestionnaires:
        if title in questionnaire_list:
            sorted_questionnaires.append(title)
    
    for title in sorted(questionnaire_list):
        if title not in sorted_questionnaires:
            sorted_questionnaires.append(title)
    
    return sorted_questionnaires


def calculate_image_size(original_width, original_height):
    """
    Berechnet die richtige Größe für das Bild in PDF.
    Das Bild soll passen aber nicht zu klein sein.
    
    Parameter:
        original_width: Die ursprüngliche Breite von Bild
        original_height: Die ursprüngliche Höhe von Bild
    
    Gibt zurück:
        (neue_breite, neue_höhe)
    """
    available_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    
    scale_for_width = available_width / original_width
    scale_for_height = MAX_CHART_HEIGHT / original_height
    
    final_scale = min(scale_for_width, scale_for_height, 1.0)
    
    new_width = original_width * final_scale
    new_height = original_height * final_scale
    
    return new_width, new_height


# ===== HAUPTFUNKTION =====

def create_patient_pdf(patient_id, questionnaire_scores, output_dir, patient_data_dict=None):
    """
    Erstellt ein PDF mit den Fragebogenergebnissen eines Patienten.
    
    Parameter:
        patient_id: Die eindeutige Patienten-ID
        questionnaire_scores: Ein Dictionary mit allen Fragebogenergebnissen
        output_dir: Der Pfad, wo das PDF gespeichert werden soll
        patient_data_dict: Dictionary mit patient_id -> (firstname, lastname) Mapping
    
    Gibt zurück:
        Der Pfad zur erstellten PDF-Datei
    """
    output_path = Path(output_dir)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    pdf_filename = output_path / f"patient_{patient_id}.pdf"
    
    pdf = canvas.Canvas(str(pdf_filename), pagesize=A4)
    
    current_position_y = PAGE_HEIGHT - MARGIN_TOP
    
    current_position_y = draw_page_header(pdf, patient_id, current_position_y, patient_data_dict)
    
    content_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    
    all_questionnaire_names = set(questionnaire_scores.keys())
    
    ordered_questionnaire_names = get_questionnaires_in_order(all_questionnaire_names)
    
    # ===== ERSTELLE FÜR JEDEN FRAGEBOGEN EIN DIAGRAMM =====
    
    for questionnaire_name in ordered_questionnaire_names:
        score_data = questionnaire_scores[questionnaire_name]
        
        if not score_data:
            continue
        
        # ===== ERSTELLE DAS DIAGRAMM =====
        
        plot_figure = create_plot_image(patient_id, questionnaire_name, score_data)
        
        pdf_image, image_buffer = convert_plot_to_pdf_image(plot_figure)
        
        image_original_width, image_original_height = pdf_image.getSize()
        
        image_new_width, image_new_height = calculate_image_size(
            image_original_width,
            image_original_height
        )
        
        # ===== ÜBERPRÜFEN, OB EINE NEUE SEITE NÖTIG IST =====
        
        required_space = image_new_height + SPACE_BETWEEN_CHARTS
        
        if current_position_y - required_space < MARGIN_BOTTOM:
            pdf.showPage()
            current_position_y = PAGE_HEIGHT - MARGIN_TOP
            current_position_y = draw_page_header(pdf, patient_id, current_position_y, patient_data_dict)
        
        # ===== ZEICHNE DAS BILD INS PDF =====
        
        image_position_x = MARGIN_LEFT + (content_width - image_new_width) / 2
        
        image_position_y = current_position_y - image_new_height
        
        pdf.drawImage(
            pdf_image,
            image_position_x,
            image_position_y,
            width=image_new_width,
            height=image_new_height,
            preserveAspectRatio=True,
            mask="auto",
        )
        
        # ===== SPEICHERPLATZ FREIGEBEN UND POSITION AKTUALISIEREN =====
        
        plt.close(plot_figure)
        
        image_buffer.close()
        
        current_position_y = image_position_y - SPACE_BETWEEN_CHARTS
    
    # ===== SPEICHERE DAS PDF =====
    
    pdf.save()
    
    return pdf_filename
