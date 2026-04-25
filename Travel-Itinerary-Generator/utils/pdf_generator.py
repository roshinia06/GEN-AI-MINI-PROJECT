from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import os

def generate_pdf(data, filename="itinerary.pdf"):
    """
    Generates a professionally formatted PDF itinerary.
    Matches the morning/afternoon/evening schema used by the frontend and agents.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = styles['Title']
    title_style.fontSize = 28
    title_style.textColor = colors.HexColor('#B35422') # Rust
    title_style.alignment = 1 # Center

    subtitle_style = styles['Heading2']
    subtitle_style.fontSize = 16
    subtitle_style.textColor = colors.HexColor('#2D241D') # Bark
    subtitle_style.alignment = 1

    day_header_style = styles['Heading2']
    day_header_style.fontSize = 14
    day_header_style.textColor = colors.white
    day_header_style.backColor = colors.HexColor('#B35422') # Rust
    day_header_style.spaceBefore = 15
    day_header_style.leftIndent = 0

    slot_header_style = styles['Heading3']
    slot_header_style.fontSize = 10
    slot_header_style.textColor = colors.HexColor('#7B5233') # Clay

    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.leading = 12

    content = []

    # Title & Subtitle
    content.append(Paragraph(f"YOUR PREMIUM ESCAPE TO {data['destination'].upper()}", title_style))
    content.append(Paragraph(f"A {data['duration']} Personalized Journey", subtitle_style))
    content.append(Spacer(1, 20))

    # Summary Table
    currency = data.get('currency_symbol', '₹')
    summary_data = [
        [Paragraph(f"<b>Origin:</b> {data.get('starting_place', 'Your location')}", normal_style), Paragraph(f"<b>Destination:</b> {data['destination']}", normal_style)],
        [Paragraph(f"<b>Duration:</b> {data['duration']}", normal_style), Paragraph(f"<b>Estimated Budget:</b> {currency}{data['total_cost']}", normal_style)],
    ]
    summary_table = Table(summary_data, colWidths=[3.5*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F5F0')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDBDBD')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    content.append(summary_table)
    content.append(Spacer(1, 20))

    # Days
    for day in data.get("itinerary", []):
        # Day header
        day_num = day.get('day', '?')
        day_text = f"DAY {day_num}"
        content.append(Paragraph(day_text, day_header_style))
        content.append(Spacer(1, 5))

        # Time Slots
        for slot in ["morning", "afternoon", "evening"]:
            slot_data = day.get(slot)
            if not slot_data: continue
            
            title = slot.capitalize()
            if isinstance(slot_data, str):
                activity = slot_data
                desc = ""
                cost = ""
            else:
                activity = slot_data.get("activity", "Exploring")
                desc = slot_data.get("description", "")
                cost_val = slot_data.get("cost")
                cost = f" ({currency}{cost_val})" if cost_val is not None else ""

            content.append(Paragraph(f"<b>{title}:</b> {activity}{cost}", normal_style))
            if desc:
                content.append(Paragraph(f"<font color='#7B5233'>{desc}</font>", normal_style))
            content.append(Spacer(1, 5))

        # Dining & Accommodation
        dining = day.get("dining")
        accommodation = day.get("accommodation")
        
        if dining or accommodation:
            info_data = []
            if dining:
                dining_text = dining if isinstance(dining, str) else dining.get("recommendation", str(dining))
                info_data.append([Paragraph("<b>DINING</b>", normal_style), Paragraph(dining_text, normal_style)])
            if accommodation:
                acc_text = accommodation if isinstance(accommodation, str) else accommodation.get("name", str(accommodation))
                info_data.append([Paragraph("<b>STAY</b>", normal_style), Paragraph(acc_text, normal_style)])
            
            info_table = Table(info_data, colWidths=[1.5*inch, 5.5*inch])
            info_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#EEEEEE')),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            content.append(Spacer(1, 5))
            content.append(info_table)
        
        content.append(Spacer(1, 10))

    # Tips
    if data.get("tips"):
        content.append(Spacer(1, 10))
        content.append(Paragraph("<b>TRAVELER TIPS</b>", slot_header_style))
        for tip in data["tips"]:
            content.append(Paragraph(f"• {tip}", normal_style))

    # Footer
    content.append(Spacer(1, 30))
    footer_text = "Generated by Wanderer AI Travel Planner. Have a safe journey!"
    footer_style = styles['Normal']
    footer_style.fontSize = 8
    footer_style.textColor = colors.gray
    footer_style.alignment = 1
    content.append(Paragraph(footer_text, footer_style))

    doc.build(content)
    return filename
