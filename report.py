from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import base64, io
from datetime import datetime


def generate_pdf(data: dict, output_path: str = "report.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('Title', fontSize=18, fontName='Helvetica-Bold',
                                 textColor=colors.HexColor('#C0392B'), spaceAfter=4)
    sub_style = ParagraphStyle('Sub', fontSize=9,
                               textColor=colors.HexColor('#7f8c8d'), spaceAfter=16)
    h2 = ParagraphStyle('H2', fontSize=11, fontName='Helvetica-Bold',
                        textColor=colors.HexColor('#2C3E50'), spaceAfter=6, spaceBefore=10)

    story.append(Paragraph("PHISHRADAR - THREAT INTELLIGENCE REPORT", title_style))
    story.append(Paragraph("CONFIDENTIAL - FOR LAW ENFORCEMENT USE ONLY", sub_style))

    ai = data.get("ai_analysis", {})
    infra = data.get("infrastructure", {})
    vt = data.get("virustotal", {})

    rows = [
        ["FIELD", "VALUE"],
        ["Report Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")],
        ["Target URL", data.get("url", "N/A")],
        ["Threat Level", ai.get("threat_level", "Unknown")],
        ["Threat Type", ai.get("threat_type", "Unknown")],
        ["AI Confidence", f"{ai.get('confidence', 0)}%"],
        ["IP Address", infra.get("ip_address", "N/A")],
        ["Hosting Provider", infra.get("org", "N/A")],
        ["Country", infra.get("country", "N/A")],
        ["ISP", infra.get("isp", "N/A")],
        ["Domain Registrar", infra.get("registrar", "N/A")],
        ["Domain Created", infra.get("domain_created", "N/A")],
        ["VT Malicious Engines", str(vt.get("malicious", 0))],
        ["VT Suspicious Engines", str(vt.get("suspicious", 0))],
        ["C2 Assessment", ai.get("c2_likelihood", "N/A")],
    ]

    t = Table(rows, colWidths=[2.3*inch, 4.2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F4F6F7'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#BDC3C7')),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("THREAT SUMMARY", h2))
    story.append(Paragraph(ai.get("summary", "N/A"), styles['Normal']))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("INDICATORS OF COMPROMISE", h2))
    for ioc in ai.get("indicators", []):
        story.append(Paragraph("- " + ioc, styles['Normal']))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("RECOMMENDED ACTION", h2))
    story.append(Paragraph(ai.get("recommended_action", "N/A"), styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("PHISHING PAGE SCREENSHOT", h2))
    if data.get("screenshot"):
        try:
            img_bytes = base64.b64decode(data["screenshot"])
            img = Image(io.BytesIO(img_bytes), width=5.5*inch, height=3.2*inch)
            story.append(img)
        except Exception:
            story.append(Paragraph("Screenshot could not be rendered.", styles['Normal']))
    else:
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(
            "Screenshot unavailable - site blocked automated browser or went offline before capture.",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(
            "This is common with phishing sites that detect and block security scanners. "
            "The URL and infrastructure data above remain valid for investigation.",
            styles['Normal']
        ))

    doc.build(story)
    return output_path