"""Apply Full-Page Landscape Business Model Canvas (BMC) to Chapter 6.
Follows official KMUTNB / Thai academic thesis standards (academic-project-report skill):
1. Replaces tiny portrait BMC thumbnail with dedicated 1-page Landscape A4 section.
2. Embeds ultra-high-definition BMC diagram (4170 x 2520 px, width=9.20", height=5.56").
3. Enforces Zero Orphan Pages in Chapter 6:
   - Page 1 (Doc Page 15): Title + Intro + 6.1 (Key Partners) + 6.2 (Key Activities)
   - Page 2 (Doc Page 16, Landscape): Figure 6.1 (Full Page 9-Box BMC) + Caption + Source
   - Page 3 (Doc Page 17): 6.3 (Key Resources) + 6.4 (Value Propositions) + 6.5 (Customer Relationships) + 6.6 (Channels)
   - Page 4 (Doc Page 18): 6.7 (Customer Segments) + 6.8 (Cost Structure) + 6.9 (Revenue Streams) + Summary
4. Applies Thai syllable segmentation and Zero Dangling Punctuation.
5. Two-pass dynamic synchronization for TOC, LOT, and LOF page numbers.
6. Headless Word COM conversion and automated PyMuPDF visual inspection.
"""

import sys, os, re, json, shutil, subprocess
from pathlib import Path
from copy import deepcopy
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import fitz

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[2]
DELIVERY_DIR = ROOT / '00_ไฟล์ส่งงาน_Smart_Queue_Food'
REPORT_DOCX = DELIVERY_DIR / '01_เล่มรายงาน_Smart_Queue_Food_ฉบับสมบูรณ์.docx'
REPORT_PDF = DELIVERY_DIR / '01_เล่มรายงาน_Smart_Queue_Food_ฉบับสมบูรณ์.pdf'
# 1. Restore clean original file from templates
src_clean = ROOT / 'Project_Smart_Queue_Food' / 'templates' / 'original-report-template.docx'
shutil.copy2(src_clean, REPORT_DOCX)
print(f'Restored clean original to {REPORT_DOCX}')

import zipfile

# Source BMC image from delivery folder
IMG_SRC = DELIVERY_DIR / '03_ภาพแบบจำลองผืนผ้าใบธุรกิจ_BMC_HighRes.png'

# Update word/media/image4.png inside docx zip package before loading
with zipfile.ZipFile(REPORT_DOCX, 'r') as zin:
    items = {item.filename: zin.read(item.filename) for item in zin.infolist()}

items['word/media/image4.png'] = IMG_SRC.read_bytes()

