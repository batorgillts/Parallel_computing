from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = "/Users/bat-orgiltsend-ochir/Desktop/School/Senior 2/Parallel Computing/lab2/report.pdf"
IMG    = "/Users/bat-orgiltsend-ochir/Desktop/School/Senior 2/Parallel Computing/lab2/speedup_graphs.png"

doc = SimpleDocTemplate(OUTPUT, pagesize=letter,
                        leftMargin=1*inch, rightMargin=1*inch,
                        topMargin=1*inch, bottomMargin=1*inch)

styles = getSampleStyleSheet()
title_style   = ParagraphStyle('Title2', parent=styles['Title'],   fontSize=16, spaceAfter=4)
sub_style     = ParagraphStyle('Sub',    parent=styles['Normal'],  fontSize=11, spaceAfter=2, alignment=TA_CENTER)
h1_style      = ParagraphStyle('H1',     parent=styles['Heading1'],fontSize=13, spaceBefore=14, spaceAfter=4)
h2_style      = ParagraphStyle('H2',     parent=styles['Heading2'],fontSize=11, spaceBefore=8,  spaceAfter=3)
body_style    = ParagraphStyle('Body',   parent=styles['Normal'],  fontSize=10, leading=14, spaceAfter=6)

story = []

# ── Title block ──────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Lab 2: OpenMP Prime Number Generation", title_style))
story.append(Paragraph("Speedup Analysis", title_style))
story.append(Paragraph("Student: bt2291", sub_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.grey, spaceAfter=12))

# ── Graph image (full, both graphs side by side) ─────────────────────────────
img = Image(IMG, width=6.4*inch, height=2.5*inch, kind='proportional')
story.append(img)
story.append(Spacer(1, 0.1*inch))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1
# ═══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph("Graph 1 — M=10, N=5,000", h1_style))

# Table 1
t1_data = [
    ["Threads", "Time (s)", "Speedup"],
    ["1",  "0.000243", "1.000"],
    ["2",  "0.000644", "0.377"],
    ["5",  "0.000533", "0.456"],
    ["10", "0.000585", "0.415"],
    ["15", "0.000656", "0.370"],
    ["20", "0.000789", "0.308"],
    ["25", "0.001138", "0.214"],
]
t1 = Table(t1_data, colWidths=[1.2*inch, 1.5*inch, 1.2*inch])
t1.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0),  colors.HexColor('#2c5f8a')),
    ('TEXTCOLOR',   (0,0), (-1,0),  colors.white),
    ('FONTNAME',    (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',    (0,0), (-1,-1), 10),
    ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#eaf1f8'), colors.white]),
    ('GRID',        (0,0), (-1,-1), 0.5, colors.grey),
    ('TOPPADDING',  (0,0), (-1,-1), 4),
    ('BOTTOMPADDING',(0,0),(-1,-1), 4),
]))
story.append(t1)
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("Pattern Observed", h2_style))
story.append(Paragraph(
    "The speedup drops immediately below 1.0 as soon as more than one thread is used, "
    "and continues to decline as thread count increases — reaching only 0.214x at 25 threads. "
    "No improvement over the single-threaded baseline is ever achieved.",
    body_style))

story.append(Paragraph("Explanation", h2_style))
story.append(Paragraph(
    "The problem size is far too small for parallelism to be beneficial. The range [10, 5000] "
    "contains only ~669 primes, and the total computation completes in under 0.3 milliseconds "
    "on a single thread. At this scale, the overhead of creating and synchronizing OpenMP threads "
    "completely dominates the actual computation time. This is a clear demonstration of Amdahl's Law: "
    "when the parallel workload is trivially small, no amount of additional threads can improve "
    "performance — the fixed overhead of parallelism itself becomes the bottleneck.",
    body_style))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2
# ═══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph("Graph 2 — M=10, N=5,000,000", h1_style))

t2_data = [
    ["Threads", "Time (s)", "Speedup"],
    ["1",  "2.031295", "1.000"],
    ["2",  "1.095261", "1.855"],
    ["5",  "0.515690", "3.939"],
    ["10", "0.380130", "5.343"],
    ["15", "0.330731", "6.141"],
    ["20", "0.311431", "6.523"],
    ["25", "0.301364", "6.740"],
]
t2 = Table(t2_data, colWidths=[1.2*inch, 1.5*inch, 1.2*inch])
t2.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0),  colors.HexColor('#2c5f8a')),
    ('TEXTCOLOR',   (0,0), (-1,0),  colors.white),
    ('FONTNAME',    (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',    (0,0), (-1,-1), 10),
    ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#eaf1f8'), colors.white]),
    ('GRID',        (0,0), (-1,-1), 0.5, colors.grey),
    ('TOPPADDING',  (0,0), (-1,-1), 4),
    ('BOTTOMPADDING',(0,0),(-1,-1), 4),
]))
story.append(t2)
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("Pattern Observed", h2_style))
story.append(Paragraph(
    "Speedup improves steadily from 1x to about 3.9x as threads increase from 1 to 5, "
    "then flattens dramatically — reaching only 6.74x at 25 threads, far below the ideal "
    "25x linear speedup.",
    body_style))

story.append(Paragraph("Explanation", h2_style))
story.append(Paragraph(
    "With a much larger range, there is enough computation for parallelism to provide real "
    "benefit — each thread handles a significant portion of the primality checks. However, "
    "speedup plateaus sharply after ~10 threads for two reasons: (1) The HPC node has a "
    "limited number of physical cores (approximately 8-12, based on where the curve flattens). "
    "Once the thread count exceeds the physical core count, threads must time-share cores, "
    "providing diminishing returns. (2) All threads share the same memory bus when reading and "
    "writing the is_prime array, so memory bandwidth becomes a bottleneck at high thread counts. "
    "The gap between the measured speedup (~6.7x) and the ideal speedup (25x) reflects both "
    "the hardware core limit and the inherently sequential portions of the code — array "
    "allocation, file I/O, and the correctness check all run on a single thread.",
    body_style))

doc.build(story)
print("Saved:", OUTPUT)
