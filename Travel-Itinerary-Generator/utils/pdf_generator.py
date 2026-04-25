from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Font Setup
try:
    font_path = "C:\\Windows\\Fonts\\arial.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        DEFAULT_FONT = 'Arial'
    else:
        DEFAULT_FONT = 'Helvetica'
except:
    DEFAULT_FONT = 'Helvetica'


def add_cover(content, data, styles):
    """Adds a professional cover page."""
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Title'],
        fontName=DEFAULT_FONT, fontSize=36, leading=42,
        textColor=colors.HexColor('#B35422'), alignment=1, spaceAfter=20
    )
    subtitle_style = ParagraphStyle(
        'CoverSub', parent=styles['Heading2'],
        fontName=DEFAULT_FONT, fontSize=18, textColor=colors.HexColor('#4A3F35'),
        alignment=1, spaceAfter=50
    )
    
    content.append(Spacer(1, 2*inch))
    content.append(Paragraph(f"{data['destination'].upper()} TOUR PACKAGE", title_style))
    content.append(Paragraph(f"Exclusively curated for {data['duration']}", subtitle_style))
    content.append(Spacer(1, 1*inch))
    
    # Info summary table on cover
    info_data = [
        [Paragraph(f"<b>Destinations:</b> {data['destination']}", styles['Normal']), 
         Paragraph(f"<b>Duration:</b> {data['duration']}", styles['Normal'])]
    ]
    t = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
    t.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#B35422')),
        ('PADDING', (0,0), (-1,-1), 12)
    ]))
    content.append(t)
    content.append(PageBreak())


def add_itinerary(content, option, styles):
    """Adds the day-wise itinerary for an option."""
    header_style = ParagraphStyle(
        'ItinHeader', parent=styles['Heading1'],
        fontName=DEFAULT_FONT, fontSize=18, textColor=colors.HexColor('#B35422'),
        spaceBefore=20, spaceAfter=15
    )
    day_style = ParagraphStyle(
        'DayHeader', parent=styles['Heading2'],
        fontName=DEFAULT_FONT, fontSize=12, textColor=colors.white,
        backColor=colors.HexColor('#B35422'), borderPadding=5, spaceBefore=10
    )
    
    content.append(Paragraph(f"Daywise Itinerary - {option['option_id']}", header_style))

    for day in option["itinerary"]:
        content.append(Paragraph(
            f"DAY {day['day']}: {day.get('title', 'Sightseeing')} ({day.get('date', 'TBD')})",
            day_style
        ))
        content.append(Spacer(1, 8))

        for act in day["activities"]:
            content.append(Paragraph(f"• {act}", styles['Normal']))
            content.append(Spacer(1, 4))

        content.append(Paragraph(f"<b>CITY:</b> {day['city']}", styles['Normal']))
        meals = ", ".join(day.get('meals', []))
        content.append(Paragraph(f"<b>MEALS INCLUDED:</b> {meals}", styles['Normal']))
        content.append(Spacer(1, 12))


def add_hotel_table(content, option, styles):
    """Adds accommodation details in a table."""
    hotel = option["hotel"]
    content.append(Paragraph("Accommodation Details", styles['Heading2']))
    content.append(Spacer(1, 8))

    table_data = [
        [Paragraph("<b>City</b>", styles['Normal']), 
         Paragraph("<b>Hotel Name</b>", styles['Normal']), 
         Paragraph("<b>Category</b>", styles['Normal']), 
         Paragraph("<b>Room Type</b>", styles['Normal']), 
         Paragraph("<b>Nights</b>", styles['Normal'])],
        [option['itinerary'][0]['city'], hotel["name"], hotel["category"], hotel["room_type"], hotel["nights"]]
    ]

    t = Table(table_data, colWidths=[1.2*inch, 2.5*inch, 1*inch, 1.3*inch, 0.8*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F8F5F0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0,0), (-1,-1), DEFAULT_FONT)
    ]))
    content.append(t)
    content.append(Spacer(1, 20))


def add_pricing(content, option, styles):
    """Adds pricing section and transport details."""
    pricing = option["pricing"]
    
    content.append(Paragraph("Transportation & Sightseeing", styles['Heading2']))
    content.append(Paragraph(option.get('transport_facility', 'Private vehicle for transfers and sightseeing.'), styles['Normal']))
    content.append(Spacer(1, 15))

    content.append(Paragraph("Pricing Details", styles['Heading2']))
    content.append(Spacer(1, 8))
    
    p_data = [
        [Paragraph("<b>Package Type</b>", styles['Normal']), Paragraph("<b>Total Cost</b>", styles['Normal']), Paragraph("<b>Per Person</b>", styles['Normal'])],
        [option['option_id'], f"INR {pricing['total_cost']}", f"INR {pricing['per_person']}"]
    ]
    t = Table(p_data, colWidths=[2.5*inch, 2*inch, 2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8F4F8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    content.append(t)
    content.append(Spacer(1, 24))


def add_list_section(content, title, items, styles):
    """Adds a bulleted list section (inclusions/exclusions)."""
    content.append(Paragraph(title.upper(), styles['Heading2']))
    content.append(Spacer(1, 5))
    for item in items:
        content.append(Paragraph(f"• {item}", styles['Normal']))
        content.append(Spacer(1, 3))
    content.append(Spacer(1, 15))


def generate_pdf(data, filename="itinerary.pdf"):
    """Main builder for the Professional Agency PDF."""
    doc = SimpleDocTemplate(
        filename, pagesize=letter,
        leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch
    )
    styles = getSampleStyleSheet()
    
    # Global Style Adjustments
    for s in styles.byName.values():
        if hasattr(s, 'fontName'): s.fontName = DEFAULT_FONT

    content = []

    # 1. Cover Page
    add_cover(content, data, styles)

    # 2. Options (Itinerary + Hotel + Pricing)
    for option in data["options"]:
        add_itinerary(content, option, styles)
        add_hotel_table(content, option, styles)
        add_pricing(content, option, styles)
        content.append(PageBreak())

    # 3. Final Details
    add_list_section(content, "Inclusions", data.get("inclusions", []), styles)
    add_list_section(content, "Exclusions", data.get("exclusions", []), styles)
    add_list_section(content, "Terms & Conditions", data.get("terms", []), styles)

    doc.build(content)
    return filename
