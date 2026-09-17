import os
import re

target_file = r'C:\Project\innovative-technopreneurs\Project_Smart_Queue_Food\scripts\build_report.py'

with open(target_file, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update add_toc_line and add add_toc_col_header
old_add_toc = '''def add_toc_line(doc, title, page, is_bold=False, indent=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.05
    if indent > 0:
        p.paragraph_format.left_indent = Inches(indent)
    else:
        p.paragraph_format.left_indent = Inches(0)
    p.paragraph_format.first_line_indent = Inches(0)
    
    pPr = p._p.get_or_add_pPr()
    tab_xml = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:leader="dot" w:pos="8300"/></w:tabs>')
    pPr.append(tab_xml)
    
    r1 = p.add_run(thai_zwsp(title))
    set_run_font(r1, size_pt=14, bold=is_bold)
    
    r_tab = p.add_run(f"\\t{page}")
    set_run_font(r_tab, size_pt=14, bold=is_bold)
    return p'''

new_add_toc = '''def add_toc_line(doc, title, page, is_bold=False, indent=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    if indent > 0:
        p.paragraph_format.left_indent = Inches(indent)
    else:
        p.paragraph_format.left_indent = Inches(0)
    p.paragraph_format.first_line_indent = Inches(0)
    
    pPr = p._p.get_or_add_pPr()
    tab_xml = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:leader="dot" w:pos="8300"/></w:tabs>')
    pPr.append(tab_xml)
    
    r1 = p.add_run(thai_zwsp(title))
    set_run_font(r1, size_pt=13.5, bold=is_bold)
    
    r_tab = p.add_run(f"\\t{page}")
    set_run_font(r_tab, size_pt=13.5, bold=is_bold)
    return p

def add_toc_col_header(doc, left_label="เรื่อง", right_label="หน้า"):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0)
    p.paragraph_format.first_line_indent = Inches(0)
    pPr = p._p.get_or_add_pPr()
    tab_xml = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:pos="8300"/></w:tabs>')
    pPr.append(tab_xml)
    r1 = p.add_run(thai_zwsp(left_label))
    set_run_font(r1, size_pt=14, bold=True)
    r2 = p.add_run(f"\\t{right_label}")
    set_run_font(r2, size_pt=14, bold=True)
    return p'''

if old_add_toc in code:
    code = code.replace(old_add_toc, new_add_toc, 1)
    print("Replaced add_toc_line successfully.")
else:
    print("WARNING: old_add_toc not found exactly.")

# 2. Update DEFAULT_PAGE_MAP and build_doc signature
old_build_doc = '''def build_doc(toc_pages=None):
    if toc_pages is None:
        # Default mapping - will be replaced in pass 2 with exact scanned pages
        toc_pages = {
            'ch1': '1', 'ch1_2': '2', 'ch1_4': '2', 'ch1_5': '3',
            'ch2': '4', 'ch2_4': '5',
            'ch3': '6', 'ch3_3': '7',
            'ch4': '8', 'ch4_2': '9', 'ch4_3': '10',
            'ch5': '11', 'ch5_2': '11', 'ch5_3': '12',
            'ch6': '13', 'ch6_1': '13', 'ch6_6': '14',
            'ch7': '15', 'ch7_2': '15',
            'ch8': '17', 'ch8_2': '18',
            'ch9': '19', 'ch9_2': '20',
            'ch10': '21', 'ch10_3': '22',
            'ref': '24', 'app_a': '25', 'app_b': '26',
            'tbl_2_1': '5', 'tbl_3_1': '7', 'tbl_5_1': '11', 'tbl_9_1': '19', 'tbl_10_1': '21', 'tbl_b_1': '26',
            'fig_4_1': '9', 'fig_4_2': '10', 'fig_6_1': '13', 'fig_7_1': '15', 'fig_9_1': '20', 'fig_a_1': '25'
        }'''

new_build_doc = '''DEFAULT_PAGE_MAP = {
    'ch1': '1', 'ch1_2': '2', 'ch1_4': '3', 'ch1_5': '4',
    'ch2': '5', 'ch2_4': '6',
    'ch3': '7', 'ch3_3': '8',
    'ch4': '9', 'ch4_2': '10', 'ch4_3': '11',
    'ch5': '12', 'ch5_2': '12', 'ch5_3': '13',
    'ch6': '14', 'ch6_1': '14', 'ch6_6': '16',
    'ch7': '17', 'ch7_2': '18',
    'ch8': '19', 'ch8_2': '20',
    'ch9': '21', 'ch9_2': '22',
    'ch10': '23', 'ch10_3': '25',
    'ref': '27', 'app_a': '28', 'app_b': '29',
    'tbl_2_1': '6', 'tbl_3_1': '8', 'tbl_5_1': '12', 'tbl_9_1': '22', 'tbl_10_1': '24', 'tbl_b_1': '29',
    'fig_4_1': '10', 'fig_4_2': '11', 'fig_6_1': '14', 'fig_7_1': '17', 'fig_9_1': '22', 'fig_a_1': '28'
}

def build_doc(toc_pages=None):
    if toc_pages is None:
        toc_pages = DEFAULT_PAGE_MAP.copy()
    else:
        merged = DEFAULT_PAGE_MAP.copy()
        merged.update(toc_pages)
        toc_pages = merged'''

if old_build_doc in code:
    code = code.replace(old_build_doc, new_build_doc, 1)
    print("Replaced build_doc header successfully.")
else:
    print("WARNING: old_build_doc not found.")

# 3. Update TOC titles and add column headers
old_toc_p1 = '''    # --- TABLE OF CONTENTS - PART 1 (สารบัญ - หน้า ค: บทที่ 1 ถึง 5) ---
    p_toc_title = doc.add_paragraph()
    format_paragraph(p_toc_title, space_before=14, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_toc_title.paragraph_format.first_line_indent = Inches(0)
    r_toc = p_toc_title.add_run("สารบัญ")
    set_run_font(r_toc, size_pt=18, bold=True)'''

new_toc_p1 = '''    # --- TABLE OF CONTENTS - PART 1 (สารบัญ - หน้า ค: บทที่ 1 ถึง 5) ---
    p_toc_title = doc.add_paragraph()
    format_paragraph(p_toc_title, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_toc_title.paragraph_format.first_line_indent = Inches(0)
    r_toc = p_toc_title.add_run("สารบัญ")
    set_run_font(r_toc, size_pt=18, bold=True)
    add_toc_col_header(doc, "เรื่อง", "หน้า")'''

if old_toc_p1 in code:
    code = code.replace(old_toc_p1, new_toc_p1, 1)
    print("Replaced TOC P1 successfully.")
else:
    print("WARNING: old_toc_p1 not found.")

old_toc_p2 = '''    # --- TABLE OF CONTENTS - PART 2 (สารบัญ - หน้า ง: บทที่ 6 ถึง 10, บรรณานุกรม, ภาคผนวก) ---
    p_toc_title2 = doc.add_paragraph()
    format_paragraph(p_toc_title2, space_before=14, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_toc_title2.paragraph_format.first_line_indent = Inches(0)
    r_toc2 = p_toc_title2.add_run("สารบัญ (ต่อ)")
    set_run_font(r_toc2, size_pt=18, bold=True)'''

new_toc_p2 = '''    # --- TABLE OF CONTENTS - PART 2 (สารบัญ - หน้า ง: บทที่ 6 ถึง 10, บรรณานุกรม, ภาคผนวก) ---
    p_toc_title2 = doc.add_paragraph()
    format_paragraph(p_toc_title2, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_toc_title2.paragraph_format.first_line_indent = Inches(0)
    r_toc2 = p_toc_title2.add_run("สารบัญ (ต่อ)")
    set_run_font(r_toc2, size_pt=18, bold=True)
    add_toc_col_header(doc, "เรื่อง", "หน้า")'''

if old_toc_p2 in code:
    code = code.replace(old_toc_p2, new_toc_p2, 1)
    print("Replaced TOC P2 successfully.")
else:
    print("WARNING: old_toc_p2 not found.")

old_lot = '''    # --- LIST OF TABLES (สารบัญตาราง - หน้า จ) ---
    p_lot_title = doc.add_paragraph()
    format_paragraph(p_lot_title, space_before=14, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_lot_title.paragraph_format.first_line_indent = Inches(0)
    r_lot = p_lot_title.add_run("สารบัญตาราง")
    set_run_font(r_lot, size_pt=18, bold=True)'''

new_lot = '''    # --- LIST OF TABLES (สารบัญตาราง - หน้า จ) ---
    p_lot_title = doc.add_paragraph()
    format_paragraph(p_lot_title, space_before=0, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_lot_title.paragraph_format.first_line_indent = Inches(0)
    r_lot = p_lot_title.add_run("สารบัญตาราง")
    set_run_font(r_lot, size_pt=18, bold=True)
    add_toc_col_header(doc, "ตารางที่", "หน้า")'''

if old_lot in code:
    code = code.replace(old_lot, new_lot, 1)
    print("Replaced LOT successfully.")
else:
    print("WARNING: old_lot not found.")

old_lof = '''    # --- LIST OF FIGURES (สารบัญภาพ - หน้า ฉ) ---
    p_lof_title = doc.add_paragraph()
    format_paragraph(p_lof_title, space_before=14, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_lof_title.paragraph_format.first_line_indent = Inches(0)
    r_lof = p_lof_title.add_run("สารบัญภาพ")
    set_run_font(r_lof, size_pt=18, bold=True)'''

new_lof = '''    # --- LIST OF FIGURES (สารบัญภาพ - หน้า ฉ) ---
    p_lof_title = doc.add_paragraph()
    format_paragraph(p_lof_title, space_before=0, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_lof_title.paragraph_format.first_line_indent = Inches(0)
    r_lof = p_lof_title.add_run("สารบัญภาพ")
    set_run_font(r_lof, size_pt=18, bold=True)
    add_toc_col_header(doc, "รูปที่", "หน้า")'''

if old_lof in code:
    code = code.replace(old_lof, new_lof, 1)
    print("Replaced LOF successfully.")
else:
    print("WARNING: old_lof not found.")

# 4. Remove internal doc.add_page_break() in chapters:
# List of internal break line patterns:
breaks_to_remove = [
    # Ch 1
    '    # --- Page 2 ---\n    doc.add_page_break()',
    '    # --- Page 3 ---\n    doc.add_page_break()',
    # Ch 2
    '    # --- Page 2 ---\n    doc.add_page_break()',
    # Ch 3
    '    # --- Page 2 ---\n    doc.add_page_break()',
    # Ch 4
    '    # --- Page 2 ---\n    doc.add_page_break()',
    '    # --- Page 3 ---\n    doc.add_page_break()',
    # Ch 5
    '    # --- Page 2 ---\n    doc.add_page_break()',
    # Ch 6
    '    # --- Page 2 ---\n    doc.add_page_break()',
    '    # --- Page 3 ---\n    doc.add_page_break()',
    # Ch 7
    '    # --- Page 2 ---\n    doc.add_page_break()',
    # Ch 8
    '    # --- Page 2 ---\n    doc.add_page_break()',
    # Ch 9
    '    # --- Page 2 ---\n    doc.add_page_break()',
    # Ch 10
    '    # --- Page 2 ---\n    doc.add_page_break()',
]

for b in breaks_to_remove:
    if b in code:
        code = code.replace(b, '# (natural page flow)', 1)
        print(f"Removed break: {repr(b[:30])}")
    else:
        print(f"NOT FOUND break: {repr(b[:30])}")

# 5. Update scan_page_map
old_scan = '''def scan_page_map(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    
    # Robust search for start of Chapter 1 body:
    ch1_pno = None
    for pno, page in enumerate(doc):
        text = page.get_text()
        if "ในสถาบันอุดมศึกษาขนาดใหญ่" in text and "บทที่ 1" in text:
            ch1_pno = pno
            break
    
    if ch1_pno is None:
        ch1_pno = 7 # fallback

    print(f"Detected Chapter 1 Body at PDF Page {ch1_pno + 1}")

    headings = [
        ("ch1", r"บทที่\\s+1\\b"),
        ("ch1_2", r"1\\.2\\s+โอกาสทางการตลาด"),
        ("ch1_4", r"1\\.4\\s+วัตถุประสงค์"),
        ("ch1_5", r"1\\.5\\s+ขอบเขตของโครงงาน"),
        ("ch2", r"บทที่\\s+2\\b"),
        ("ch2_4", r"2\\.4\\s+เป้าหมายเชิงกลยุทธ์"),
        ("ch3", r"บทที่\\s+3\\b"),
        ("ch3_3", r"3\\.3\\s+การเปรียบเทียบคุณค่า"),
        ("ch4", r"บทที่\\s+4\\b"),
        ("ch4_2", r"4\\.2\\s+สถาปัตยกรรมระบบ"),
        ("ch4_3", r"4\\.3\\s+ภาพจำลอง"),
        ("ch5", r"บทที่\\s+5\\b"),
        ("ch5_2", r"5\\.2\\s+ข้อมูลจำลอง"),
        ("ch5_3", r"5\\.3\\s+การประมาณการ"),
        ("ch6", r"บทที่\\s+6\\b"),
        ("ch6_1", r"6\\.1\\s+พันธมิตรหลัก"),
        ("ch6_6", r"6\\.6\\s+ช่องทางการเข้าถึง"),
        ("ch7", r"บทที่\\s+7\\b"),
        ("ch7_2", r"7\\.2\\s+กลยุทธ์ส่วนประสม"),
        ("ch8", r"บทที่\\s+8\\b"),
        ("ch8_2", r"หมวดที่\\s+3:\\s+Experience|8\\.2\\s+การคุ้มครอง"),
        ("ch9", r"บทที่\\s+9\\b"),
        ("ch9_2", r"9\\.2\\s+เมทริกซ์"),
        ("ch10", r"บทที่\\s+10\\b"),
        ("ch10_3", r"10\\.3\\s+การวิเคราะห์จุดคุ้มทุน"),
        ("ref", r"บรรณานุกรม"),
        ("app_a", r"ภาคผนวก\\s+ก"),
        ("app_b", r"ภาคผนวก\\s+ข"),
        ("tbl_2_1", r"ตารางที่\\s+2\\.1"),
        ("tbl_3_1", r"ตารางที่\\s+3\\.1"),
        ("tbl_5_1", r"ตารางที่\\s+5\\.1"),
        ("tbl_9_1", r"ตารางที่\\s+9\\.1"),
        ("tbl_10_1", r"ตารางที่\\s+10\\.1"),
        ("tbl_b_1", r"ตารางที่\\s+ข\\.1"),
        ("fig_4_1", r"รูปที่\\s+4\\.1"),
        ("fig_4_2", r"รูปที่\\s+4\\.2"),
        ("fig_6_1", r"รูปที่\\s+6\\.1"),
        ("fig_7_1", r"รูปที่\\s+7\\.1"),
        ("fig_9_1", r"รูปที่\\s+9\\.1"),
        ("fig_a_1", r"รูปที่\\s+ก\\.1"),
    ]

    p_map = {}
    for key, pattern in headings:
        for pno in range(ch1_pno, len(doc)):
            text = doc[pno].get_text()
            if re.search(pattern, text):
                arabic_page = str(pno - ch1_pno + 1)
                p_map[key] = arabic_page
                break
    doc.close()
    return p_map'''

new_scan = '''def scan_page_map(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    
    # Robust search for start of Chapter 1 body:
    ch1_pno = None
    for pno, page in enumerate(doc):
        text = page.get_text().replace('\\u200b', '')
        if "ในสถาบันอุดมศึกษาขนาดใหญ่" in text and "บทที่ 1" in text:
            ch1_pno = pno
            break
    
    if ch1_pno is None:
        ch1_pno = 7 # fallback

    print(f"Detected Chapter 1 Body at PDF Page {ch1_pno + 1}")

    headings = [
        ("ch1", r"บทที่\\s*1\\b"),
        ("ch1_2", r"1\\.2\\s+"),
        ("ch1_4", r"1\\.4\\s+"),
        ("ch1_5", r"1\\.5\\s+"),
        ("ch2", r"บทที่\\s*2\\b"),
        ("ch2_4", r"2\\.4\\s+"),
        ("ch3", r"บทที่\\s*3\\b"),
        ("ch3_3", r"3\\.3\\s+"),
        ("ch4", r"บทที่\\s*4\\b"),
        ("ch4_2", r"4\\.2\\s+"),
        ("ch4_3", r"4\\.3\\s+"),
        ("ch5", r"บทที่\\s*5\\b"),
        ("ch5_2", r"5\\.2\\s+"),
        ("ch5_3", r"5\\.3\\s+"),
        ("ch6", r"บทที่\\s*6\\b"),
        ("ch6_1", r"6\\.1\\s+"),
        ("ch6_6", r"6\\.6\\s+"),
        ("ch7", r"บทที่\\s*7\\b"),
        ("ch7_2", r"7\\.2\\s+"),
        ("ch8", r"บทที่\\s*8\\b"),
        ("ch8_2", r"8\\.2\\s+|หมวดที่\\s*3"),
        ("ch9", r"บทที่\\s*9\\b"),
        ("ch9_2", r"9\\.2\\s+"),
        ("ch10", r"บทที่\\s*10\\b"),
        ("ch10_3", r"10\\.3\\s+"),
        ("ref", r"บรรณานุกรม"),
        ("app_a", r"ภาคผนวก\\s*ก"),
        ("app_b", r"ภาคผนวก\\s*ข"),
        ("tbl_2_1", r"ตารางที่\\s*2\\.1"),
        ("tbl_3_1", r"ตารางที่\\s*3\\.1"),
        ("tbl_5_1", r"ตารางที่\\s*5\\.1"),
        ("tbl_9_1", r"ตารางที่\\s*9\\.1"),
        ("tbl_10_1", r"ตารางที่\\s*10\\.1"),
        ("tbl_b_1", r"ตารางที่\\s*ข\\.1"),
        ("fig_4_1", r"รูปที่\\s*4\\.1"),
        ("fig_4_2", r"รูปที่\\s*4\\.2"),
        ("fig_6_1", r"รูปที่\\s*6\\.1"),
        ("fig_7_1", r"รูปที่\\s*7\\.1"),
        ("fig_9_1", r"รูปที่\\s*9\\.1"),
        ("fig_a_1", r"รูปที่\\s*ก\\.1"),
    ]

    p_map = DEFAULT_PAGE_MAP.copy()
    for key, pattern in headings:
        for pno in range(ch1_pno, len(doc)):
            text = doc[pno].get_text().replace('\\u200b', '')
            if re.search(pattern, text):
                arabic_page = str(pno - ch1_pno + 1)
                p_map[key] = arabic_page
                break
    doc.close()
    return p_map'''

if old_scan in code:
    code = code.replace(old_scan, new_scan, 1)
    print("Replaced scan_page_map successfully.")
else:
    print("WARNING: old_scan not found.")

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved updated build_report.py successfully.")
