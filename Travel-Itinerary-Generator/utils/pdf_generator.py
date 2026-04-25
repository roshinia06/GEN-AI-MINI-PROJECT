from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import os


def generate_pdf(data, filename="itinerary.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = styles['Title']
    title_style.fontSize = 28
    title_style.textColor = colors.HexColor('#1A237E') # Deep Blue
    title_style.alignment = 1 # Center

    subtitle_style = styles['Heading2']
    subtitle_style.fontSize = 18
    subtitle_style.textColor = colors.HexColor('#3F51B5') # Indigo
    subtitle_style.alignment = 1

    day_header_style = styles['Heading2']
    day_header_style.fontSize = 16
    day_header_style.textColor = colors.white
    day_header_style.backColor = colors.HexColor('#009688') # Teal
    day_header_style.spaceBefore = 20
    day_header_style.leftIndent = 0

    section_header_style = styles['Heading3']
    section_header_style.fontSize = 12
    section_header_style.textColor = colors.HexColor('#E91E63') # Pink

    normal_style = styles['Normal']
    normal_style.fontSize = 11
    normal_style.leading = 14

    content = []

    # Title & Subtitle
    content.append(Paragraph(f"YOUR PREMIUM ESCAPE TO {data['destination'].upper()}", title_style))
    content.append(Paragraph(f"Curated {data['duration']} Itinerary", subtitle_style))
    content.append(Spacer(1, 30))

    # Summary Table
    currency = data.get('currency_symbol', '₹')
    summary_data = [
        [Paragraph(f"<b>Starting Point:</b> {data.get('starting_place', 'Your location')}", normal_style), Paragraph(f"<b>Destination:</b> {data['destination']}", normal_style)],
        [Paragraph(f"<b>Duration:</b> {data['duration']}", normal_style), Paragraph(f"<b>Estimated Budget:</b> {currency}{data['total_cost']}", normal_style)],
        [Paragraph(f"<b>Travel Style:</b> Personalized", normal_style), Paragraph("", normal_style)]
    ]
    summary_table = Table(summary_data, colWidths=[3.5*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F5F5F5')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    content.append(summary_table)
    content.append(Spacer(1, 20))

    # Days
    for day in data["itinerary"]:
        # Day header (Teal bar)
        day_text = f"DAY {day['day']}: {day['title'].upper()}"
        content.append(Paragraph(day_text, day_header_style))
        content.append(Spacer(1, 10))

        # Activities
        content.append(Paragraph("EXPERIENCES & EXPLORATION", section_header_style))
        for act in day["activities"]:
            content.append(Paragraph(f"• {act}", normal_style))
        content.append(Spacer(1, 10))

        # Stay and Meals Table
        stay_meals_data = [
            [Paragraph("<b>ACCOMMODATION</b>", normal_style), Paragraph(day['stay'], normal_style)],
            [Paragraph("<b>DINING PLAN</b>", normal_style), Paragraph(', '.join(day['meals']), normal_style)]
        ]
        
        sm_table = Table(stay_meals_data, colWidths=[2*inch, 5*inch])
        sm_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDBDBD')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#EEEEEE')),
        ]))
        content.append(sm_table)
        content.append(Spacer(1, 15))

    # Final Total cost
    content.append(Spacer(1, 20))
    cost_text = f"TOTAL ESTIMATED INVESTMENT: {currency}{data['total_cost']}"
    cost_style = styles['Heading2']
    cost_style.textColor = colors.HexColor('#43A047') # Green
    cost_style.alignment = 2 # Right
    content.append(Paragraph(cost_text, cost_style))

    # Footer
    content.append(Spacer(1, 40))
    footer_text = "Thank you for choosing our AI Travel Planner. Have a safe and wonderful journey!"
    footer_style = styles['Normal']
    footer_style.fontSize = 9
    footer_style.textColor = colors.gray
    footer_style.alignment = 1
    content.append(Paragraph(footer_text, footer_style))

    doc.build(content)
    return filename
