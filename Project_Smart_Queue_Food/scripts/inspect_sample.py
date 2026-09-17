import os
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

sample_path = r'C:\Project\innovative-technopreneurs\Lectures\Project\ตัวอย่าง\03_เล่มโปรเจค_Word_บทที่_1-5\บทที่-1.docx'
doc = docx.Document(sample_path)

print("=== SECTIONS & MARGINS ===")
for i, s in enumerate(doc.sections):
    print(f"Section {i}: top={s.top_margin.inches} bottom={s.bottom_margin.inches} left={s.left_margin.inches} right={s.right_margin.inches}")

print("\n=== STYLES / PARAGRAPHS IN SAMPLE ===")
for idx, p in enumerate(doc.paragraphs):
    if not p.text.strip():
        continue
    runs = p.runs
    r_font = runs[0].font.name if runs else None
    r_size = runs[0].font.size.pt if (runs and runs[0].font.size) else None
    r_bold = runs[0].bold if runs else None
    
    # Check alignment and jc xml
    jc_val = "None"
    pPr = p._p.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
    if pPr is not None:
        jc = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}jc')
        if jc is not None:
            jc_val = jc.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
            
    first_ind = p.paragraph_format.first_line_indent.inches if p.paragraph_format.first_line_indent else 0
    left_ind = p.paragraph_format.left_indent.inches if p.paragraph_format.left_indent else 0
    
    print(f"P{idx:02d} | text: {p.text[:35]!r} | font: {r_font} {r_size}pt bold={r_bold} | jc: {jc_val} align: {p.alignment} | left: {left_ind:.2f}\" first: {first_ind:.2f}\"")
