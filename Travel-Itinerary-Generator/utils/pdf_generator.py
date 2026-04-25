from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Try to register a font that supports Unicode (Rupee symbol etc.)
try:
    font_path = "C:\\Windows\\Fonts\\arial.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        DEFAULT_FONT = 'Arial'
    else:
        DEFAULT_FONT = 'Helvetica'
except:
    DEFAULT_FONT = 'Helvetica'


def generate_pdf(data, filename="itinerary.pdf"):
    """
    Generates a PROFESSIONAL TRAVEL AGENCY style PDF.
    Uses the activities-list schema.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = styles['Title']
    title_style.fontName = DEFAULT_FONT
    title_style.fontSize = 24
    title_style.textColor = colors.HexColor('#B35422') # Rust
    title_style.alignment = 1

    subtitle_style = styles['Heading2']
    subtitle_style.fontName = DEFAULT_FONT
    subtitle_style.fontSize = 14
    subtitle_style.textColor = colors.HexColor('#2D241D') # Bark
    subtitle_style.alignment = 1

    day_header_style = styles['Heading2']
    day_header_style.fontName = DEFAULT_FONT
    day_header_style.fontSize = 12
    day_header_style.textColor = colors.white
    day_header_style.backColor = colors.HexColor('#B35422') # Rust
    day_header_style.spaceBefore = 10

    normal_style = styles['Normal']
    normal_style.fontName = DEFAULT_FONT
    normal_style.fontSize = 10
    normal_style.leading = 14

    bullet_style = styles['Normal']
    bullet_style.fontName = DEFAULT_FONT
    bullet_style.fontSize = 10
    bullet_style.leading = 14
    bullet_style.leftIndent = 20

    content = []

    # Header
    content.append(Paragraph(f"PREMIUM TRAVEL ITINERARY: {data['destination'].upper()}", title_style))
    content.append(Paragraph(f"{data['duration']} Package | Prepared for Your Journey", subtitle_style))
    content.append(Spacer(1, 15))

    # Summary
    currency = data.get('currency_symbol', '₹')
    summary_data = [
        [Paragraph(f"<b>Starting From:</b> {data.get('starting_place', 'N/A')}", normal_style), Paragraph(f"<b>Destinations:</b> {data['destination']}", normal_style)],
        [Paragraph(f"<b>Mode:</b> {data.get('mode', 'Seasonal').capitalize()}", normal_style), Paragraph(f"<b>Total Budget:</b> {currency}{data['total_cost']}", normal_style)],
    ]
    summary_table = Table(summary_data, colWidths=[3.5*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F5F0')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDBDBD')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(summary_table)
    content.append(Spacer(1, 20))

    # Days
    for day in data.get("itinerary", []):
        day_num = day.get('day', '?')
        title = day.get('title', 'Sightseeing')
        date = day.get('date', '')
        
        header_text = f"DAY {day_num}: {title.upper()}"
        if date:
            header_text += f" ({date})"
            
        content.append(Paragraph(header_text, day_header_style))
        content.append(Spacer(1, 5))

        # Activities
        activities = day.get("activities", [])
        for act in activities:
            content.append(Paragraph(f"• {act}", bullet_style))
            content.append(Spacer(1, 3))

        # Meals
        meals = day.get("meals", [])
        if meals:
            meals_text = ", ".join(meals)
            content.append(Spacer(1, 5))
            content.append(Paragraph(f"<b>MEALS INCLUDED:</b> {meals_text}", normal_style))
        
        content.append(Spacer(1, 15))

    # Tips
    if data.get("tips"):
        content.append(Paragraph("<b>IMPORTANT TRAVEL NOTES & TIPS</b>", subtitle_style))
        content.append(Spacer(1, 5))
        for tip in data["tips"]:
            content.append(Paragraph(f"• {tip}", bullet_style))
            content.append(Spacer(1, 2))

    # Footer
    content.append(Spacer(1, 40))
    footer_text = "Thank you for choosing our professional travel planning services. Have a safe and memorable trip!"
    footer_style = styles['Normal']
    footer_style.fontSize = 8
    footer_style.textColor = colors.gray
    footer_style.alignment = 1
    content.append(Paragraph(footer_text, footer_style))

    doc.build(content)
    return filename