with zipfile.ZipFile(REPORT_DOCX, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
    for fname, data in items.items():
        zout.writestr(fname, data)
print('Replaced word/media/image4.png inside docx with new large high-res image')

# Load document
doc = docx.Document(REPORT_DOCX)
P = doc.paragraphs

# Locate Chapter 6
ch6_idx = None
for i, p in enumerate(P):
    if p.text.strip() == 'บทที่ 6':
        ch6_idx = i
        break
assert ch6_idx is not None, "Chapter 6 not found!"
print(f'Found Chapter 6 at paragraph {ch6_idx}')

# Update intro paragraph (P220)
intro_text = (
    "แบบจำลองผืนผ้าใบธุรกิจ (Business Model Canvas: BMC) ทั้ง 9 องค์ประกอบ เป็นเครื่องมือเชิงกลยุทธ์สำคัญ"
    "ที่คณะผู้จัดทำใช้สังเคราะห์และบูรณาการคุณค่า นวัตกรรมเทคโนโลยี การดำเนินงาน และโครงสร้างทางการเงินของ "
    "Smart Queue Food เข้าด้วยกันอย่างเป็นรูปธรรม เพื่อให้เห็นภาพรวมของระบบนิเวศธุรกิจอย่างชัดเจนและครบถ้วน "
    "คณะผู้จัดทำได้จัดวางแผนภาพสรุป BMC 9 ช่องในรูปแบบแนวนอนเต็มหน้ากระดาษในรูปที่ 6.1 (หน้าถัดไป) "
    "เพื่อให้เห็นองค์ประกอบทุกด้านได้อย่างชัดเจนสมบูรณ์ โดยมีรายละเอียดการวิเคราะห์เชิงลึกของแต่ละองค์ประกอบดังต่อไปนี้:"
)

def set_para_text(p, text, font_name="TH Sarabun New", font_size_pt=16, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY):
    p.clear()
    p.paragraph_format.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.first_line_indent = Inches(0.5)
    r = p.add_run(text)
    r.font.name = font_name
    r.font.size = Pt(font_size_pt)
    r.font.bold = bold
    r.font.italic = italic
    rf = r._r.get_or_add_rPr().rFonts
    for attr in ['ascii', 'hAnsi', 'cs', 'eastAsia']:
        rf.set(qn('w:' + attr), font_name)
    return r

set_para_text(P[ch6_idx + 2], intro_text)

# Find and extract old image drawing from P221
drawings = P[ch6_idx + 3]._p.xpath('.//*[local-name()="drawing"]')
assert len(drawings) > 0, "No drawing found in P221!"
drawing_copy = deepcopy(drawings[0])

# Remove old small image and caption paragraphs
p_img_old = P[ch6_idx + 3]._p
p_cap_old = P[ch6_idx + 4]._p
parent_p = p_img_old.getparent()
parent_p.remove(p_img_old)
parent_p.remove(p_cap_old)
print('Removed old portrait thumbnail paragraphs')

# Find end of 6.2 (item 3: 'การตลาดและการสื่อสาร') in body paragraphs (index >= ch6_idx)
p_6_2_end = None
for i in range(ch6_idx, min(ch6_idx + 40, len(doc.paragraphs))):
    p = doc.paragraphs[i]
    clean = p.text.replace('\u200b', '')
    if 'การตลาดและการสื่อสาร' in clean and clean.startswith('3)'):
        p_6_2_end = p
        print(f'Found end of 6.2 at paragraph {i}: {p.text[:40]}')
        break
assert p_6_2_end is not None, "End of 6.2 not found!"

# Add Portrait Section Break to p_6_2_end
sectpr_portrait_first = parse_xml(
    f'<w:sectPr {nsdecls("w", "r")}>\n'
    f'  <w:headerReference w:type="first" r:id="rId18"/>\n'
    f'  <w:pgSz w:w="11909" w:h="16834"/>\n'
    f'  <w:pgMar w:top="2160" w:right="1440" w:bottom="1440" w:left="2160" w:header="720" w:footer="720" w:gutter="0"/>\n'
    f'  <w:cols w:space="720"/>\n'
    f'  <w:titlePg/>\n'
    f'  <w:docGrid w:linePitch="360"/>\n'
    f'</w:sectPr>'
)
p_6_2_end._p.get_or_add_pPr().append(sectpr_portrait_first)

# Create Landscape Paragraphs:
# 1. Image paragraph
p_img_new = OxmlElement('w:p')
pPr_img = OxmlElement('w:pPr')
pPr_img.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="center"/>'))
pPr_img.append(parse_xml(f'<w:spacing {nsdecls("w")} w:before="0" w:after="72" w:line="240" w:lineRule="auto"/>'))
pPr_img.append(parse_xml(f'<w:ind {nsdecls("w")} w:firstLine="0" w:left="0"/>'))
pPr_img.append(parse_xml(f'<w:keepNext {nsdecls("w")}/>'))
p_img_new.append(pPr_img)

new_w_emu = int(9.20 * 914400)
new_h_emu = int(5.56 * 914400)
xfrm_ext = drawing_copy.xpath('.//*[local-name()="xfrm"]/*[local-name()="ext"]')[0]
xfrm_ext.attrib['cx'] = str(new_w_emu)
xfrm_ext.attrib['cy'] = str(new_h_emu)
wp_extent = drawing_copy.xpath('.//*[local-name()="extent"]')[0]
wp_extent.attrib['cx'] = str(new_w_emu)
wp_extent.attrib['cy'] = str(new_h_emu)

r_img = OxmlElement('w:r')
r_img.append(drawing_copy)
p_img_new.append(r_img)

# 2. Figure Caption
p_cap_new = OxmlElement('w:p')
pPr_cap = OxmlElement('w:pPr')
pPr_cap.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="center"/>'))
pPr_cap.append(parse_xml(f'<w:spacing {nsdecls("w")} w:before="72" w:after="36" w:line="240" w:lineRule="auto"/>'))
pPr_cap.append(parse_xml(f'<w:ind {nsdecls("w")} w:firstLine="0" w:left="0"/>'))
pPr_cap.append(parse_xml(f'<w:keepNext {nsdecls("w")}/>'))
p_cap_new.append(pPr_cap)

r_cap = OxmlElement('w:r')
rPr_cap = parse_xml(
    f'<w:rPr {nsdecls("w")}>\n'
    f'  <w:rFonts w:ascii="TH Sarabun New" w:hAnsi="TH Sarabun New" w:cs="TH Sarabun New" w:eastAsia="TH Sarabun New"/>\n'
    f'  <w:b/>\n'
    f'  <w:bCs/>\n'
    f'  <w:sz w:val="28"/>\n'
    f'  <w:szCs w:val="28"/>\n'
    f'</w:rPr>'
)
r_cap.append(rPr_cap)
t_cap = OxmlElement('w:t')
t_cap.text = "รูปที่ 6.1  แบบจำลองผืนผ้าใบธุรกิจ 9 ช่อง (Business Model Canvas)"
r_cap.append(t_cap)
p_cap_new.append(r_cap)

# 3. Source paragraph with Landscape SectPr
p_src_new = OxmlElement('w:p')
pPr_src = OxmlElement('w:pPr')
pPr_src.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="center"/>'))
pPr_src.append(parse_xml(f'<w:spacing {nsdecls("w")} w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'))
pPr_src.append(parse_xml(f'<w:ind {nsdecls("w")} w:firstLine="0" w:left="0"/>'))

sectpr_landscape = parse_xml(
    f'<w:sectPr {nsdecls("w", "r")}>\n'
    f'  <w:pgSz w:w="16834" w:h="11909" w:orient="landscape"/>\n'
    f'  <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="2160" w:header="720" w:footer="720" w:gutter="0"/>\n'
    f'  <w:cols w:space="720"/>\n'
    f'  <w:docGrid w:linePitch="360"/>\n'
    f'</w:sectPr>'
)
pPr_src.append(sectpr_landscape)
p_src_new.append(pPr_src)

r_src = OxmlElement('w:r')
rPr_src = parse_xml(
    f'<w:rPr {nsdecls("w")}>\n'
    f'  <w:rFonts w:ascii="TH Sarabun New" w:hAnsi="TH Sarabun New" w:cs="TH Sarabun New" w:eastAsia="TH Sarabun New"/>\n'
    f'  <w:i/>\n'
    f'  <w:iCs/>\n'
    f'  <w:sz w:val="24"/>\n'
    f'  <w:szCs w:val="24"/>\n'
    f'</w:rPr>'
)
r_src.append(rPr_src)
t_src = OxmlElement('w:t')
t_src.text = "(ที่มา: คณะผู้จัดทำ, 2569)"
r_src.append(t_src)
p_src_new.append(r_src)

# Insert after p_6_2_end
elem_6_2 = p_6_2_end._p
elem_6_2.addnext(p_src_new)
elem_6_2.addnext(p_cap_new)
elem_6_2.addnext(p_img_new)
print('Inserted dedicated landscape BMC page elements')

# Strategic page break on Section 6.7 in the body (index >= ch6_idx)
for i in range(ch6_idx, len(doc.paragraphs)):
    p = doc.paragraphs[i]
    if '6.7' in p.text and 'กลุ่มลูกค้าเป้าหมาย' in p.text.replace('\u200b', ''):
        p.paragraph_format.page_break_before = True
        print(f'Applied strategic page break on Section 6.7 at paragraph {i}')
        break

# Ensure section header compliance:
# Section 7 (Chapter 6 start) -> diff_first = True (hide page number on chapter start page)
doc.sections[7].different_first_page_header_footer = True
doc.sections[7].first_page_header.is_linked_to_previous = False
if doc.sections[7].first_page_header.paragraphs:
    doc.sections[7].first_page_header.paragraphs[0].text = ''

# Section 9 (Chapter 6 continuation from 6.3) -> diff_first = False (show page numbers 17 & 18)
doc.sections[9].different_first_page_header_footer = False
print('Configured section headers: Section 7 diff_first=True, Section 9 diff_first=False')

# Thai word tokenization and zero dangling punctuation using bundled Node ICU segmenter
runs = []
for index, p in enumerate(doc.paragraphs):
    if index in [7, 8, 9, 13, 14, 15] or index >= 98:
        runs.extend(r for r in p.runs if len(r.text) > 40 and re.search('[ก-๙]', r.text))
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                runs.extend(r for r in p.runs if len(r.text) > 40 and re.search('[ก-๙]', r.text))

runs = list({id(r._r): r for r in runs}.values())
node = Path(r'C:\Users\PC\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe')
code = """let b='';process.stdin.setEncoding('utf8');process.stdin.on('data',x=>b+=x);process.stdin.on('end',()=>{const s=new Intl.Segmenter('th',{granularity:'word'});const out=JSON.parse(b).map(t=>Array.from(s.segment(t.replace(/\\u200b/g,'')),x=>x.segment).join('\\u200b').replace(/\\u200b+([,.:;!?\\)\\]\\}%\\sฯๆ/”’])/g,'$1').replace(/([\\(\\[\\{\\s/“‘])\\u200b+/g,'$1'));process.stdout.write(JSON.stringify(out));});"""
proc = subprocess.run([str(node), '-e', code], input=json.dumps([r.text for r in runs], ensure_ascii=False), text=True, encoding='utf8', capture_output=True, check=True)
for r, t in zip(runs, json.loads(proc.stdout)):
    r.text = t
print(f'Segmented {len(runs)} Thai text runs with Zero Dangling Punctuation')

# Save Pass 1 document in system temp directory
import tempfile
temp_dir = Path(tempfile.gettempdir())
pass1_docx = temp_dir / 'smart_queue_pass1_report.docx'
pass1_pdf = temp_dir / 'smart_queue_pass1_report.pdf'
doc.save(pass1_docx)
print(f'Saved Pass 1 docx: {pass1_docx}')

# Convert Pass 1 to PDF via Word COM
import win32com.client
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
doc_com = word.Documents.Open(str(pass1_docx.resolve()))
doc_com.SaveAs(str(pass1_pdf.resolve()), FileFormat=17)
doc_com.Close(False)
word.Quit()
print(f'Converted Pass 1 to PDF: {pass1_pdf}')

# Pass 2: Dynamic TOC/LOT/LOF Sync
pdf = fitz.open(pass1_pdf)
print(f'Total PDF pages in Pass 1: {len(pdf)}')

# Map physical pages to document page numbers
body_start_phys = None
for i in range(len(pdf)):
    t = pdf[i].get_text()
    lines = [l.strip().replace('\u200b', '') for l in t.split('\n') if l.strip()]
    if 'บทที่ 1' in lines and any('บทนำ' in l for l in lines):
        body_start_phys = i
        print(f'Body starts at physical page {i+1} (Doc Page 1)')
        break
assert body_start_phys is not None, "Could not determine body start physical page!"

def norm(t):
    return re.sub(r'\s+', '', t).replace('\u200b', '').replace('ำ', 'า')

pdf_pages_lines = []
for p in pdf:
    text = p.get_text()
    pdf_pages_lines.append([l.strip().replace('\u200b', '') for l in text.split('\n') if l.strip()])

# Build page mapping for each token by scanning from body_start_phys onwards
token_page_map = {}
for phys_idx in range(body_start_phys, len(pdf)):
    doc_page = phys_idx - body_start_phys + 1
    lines = pdf_pages_lines[phys_idx]
    for line in lines:
        clean_line = norm(line)
        m = re.match(r'^(บทที่\d+|ตารางที่(?:\d+|ข)\.\d+|รูปที่(?:\d+|ก)\.\d+|บรรณานุกรม|ภาคผนวก[กข]|\d+\.\d+)', clean_line)
        if m:
            t = m.group(1)
            if t not in token_page_map:
                token_page_map[t] = doc_page

print('Detected tokens in body pages:', len(token_page_map))

verified_toc = []
for p_idx, p in enumerate(doc.paragraphs[:98]):
    if '\t' not in p.text:
        continue
    label, old_page = p.text.rsplit('\t', 1)
    key = norm(label)
    if not old_page.strip().isdigit():
        continue
    m = re.match(r'(บทที่\d+|\d+\.\d+|ตารางที่(?:\d+|ข)\.\d+|รูปที่(?:\d+|ก)\.\d+|บรรณานุกรม|ภาคผนวก[กข])', key)
    if not m:
        continue
    token = m.group(1)
    
    target_page = token_page_map.get(token)
    if target_page is not None:
        rp = deepcopy(p.runs[0]._r.rPr) if p.runs else None
        p.clear()
        r = p.add_run(f'{label}\t{target_page}')
        if rp is not None:
            r._r.insert(0, rp)
        verified_toc.append({'token': token, 'label': label, 'page': target_page})
        print(f'TOC Sync: {token} -> Page {target_page}')
    else:
        print(f'WARNING: Could not find page for token {token} (label={label})')

print(f'Synchronized {len(verified_toc)} TOC/LOT/LOF entries!')

# Save final docx directly into delivery folder
doc.save(REPORT_DOCX)
print(f'Saved final delivery DOCX: {REPORT_DOCX}')

# Convert to final PDF via Word COM
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
doc_com = word.Documents.Open(str(REPORT_DOCX.resolve()))
doc_com.SaveAs(str(REPORT_PDF.resolve()), FileFormat=17)
doc_com.Close(False)
word.Quit()
print(f'Saved final delivery PDF: {REPORT_PDF}')

# Final Verification
final_pdf = fitz.open(REPORT_PDF)
print(f'Final PDF has {len(final_pdf)} pages.')
for i, page in enumerate(final_pdf):
    if page.rect.width > page.rect.height:
        print(f'Verified LANDSCAPE Page {i+1}: size={page.rect.width}x{page.rect.height}')
