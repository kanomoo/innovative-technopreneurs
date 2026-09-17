import os
import sys
import shutil
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
import win32com.client
import fitz

sys.path.append(r'C:\Project\innovative-technopreneurs\Project_Smart_Queue_Food\scripts')
from report_helpers import (
    BASE_DIR, ASSETS_DIR, DOCX_OUTPUT, PDF_OUTPUT,
    thai_zwsp, set_run_font, format_paragraph, add_body_p,
    add_numbered_item, add_bullet_item,
    add_heading_1, add_heading_2, add_heading_3, add_chapter_title,
    add_figure, add_styled_table, add_reference_item
)

def clear_pg_num_types(sec):
    for pnt in sec._sectPr.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgNumType'):
        sec._sectPr.remove(pnt)

def add_toc_line(doc, title, page, is_bold=False, indent=0):
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
    
    r_tab = p.add_run(f"\t{page}")
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
    r2 = p.add_run(f"\t{right_label}")
    set_run_font(r2, size_pt=14, bold=True)
    return p

def add_header_page_field(header_obj):
    h_p = header_obj.paragraphs[0]
    format_paragraph(h_p, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.RIGHT)
    h_p.paragraph_format.first_line_indent = Inches(0)
    h_p.paragraph_format.left_indent = Inches(0)
    h_run = h_p.add_run()
    set_run_font(h_run, size_pt=14)
    h_run._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w')))
    h_run._r.append(parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w')))
    h_run._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w')))
    h_run._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w')))

DEFAULT_PAGE_MAP = {
    'ch1': '1', 'ch1_2': '2', 'ch1_5': '3',
    'ch2': '4', 'ch2_4': '5',
    'ch3': '6', 'ch3_3': '7',
    'ch4': '8', 'ch4_2': '9', 'ch4_3': '10',
    'ch5': '11', 'ch5_3': '12',
    'ch6': '13', 'ch6_3': '14', 'ch6_7': '15',
    'ch7': '16', 'ch7_2': '17',
    'ch8': '18', 'ch8_2': '19',
    'ch9': '20', 'ch9_3': '21',
    'ch10': '22', 'ch10_3': '22', 'ch10_4': '23',
    'ref': '24', 'app_a': '25', 'app_b': '26',
    'tbl_2_1': '5', 'tbl_3_1': '7', 'tbl_5_1': '11', 'tbl_9_1': '21', 'tbl_10_1': '22', 'tbl_b_1': '26',
    'fig_4_1': '9', 'fig_4_2': '10', 'fig_6_1': '13', 'fig_7_1': '16', 'fig_9_1': '20', 'fig_a_1': '25'
}

def build_doc(toc_pages=None):
    if toc_pages is None:
        toc_pages = DEFAULT_PAGE_MAP.copy()
    else:
        merged = DEFAULT_PAGE_MAP.copy()
        merged.update(toc_pages)
        toc_pages = merged

    doc = docx.Document()

    # =========================================================================
    # SECTION 0: COVER PAGE (หน้าปกนอก - 1 หน้าพอดีเป๊ะ)
    # =========================================================================
    sec_cover = doc.sections[0]
    sec_cover.top_margin = Inches(1.0)
    sec_cover.bottom_margin = Inches(1.0)
    sec_cover.left_margin = Inches(1.5)
    sec_cover.right_margin = Inches(1.0)
    sec_cover.page_width = Inches(8.27)
    sec_cover.page_height = Inches(11.69)
    sec_cover.different_first_page_header_footer = True
    clear_pg_num_types(sec_cover)

    # KMUTNB Logo
    logo_path = os.path.join(ASSETS_DIR, 'kmutnb_logo.png')
    p_logo = doc.add_paragraph()
    format_paragraph(p_logo, space_before=0, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_logo.paragraph_format.first_line_indent = Inches(0)
    r_logo = p_logo.add_run()
    if os.path.exists(logo_path):
        r_logo.add_picture(logo_path, width=Inches(1.3))

    # Project Title
    p_title = doc.add_paragraph()
    format_paragraph(p_title, space_before=0, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_title.paragraph_format.first_line_indent = Inches(0)
    r_t_en = p_title.add_run("Smart Queue Food:\nAn Intelligent Pre-ordering and Queue Management System for University\n")
    set_run_font(r_t_en, size_pt=15, bold=True)
    r_t_th = p_title.add_run("ระบบสั่งอาหารและจัดการคิวอัจฉริยะในโรงอาหารมหาวิทยาลัย")
    set_run_font(r_t_th, size_pt=17, bold=True)

    # Submission info
    p_to = doc.add_paragraph()
    format_paragraph(p_to, space_before=14, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_to.paragraph_format.first_line_indent = Inches(0)
    r_to1 = p_to.add_run("เสนอ\n")
    set_run_font(r_to1, size_pt=15, bold=False)
    r_to2 = p_to.add_run("อาจารย์ผู้สอนประจำวิชา 080203914 ผู้ประกอบการนวัตกรรม (Innovative Technopreneurs)")
    set_run_font(r_to2, size_pt=15, bold=False)

    # Group info
    p_grp = doc.add_paragraph()
    format_paragraph(p_grp, space_before=8, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_grp.paragraph_format.first_line_indent = Inches(0)
    r_grp1 = p_grp.add_run("จัดทำโดย\n")
    set_run_font(r_grp1, size_pt=16, bold=True)
    r_grp2 = p_grp.add_run("กลุ่ม “พี่หล่อไหมน้องงงง” (กลุ่มที่ 1)")
    set_run_font(r_grp2, size_pt=16, bold=True)

    # Students Table (3 cols: First Name, Last Name, ID)
    students = [
        ("นายจิณณะ", "พันธุมงคล", "6806021612053"),
        ("นายปภาวิน", "ธิติชุณหกุล", "6806021612037"),
        ("นายดนุสรณ์", "อุปรี", "6806021611413"),
        ("นายนัทธพงศ์", "ธนะเพิ่ม", "6806021612258"),
        ("นายภัทรพล", "แจ่มดวง", "6806021612011"),
        ("นางสาวกนกวรรณ", "เทพสถิตย์", "6806021611171"),
        ("นางสาวณัฐธิดา", "ตันอิน", "6806021612291"),
        ("นายปรัชญา", "เรืองโรจน์", "6806021612347"),
    ]

    tbl_mem = doc.add_table(rows=8, cols=3)
    tbl_mem.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_mem.autofit = False

    tbl_borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/><w:bottom w:val="none"/><w:left w:val="none"/>'
        f'<w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tbl_mem._tbl.tblPr.append(tbl_borders)

    col_widths = [Inches(1.5), Inches(1.6), Inches(1.5)]
    for r_idx, s in enumerate(students):
        row = tbl_mem.rows[r_idx]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:trHeight {nsdecls("w")} w:val="250" w:hRule="atLeast"/>'))
        for c_idx, text in enumerate(s):
            cell = row.cells[c_idx]
            tcPr = cell._tc.get_or_add_tcPr()
            twips = int(col_widths[c_idx].inches * 1440)
            tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{twips}" w:type="dxa"/>'))
            tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:left w:w="40" w:type="dxa"/><w:right w:w="40" w:type="dxa"/></w:tcMar>')
            tcPr.append(tcMar)
            
            p = cell.paragraphs[0]
            format_paragraph(p, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.LEFT)
            p.paragraph_format.first_line_indent = Inches(0)
            r = p.add_run(text)
            set_run_font(r, size_pt=15)

    # University Footer
    p_bot = doc.add_paragraph()
    format_paragraph(p_bot, space_before=14, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_bot.paragraph_format.first_line_indent = Inches(0)
    r_bot = p_bot.add_run(
        "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ\n"
        "คณะเทคโนโลยีและการจัดการอุตสาหกรรม ภาควิชาเทคโนโลยีสารสนเทศ\n"
        "ภาคเรียนที่ 1 ปีการศึกษา 2569"
    )
    set_run_font(r_bot, size_pt=15, bold=False)

    # =========================================================================
    # SECTION 1: PRELIMINARY PAGES (ก, ข, ค, ง, จ, ฉ)
    # =========================================================================
    sec_prelim = doc.add_section(WD_SECTION.NEW_PAGE)
    sec_prelim.top_margin = Inches(1.5)
    sec_prelim.bottom_margin = Inches(1.0)
    sec_prelim.left_margin = Inches(1.5)
    sec_prelim.right_margin = Inches(1.0)
    sec_prelim.different_first_page_header_footer = False
    sec_prelim.header.is_linked_to_previous = False
    clear_pg_num_types(sec_prelim)
    sec_prelim._sectPr.append(parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="thaiLetters" w:start="1"/>'))
    add_header_page_field(sec_prelim.header)

    # --- PREFACE (คำนำ - หน้า ก) ---
    p_pref_title = doc.add_paragraph()
    format_paragraph(p_pref_title, space_before=14, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_pref_title.paragraph_format.first_line_indent = Inches(0)
    r_pref = p_pref_title.add_run("คำนำ")
    set_run_font(r_pref, size_pt=18, bold=True)

    add_body_p(doc, "รายงานโครงงานฉบับนี้จัดทำขึ้นเพื่อเป็นส่วนหนึ่งของรายวิชา 080203914 ผู้ประกอบการนวัตกรรม (Innovative Technopreneurs) ภาคการศึกษาที่ 1 ปีการศึกษา 2569 โดยมีวัตถุประสงค์เพื่อนำองค์ความรู้ด้านการพัฒนานวัตกรรม การวิเคราะห์โมเดลธุรกิจ และกระบวนการคิดเชิงออกแบบ (Design Thinking) มาประยุกต์ใช้ในการแก้ไขปัญหาจริงในชีวิตประจำวันของประชาคมชาวมหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ (มจพ.)")
    add_body_p(doc, "คณะผู้จัดทำได้เลือกศึกษาและพัฒนาโครงงานเรื่อง “Smart Queue Food: ระบบสั่งอาหารและจัดการคิวอัจฉริยะในโรงอาหารมหาวิทยาลัยผ่าน LINE Official Account” เพื่อแก้ไขปัญหาความแออัด การรอคอยคิวที่ยาวนานในช่วงเวลาเร่งด่วน และเพิ่มประสิทธิภาพการบริหารจัดการคำสั่งซื้อของร้านค้า โดยบูรณาการเทคโนโลยีดิจิทัลที่เข้าถึงง่าย เช่น LINE Front-end Framework (LIFF), ระบบชำระเงิน Dynamic PromptPay QR Code, และระบบ Kitchen Display System (KDS)")
    add_body_p(doc, "คณะผู้จัดทำขอขอบพระคุณอาจารย์ผู้สอนประจำวิชาผู้ประกอบการนวัตกรรม ที่ได้กรุณาให้คำแนะนำ ถ่ายทอดองค์ความรู้ และชี้แนะแนวทางอันเป็นประโยชน์ยิ่งตลอดการจัดทำโครงงาน รวมถึงขอขอบคุณผู้ประกอบการร้านอาหาร นักศึกษา และบุคลากรในโรงอาหารกลาง มจพ. ทุกท่านที่ให้ความร่วมมือในการตอบแบบสอบถามและให้ข้อมูลเชิงลึก คณะผู้จัดทำหวังเป็นอย่างยิ่งว่ารายงานโครงงานฉบับนี้จะเป็นประโยชน์และสร้างแรงบันดาลใจในการพัฒนานวัตกรรมเทคโนโลยีเพื่อสังคมต่อไป")

    p_sig = doc.add_paragraph()
    format_paragraph(p_sig, space_before=16, space_after=2, align=WD_ALIGN_PARAGRAPH.RIGHT)
    p_sig.paragraph_format.first_line_indent = Inches(0)
    r_s = p_sig.add_run("คณะผู้จัดทำ กลุ่ม “พี่หล่อไหมน้องงงง”")
    set_run_font(r_s, size_pt=15, bold=True)

    p_date = doc.add_paragraph()
    format_paragraph(p_date, space_before=2, space_after=0, align=WD_ALIGN_PARAGRAPH.RIGHT)
    p_date.paragraph_format.first_line_indent = Inches(0)
    r_d = p_date.add_run("วันที่ 1 ตุลาคม พ.ศ. 2569")
    set_run_font(r_d, size_pt=14)

    doc.add_page_break()

    # --- ABSTRACT (บทคัดย่อ - หน้า ข) ---
    p_abs_title = doc.add_paragraph()
    format_paragraph(p_abs_title, space_before=14, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_abs_title.paragraph_format.first_line_indent = Inches(0)
    r_abs = p_abs_title.add_run("บทคัดย่อ")
    set_run_font(r_abs, size_pt=18, bold=True)

    add_body_p(doc, "โครงงานเรื่อง “Smart Queue Food: ระบบสั่งอาหารและจัดการคิวอัจฉริยะในโรงอาหารมหาวิทยาลัยผ่าน LINE Official Account” มีวัตถุประสงค์เพื่อแก้ไขปัญหาความแออัดและการรอคอยคิวที่ยาวนานในช่วงเวลาเร่งด่วน (11:30 - 13:00 น.) ในโรงอาหารมหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ ซึ่งการสำรวจพบว่านักศึกษาและบุคลากรต้องใช้เวลารออาหารเฉลี่ย 20 ถึง 30 นาทีต่อมื้อ ส่งผลกระทบต่อเวลาเรียนและการปฏิบัติงาน")
    add_body_p(doc, "คณะผู้จัดทำได้นำระเบียบวิธี Lean Startup, Business Model Canvas และกลยุทธ์นวัตกรรม '3 หมวด 10 ยุทธวิธี' มาใช้ออกแบบระบบ โดยพัฒนาส่วนต่อประสานบน LINE Official Account (LIFF) ประกอบด้วย 5 ฟังก์ชันหลัก ได้แก่ ระบบสั่งอาหารล่วงหน้า, ระบบจัดสรรคิวไดนามิก, ระบบ PromptPay QR Code ไร้เงินสด, ระบบแจ้งเตือน 3 ขั้นตอนผ่าน LINE API และระบบ Kitchen Display System (KDS) สำหรับร้านค้า")
    add_body_p(doc, "ผลการศึกษาและทดสอบแนวคิดพบว่า ระบบ Smart Queue Food สามารถลดระยะเวลาการรอคอยอาหารลงได้มากกว่าร้อยละ 70 เพิ่มยอดขายให้ร้านค้าร้อยละ 25 โดยมีโครงสร้างรายได้จากค่าธรรมเนียมร้อยละ 3 ถึง 5 และค่าบริการวิเคราะห์ข้อมูลร้านค้า 199 บาทต่อเดือน มีระยะเวลาคืนทุนประมาณ 7 เดือน โครงงานนี้จึงเป็นต้นแบบที่มีศักยภาพสูงในการยกระดับโรงอาหารมหาวิทยาลัยสู่การเป็น Smart Canteen")
    add_body_p(doc, "ผู้ประกอบการนวัตกรรม, Business Model Canvas, ระบบสั่งอาหารล่วงหน้า, การบริหารจัดการคิว, LINE Official Account, โรงอาหารอัจฉริยะ, มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", bold_prefix="คำสำคัญ: ")

    doc.add_page_break()

    # --- TABLE OF CONTENTS - PART 1 (สารบัญ - หน้า ค: บทที่ 1 ถึง 5) ---
    p_toc_title = doc.add_paragraph()
    format_paragraph(p_toc_title, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_toc_title.paragraph_format.first_line_indent = Inches(0)
    r_toc = p_toc_title.add_run("สารบัญ")
    set_run_font(r_toc, size_pt=18, bold=True)
    add_toc_col_header(doc, "เรื่อง", "หน้า")

    add_toc_line(doc, "คำนำ", "ก", is_bold=True)
    add_toc_line(doc, "บทคัดย่อ", "ข", is_bold=True)
    add_toc_line(doc, "สารบัญ", "ค", is_bold=True)
    add_toc_line(doc, "สารบัญตาราง", "จ", is_bold=True)
    add_toc_line(doc, "สารบัญภาพ", "ฉ", is_bold=True)
    add_toc_line(doc, "บทที่ 1  บทนำและแนวคิดธุรกิจ", toc_pages['ch1'], is_bold=True)
    add_toc_line(doc, "1.1  ความเป็นมาและความสำคัญของปัญหา", toc_pages['ch1'], indent=0.25)
    add_toc_line(doc, "1.2  โอกาสทางการตลาดและพฤติกรรมผู้บริโภค", toc_pages['ch1_2'], indent=0.25)
    add_toc_line(doc, "1.3  แนวคิดและคำตอบของนวัตกรรม", toc_pages['ch1_2'], indent=0.25)
    add_toc_line(doc, "1.4  วัตถุประสงค์ของโครงงาน", toc_pages['ch1_2'], indent=0.25)
    add_toc_line(doc, "1.5  ขอบเขตของโครงงาน", toc_pages['ch1_5'], indent=0.25)
    add_toc_line(doc, "1.6  ประโยชน์ที่คาดว่าจะได้รับ", toc_pages['ch1_5'], indent=0.25)
    add_toc_line(doc, "1.7  นิยามศัพท์เฉพาะ", toc_pages['ch1_5'], indent=0.25)
    add_toc_line(doc, "บทที่ 2  วิสัยทัศน์ พันธกิจ และเป้าหมายขององค์กร", toc_pages['ch2'], is_bold=True)
    add_toc_line(doc, "2.1  วิสัยทัศน์ (Vision)", toc_pages['ch2'], indent=0.25)
    add_toc_line(doc, "2.2  พันธกิจ (Mission)", toc_pages['ch2'], indent=0.25)
    add_toc_line(doc, "2.3  ค่านิยมหลักขององค์กร (Core Values)", toc_pages['ch2'], indent=0.25)
    add_toc_line(doc, "2.4  เป้าหมายเชิงกลยุทธ์ระยะสั้น ระยะกลาง และระยะยาว", toc_pages['ch2_4'], indent=0.25)
    add_toc_line(doc, "บทที่ 3  คุณค่าที่ส่งมอบและความได้เปรียบทางการแข่งขัน", toc_pages['ch3'], is_bold=True)
    add_toc_line(doc, "3.1  คุณค่าหลักที่ส่งมอบแก่ผู้มีส่วนได้ส่วนเสีย", toc_pages['ch3'], indent=0.25)
    add_toc_line(doc, "3.2  การวิเคราะห์ผืนผ้าใบคุณค่า (Value Proposition Canvas)", toc_pages['ch3'], indent=0.25)
    add_toc_line(doc, "3.3  การเปรียบเทียบคุณค่าเชิงลึกกับทางเลือกอื่นในตลาด", toc_pages['ch3_3'], indent=0.25)
    add_toc_line(doc, "บทที่ 4  คุณลักษณะของผลิตภัณฑ์ บริการ และสถาปัตยกรรมระบบ", toc_pages['ch4'], is_bold=True)
    add_toc_line(doc, "4.1  ฟังก์ชันการทำงานหลัก 5 ระบบของ Smart Queue Food", toc_pages['ch4'], indent=0.25)
    add_toc_line(doc, "4.2  สถาปัตยกรรมระบบและโครงสร้างเทคโนโลยี", toc_pages['ch4_2'], indent=0.25)
    add_toc_line(doc, "4.3  ภาพจำลองส่วนต่อประสานผู้ใช้งานจริง (UI Prototype)", toc_pages['ch4_3'], indent=0.25)
    add_toc_line(doc, "บทที่ 5  กลุ่มลูกค้าเป้าหมายและการวิเคราะห์ตลาด", toc_pages['ch5'], is_bold=True)
    add_toc_line(doc, "5.1  การแบ่งส่วนตลาด (Market Segmentation)", toc_pages['ch5'], indent=0.25)
    add_toc_line(doc, "5.2  ข้อมูลจำลองตัวแทนกลุ่มเป้าหมาย (Customer Personas)", toc_pages['ch5'], indent=0.25)
    add_toc_line(doc, "5.3  การประมาณการขนาดตลาด (TAM, SAM, SOM)", toc_pages['ch5_3'], indent=0.25)

    doc.add_page_break()

    # --- TABLE OF CONTENTS - PART 2 (สารบัญ - หน้า ง: บทที่ 6 ถึง 10, บรรณานุกรม, ภาคผนวก) ---
    p_toc_title2 = doc.add_paragraph()
    format_paragraph(p_toc_title2, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_toc_title2.paragraph_format.first_line_indent = Inches(0)
    r_toc2 = p_toc_title2.add_run("สารบัญ (ต่อ)")
    set_run_font(r_toc2, size_pt=18, bold=True)
    add_toc_col_header(doc, "เรื่อง", "หน้า")

    add_toc_line(doc, "บทที่ 6  แบบจำลองผืนผ้าใบธุรกิจ (Business Model Canvas - BMC)", toc_pages['ch6'], is_bold=True)
    add_toc_line(doc, "6.1  พันธมิตรหลัก (Key Partners)", toc_pages['ch6'], indent=0.25)
    add_toc_line(doc, "6.2  กิจกรรมหลัก (Key Activities)", toc_pages['ch6'], indent=0.25)
    add_toc_line(doc, "6.3  ทรัพยากรหลัก (Key Resources)", toc_pages['ch6_3'], indent=0.25)
    add_toc_line(doc, "6.4  คุณค่าที่ส่งมอบ (Value Propositions)", toc_pages['ch6_3'], indent=0.25)
    add_toc_line(doc, "6.5  ความสัมพันธ์กับลูกค้า (Customer Relationships)", toc_pages['ch6_3'], indent=0.25)
    add_toc_line(doc, "6.6  ช่องทางการเข้าถึง (Channels)", toc_pages['ch6_3'], indent=0.25)
    add_toc_line(doc, "6.7  กลุ่มลูกค้าเป้าหมาย (Customer Segments)", toc_pages['ch6_7'], indent=0.25)
    add_toc_line(doc, "6.8  โครงสร้างต้นทุน (Cost Structure)", toc_pages['ch6_7'], indent=0.25)
    add_toc_line(doc, "6.9  แหล่งที่มารายได้ (Revenue Streams)", toc_pages['ch6_7'], indent=0.25)
    add_toc_line(doc, "บทที่ 7  กลยุทธ์การตลาดและการขาย (Marketing & Sales Strategy)", toc_pages['ch7'], is_bold=True)
    add_toc_line(doc, "7.1  การวางตำแหน่งทางการตลาด (Market Positioning Map)", toc_pages['ch7'], indent=0.25)
    add_toc_line(doc, "7.2  กลยุทธ์ส่วนประสมทางการตลาด 4Ps สำหรับนวัตกรรมบริการ", toc_pages['ch7_2'], indent=0.25)
    add_toc_line(doc, "7.3  กลยุทธ์การเจาะตลาดและการส่งเสริมการขาย (Go-to-Market)", toc_pages['ch7_2'], indent=0.25)
    add_toc_line(doc, "บทที่ 8  กลยุทธ์ด้านเทคโนโลยีและนวัตกรรม (3 หมวด 10 ยุทธวิธี)", toc_pages['ch8'], is_bold=True)
    add_toc_line(doc, "8.1  การวิเคราะห์ตามโมเดล Ten Types of Innovation", toc_pages['ch8'], indent=0.25)
    add_toc_line(doc, "8.2  การคุ้มครองทรัพย์สินทางปัญญาและความได้เปรียบทางเทคโนโลยี", toc_pages['ch8_2'], indent=0.25)
    add_toc_line(doc, "บทที่ 9  การประเมินและการบริหารจัดการความเสี่ยง (Risk Management)", toc_pages['ch9'], is_bold=True)
    add_toc_line(doc, "9.1  การบ่งชี้ความเสี่ยง 6 ด้านตามบทเรียนที่ 11", toc_pages['ch9'], indent=0.25)
    add_toc_line(doc, "9.2  เมทริกซ์การประเมินระดับความเสี่ยง (Risk Assessment Matrix)", toc_pages['ch9'], indent=0.25)
    add_toc_line(doc, "9.3  ตารางประเมินความเสี่ยงและแผนบริหารความต่อเนื่องทางธุรกิจ", toc_pages['ch9_3'], indent=0.25)
    add_toc_line(doc, "บทที่ 10  บทสรุป แผนการดำเนินงาน และความเป็นไปได้ทางการเงิน", toc_pages['ch10'], is_bold=True)
    add_toc_line(doc, "10.1  บทสรุปโครงการ (Executive Summary)", toc_pages['ch10'], indent=0.25)
    add_toc_line(doc, "10.2  แผนงานและเส้นทางการดำเนินโครงการ (Project Roadmap)", toc_pages['ch10'], indent=0.25)
    add_toc_line(doc, "10.3  การวิเคราะห์จุดคุ้มทุนและความเป็นไปได้ทางการเงิน", toc_pages['ch10_3'], indent=0.25)
    add_toc_line(doc, "10.4  ปัจจัยแห่งความสำเร็จ (Critical Success Factors)", toc_pages['ch10_4'], indent=0.25)
    add_toc_line(doc, "10.5  ข้อเสนอแนะและทิศทางการพัฒนาในอนาคต", toc_pages['ch10_4'], indent=0.25)
    add_toc_line(doc, "บรรณานุกรม (References)", toc_pages['ref'], is_bold=True)
    add_toc_line(doc, "ภาคผนวก ก  ภาพถ่ายโปสเตอร์ Business Model Canvas ต้นฉบับ", toc_pages['app_a'], is_bold=True)
    add_toc_line(doc, "ภาคผนวก ข  สรุปผลการสำรวจความคิดเห็นกลุ่มตัวอย่างในโรงอาหาร มจพ.", toc_pages['app_b'], is_bold=True)

    doc.add_page_break()

    # --- LIST OF TABLES (สารบัญตาราง - หน้า จ) ---
    p_lot_title = doc.add_paragraph()
    format_paragraph(p_lot_title, space_before=0, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_lot_title.paragraph_format.first_line_indent = Inches(0)
    r_lot = p_lot_title.add_run("สารบัญตาราง")
    set_run_font(r_lot, size_pt=18, bold=True)
    add_toc_col_header(doc, "ตารางที่", "หน้า")

    add_toc_line(doc, "ตารางที่ 2.1  แผนงานและเป้าหมายเชิงกลยุทธ์ของโครงการ Smart Queue Food", toc_pages['tbl_2_1'])
    add_toc_line(doc, "ตารางที่ 3.1  การเปรียบเทียบความสามารถในการแข่งขันกับทางเลือกอื่นในตลาด", toc_pages['tbl_3_1'])
    add_toc_line(doc, "ตารางที่ 5.1  ตารางสรุปข้อมูลจำลองตัวแทนกลุ่มเป้าหมาย (Customer Personas)", toc_pages['tbl_5_1'])
    add_toc_line(doc, "ตารางที่ 9.1  ตารางการประเมินความเสี่ยงและมาตรการบริหารจัดการความเสี่ยง", toc_pages['tbl_9_1'])
    add_toc_line(doc, "ตารางที่ 10.1  แผนงานและเส้นทางการดำเนินโครงการ Smart Queue Food", toc_pages['tbl_10_1'])
    add_toc_line(doc, "ตารางที่ ข.1  สรุปผลการสำรวจความคิดเห็นและความพึงพอใจของกลุ่มตัวอย่างใน มจพ.", toc_pages['tbl_b_1'])

    doc.add_page_break()

    # --- LIST OF FIGURES (สารบัญภาพ - หน้า ฉ) ---
    p_lof_title = doc.add_paragraph()
    format_paragraph(p_lof_title, space_before=0, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_lof_title.paragraph_format.first_line_indent = Inches(0)
    r_lof = p_lof_title.add_run("สารบัญภาพ")
    set_run_font(r_lof, size_pt=18, bold=True)
    add_toc_col_header(doc, "รูปที่", "หน้า")

    add_toc_line(doc, "รูปที่ 4.1  แผนภาพสถาปัตยกรรมระบบ Smart Queue Food (System Architecture)", toc_pages['fig_4_1'])
    add_toc_line(doc, "รูปที่ 4.2  ภาพจำลองส่วนต่อประสานผู้ใช้งานจริง (UI Prototype)", toc_pages['fig_4_2'])
    add_toc_line(doc, "รูปที่ 6.1  แบบจำลองผืนผ้าใบธุรกิจ 9 ช่อง (Business Model Canvas)", toc_pages['fig_6_1'])
    add_toc_line(doc, "รูปที่ 7.1  แผนภาพการวางตำแหน่งผลิตภัณฑ์ในตลาด (Market Positioning Map)", toc_pages['fig_7_1'])
    add_toc_line(doc, "รูปที่ 9.1  เมทริกซ์การประเมินระดับความเสี่ยง (Risk Assessment Matrix)", toc_pages['fig_9_1'])
    add_toc_line(doc, "รูปที่ ก.1  ภาพถ่ายโปสเตอร์ Business Model Canvas ต้นฉบับโครงงาน Smart Queue Food", toc_pages['fig_a_1'])

    # Helper function for starting chapters
    def start_chapter_section(doc, is_first_chapter=False):
        sec = doc.add_section(WD_SECTION.NEW_PAGE)
        sec.top_margin = Inches(1.5)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.5)
        sec.right_margin = Inches(1.0)
        sec.different_first_page_header_footer = True
        clear_pg_num_types(sec)
        
        if is_first_chapter:
            sec.header.is_linked_to_previous = False
            sec.first_page_header.is_linked_to_previous = False
            sec._sectPr.append(parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="decimal" w:start="1"/>'))
            add_header_page_field(sec.header)
        else:
            sec.header.is_linked_to_previous = True
            sec.first_page_header.is_linked_to_previous = False
        return sec

    # =========================================================================
    # CHAPTER 1: BUSINESS IDEA & PROBLEM STATEMENT (เป๊ะ 3 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc, is_first_chapter=True)
    add_chapter_title(doc, "1", "บทนำและแนวคิดธุรกิจ\n(Business Idea & Problem Statement)")

    add_heading_1(doc, "1.1  ความเป็นมาและความสำคัญของปัญหา (Problem Statement)")
    add_body_p(doc, "ในสถาบันอุดมศึกษาขนาดใหญ่ เช่น มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ (มจพ.) ซึ่งมีจำนวนนักศึกษาและบุคลากรรวมกันมากกว่า 25,000 คน กิจกรรมการรับประทานอาหารกลางวันเป็นกิจวัตรที่มีความหนาแน่นสูงสุด โดยเฉพาะในช่วงเวลาเร่งด่วนระหว่าง 11:30 น. ถึง 13:00 น. ส่งผลให้เกิดปัญหาความแออัดและการรอคอยคิวที่ยาวนานในโรงอาหารอย่างหลีกเลี่ยงไม่ได้")
    add_body_p(doc, "จากการศึกษาและสำรวจข้อมูลเชิงประจักษ์ในโรงอาหารกลาง มจพ. พบปัญหาสำคัญ 4 ประการ ดังนี้:")
    add_numbered_item(doc, "1)", "ระยะเวลารอคอยเฉลี่ย 20-30 นาทีต่อมื้อ คิดเป็นเกือบครึ่งหนึ่งของเวลาพัก ทำให้นักศึกษาตึงเครียดและเข้าเรียนภาคบ่ายล่าช้า", space_after=1)
    add_numbered_item(doc, "2)", "ความแออัดในพื้นที่โรงอาหาร แถวคิวยาวกีดขวางทางเดิน โต๊ะที่นั่งไม่เพียงพอ ส่งผลกระทบต่อสุขอนามัยและบรรยากาศในมหาวิทยาลัย", space_after=1)
    add_numbered_item(doc, "3)", "ความผิดพลาดของคำสั่งซื้อ การจดออเดอร์ด้วยกระดาษช่วงเร่งด่วนทำให้เกิดความผิดพลาด ลำดับคิวสับสน และอาหารตกหล่น", space_after=1)
    add_numbered_item(doc, "4)", "คอขวดขั้นตอนชำระเงิน การสแกนจ่ายเงินหน้าร้านขณะปรุงอาหารทำให้คิวหยุดชะงักจากการรอเปิดหน้าจอและตรวจยอดเงินทีละรายการ", space_after=1)

    add_heading_1(doc, "1.2  โอกาสทางการตลาดและพฤติกรรมผู้บริโภค (Market Opportunity)")
    add_body_p(doc, "จากการวิเคราะห์สภาพแวดล้อมทางเทคโนโลยีและพฤติกรรมของกลุ่มเป้าหมาย พบโอกาสทางธุรกิจ 3 ประการ:")
    add_numbered_item(doc, "1)", "ความคุ้นเคยกับสมาร์ตโฟน: นักศึกษาและบุคลากรทุกคนใช้งาน LINE เป็นประจำ การสั่งผ่าน LINE LIFF จึงเปิดใช้งานได้ทันทีโดยไม่ต้องติดตั้งแอปใหม่", space_after=1)
    add_numbered_item(doc, "2)", "ช่องว่างของแอปเดลิเวอรี่: แพลตฟอร์มทั่วไปคิดค่า GP สูง 30-35% และมีค่าส่ง Smart Queue Food จึงตอบโจทย์ด้วยค่าธรรมเนียมต่ำมากและเน้นรับเอง", space_after=1)
    add_numbered_item(doc, "3)", "นโยบายสนับสนุนของสถาบัน: สอดรับกับยุทธศาสตร์ Smart Campus และสังคมไร้เงินสด (Cashless Society) ของ มจพ. อย่างแท้จริง", space_after=1)

    add_heading_1(doc, "1.3  แนวคิดและคำตอบของนวัตกรรม (Solution Concept)")
    add_body_p(doc, "ระบบ 'Smart Queue Food' เป็นนวัตกรรมบริการดิจิทัลบน LINE Official Account เชื่อมโยงผู้บริโภคเข้ากับหน้าจอจัดการครัว (KDS) และระบบชำระเงิน PromptPay ผู้ใช้สามารถเลือกดูเมนู สั่งอาหารล่วงหน้าก่อนเวลาพัก เลือกรอบเวลารับอาหาร และชำระเงินดิจิทัลทันที เมื่อร้านค้าปรุงอาหารใกล้เสร็จ ระบบจะส่งข้อความแจ้งเตือนผ่าน LINE ให้นักศึกษาเดินมารับอาหารได้พอดีเวลาโดยไม่ต้องยืนรอคิวหน้าร้าน")

    add_heading_1(doc, "1.4  วัตถุประสงค์ของโครงงาน")
    add_numbered_item(doc, "1)", "เพื่อพัฒนาระบบสั่งอาหารล่วงหน้าและจัดการคิวออนไลน์ผ่าน LINE Official Account สำหรับโรงอาหาร มจพ.", space_after=1)
    add_numbered_item(doc, "2)", "เพื่อลดระยะเวลาการรอคอยอาหารของนักศึกษาและบุคลากรในช่วงเวลาเร่งด่วนลงไม่น้อยกว่าร้อยละ 60-70", space_after=1)
    add_numbered_item(doc, "3)", "เพื่อเพิ่มประสิทธิภาพการจัดการคำสั่งซื้อและขยายขีดความสามารถการจำหน่ายอาหารของร้านค้าในโรงอาหาร", space_after=1)
    add_numbered_item(doc, "4)", "เพื่อศึกษาความเป็นไปได้ทางธุรกิจและจัดทำแบบจำลองธุรกิจนวัตกรรม (BMC) ที่ต่อยอดเชิงพาณิชย์ได้จริง", space_after=1)

    add_heading_1(doc, "1.5  ขอบเขตของโครงงาน (Project Scope)")
    add_numbered_item(doc, "1)", "ดำเนินการศึกษาและพัฒนาระบบนำร่อง ณ โรงอาหารกลาง มจพ. (กรุงเทพฯ) เชื่อมต่อร้านค้านำร่อง 15 ร้าน ครอบคลุมนักศึกษา อาจารย์ และบุคลากร", bold_prefix="ขอบเขตด้านพื้นที่และกลุ่มเป้าหมาย: ", space_after=1)
    add_numbered_item(doc, "2)", "ครอบคลุมระบบ LINE LIFF, ระบบจัดคิวไดนามิก, ชำระเงิน Dynamic PromptPay, ระบบแจ้งเตือนอัตโนมัติ และระบบหน้าจอร้านค้า (KDS)", bold_prefix="ขอบเขตด้านระบบซอฟต์แวร์: ", space_after=1)
    add_numbered_item(doc, "3)", "ดำเนินงานตลอดภาคเรียนที่ 1 ปีการศึกษา 2569 ตั้งแต่สำรวจปัญหา ออกแบบสถาปัตยกรรม พัฒนา ทดสอบ จนถึงประเมินผลลัพธ์ธุรกิจ", bold_prefix="ขอบเขตด้านระยะเวลา: ", space_after=1)

    add_heading_1(doc, "1.6  ประโยชน์ที่คาดว่าจะได้รับ (Expected Benefits)")
    add_numbered_item(doc, "1)", "ประหยัดเวลารออาหาร มีเวลาพักผ่อนเพิ่มขึ้น ส่งเสริมสุขอนามัยและประสิทธิภาพการเรียนรู้", bold_prefix="ด้านนักศึกษาและบุคลากร: ", space_after=1)
    add_numbered_item(doc, "2)", "บริหารจัดการคิวในครัวได้อย่างมีแบบแผน ลดข้อผิดพลาดของรายการอาหาร และเพิ่มยอดขายในชั่วโมงเร่งด่วน", bold_prefix="ด้านผู้ประกอบการร้านอาหาร: ", space_after=1)
    add_numbered_item(doc, "3)", "ลดความแออัดในพื้นที่ส่วนรวม ยกระดับความปลอดภัยทางสุขอนามัย และขับเคลื่อนมหาวิทยาลัยสู่ Smart Campus", bold_prefix="ด้านมหาวิทยาลัย: ", space_after=1)

    add_heading_1(doc, "1.7  นิยามศัพท์เฉพาะ (Definitions of Key Terms)")
    add_numbered_item(doc, "1)", "ระบบเว็บแอปพลิเคชันบน LINE ที่ให้บริการสั่งอาหารล่วงหน้า คำนวณเวลารับอาหาร และแจ้งเตือนสถานะคิวแบบเรียลไทม์", bold_prefix="Smart Queue Food: ", space_after=1)
    add_numbered_item(doc, "2)", "ระบบหน้าจอแสดงผลคำสั่งซื้อดิจิทัลสำหรับผู้ประกอบการร้านอาหาร เพื่อจัดลำดับและตัดจ่ายคิวอย่างมีประสิทธิภาพ", bold_prefix="Kitchen Display System (KDS): ", space_after=1)
    add_numbered_item(doc, "3)", "คิวอาร์โค้ดมาตรฐานพร้อมเพย์ที่ฝังยอดเงินถูกต้องตามบิลคำสั่งซื้อโดยอัตโนมัติ เพื่อการชำระเงินที่สะดวกรวดเร็ว", bold_prefix="Dynamic PromptPay QR: ", space_after=1)
    add_numbered_item(doc, "4)", "เวลาการรอคอยโดยประมาณที่คำนวณจากอัลกอริทึมคิวสะสมและความเร็วในการปรุงจริงของแต่ละร้าน", bold_prefix="Estimated Waiting Time (EWT): ", space_after=1)
    add_numbered_item(doc, "5)", "แพลตฟอร์มเว็บแอปที่ทำงานอยู่ภายในแอปพลิเคชัน LINE ช่วยให้เข้าถึงระบบได้ทันทีโดยไม่ต้องดาวน์โหลดแอปเพิ่มเติม", bold_prefix="LINE Front-end Framework (LIFF): ", space_after=1)

    # =========================================================================
    # CHAPTER 2: VISION, MISSION & STRATEGIC GOALS (เป๊ะ 2 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    add_chapter_title(doc, "2", "วิสัยทัศน์ พันธกิจ และเป้าหมายขององค์กร\n(Vision, Mission & Strategic Goals)")

    add_heading_1(doc, "2.1  วิสัยทัศน์ (Vision)")
    add_body_p(doc, "“ก้าวสู่การเป็นแพลตฟอร์มบริหารจัดการคิวและสั่งอาหารในโรงอาหารสถาบันการศึกษาชั้นนำของประเทศ ที่ยกระดับคุณภาพชีวิตของประชาคมมหาวิทยาลัยด้วยเทคโนโลยีดิจิทัลที่เข้าถึงง่าย สะดวกรวดเร็ว และสร้างการเติบโตอย่างยั่งยืนแก่ผู้ประกอบการท้องถิ่น”")

    add_heading_1(doc, "2.2  พันธกิจ (Mission)")
    add_numbered_item(doc, "1)", "พัฒนาระบบสั่งอาหารและคิวออนไลน์ที่ทำงานได้อย่างรวดเร็ว เสถียร และเข้าถึงง่ายผ่าน LINE เพื่อลดเวลาการรอคอยที่สูญเปล่า", space_after=1)
    add_numbered_item(doc, "2)", "สนับสนุนเครื่องมือดิจิทัลที่ใช้งานง่าย เพื่อช่วยให้ร้านอาหารบริหารจัดการครัวได้อย่างเป็นระบบ ลดความผิดพลาด และเพิ่มรายได้", space_after=1)
    add_numbered_item(doc, "3)", "ร่วมมือกับมหาวิทยาลัยในการสร้างระบบนิเวศโรงอาหารอัจฉริยะ สังคมไร้เงินสด และส่งเสริมสุขอนามัยที่ดีในพื้นที่ส่วนรวม", space_after=1)
    add_numbered_item(doc, "4)", "ดำเนินธุรกิจด้วยความโปร่งใส คิดค่าบริการที่เป็นธรรม และมุ่งเน้นการสร้างคุณค่าร่วมกันของผู้มีส่วนได้ส่วนเสียทุกฝ่าย", space_after=1)

    add_heading_1(doc, "2.3  ค่านิยมหลักขององค์กร (Core Values: F-A-S-T)")
    add_bullet_item(doc, "มุ่งเน้นการลดระยะเวลาการรอคอยและการประมวลผลคำสั่งซื้อที่ฉับไว แม่นยำ", bold_prefix="F - Fast (รวดเร็ว): ", space_after=1)
    add_bullet_item(doc, "เข้าถึงได้ทันทีผ่าน LINE โดยไม่มีค่าใช้จ่ายและไม่มีอุปสรรคด้านการติดตั้งแอปพลิเคชัน", bold_prefix="A - Accessible (เข้าถึงง่าย): ", space_after=1)
    add_bullet_item(doc, "การจัดสรรคิวที่แม่นยำและเที่ยงตรงด้วยอัลกอริทึมที่คำนวณตามเวลาจริง", bold_prefix="S - Systematic (เป็นระบบ): ", space_after=1)
    add_bullet_item(doc, "แสดงสถานะคำสั่งซื้อ เวลารอคอย และการชำระเงินที่ตรวจสอบได้ทุกขั้นตอน", bold_prefix="T - Transparent (โปร่งใส): ", space_after=1)

    add_heading_1(doc, "2.4  เป้าหมายเชิงกลยุทธ์ (Strategic Goals)")
    add_body_p(doc, "เพื่อให้การขับเคลื่อนโครงการบรรลุผลสัมฤทธิ์อย่างเป็นรูปธรรม องค์กรได้กำหนดเป้าหมายเชิงกลยุทธ์ 3 ระยะ ดังแสดงในตารางที่ 2.1:")

    strat_headers = ["ระยะเวลา", "เป้าหมายเชิงกลยุทธ์ (Strategic Goals)", "ตัวชี้วัดความสำเร็จ (KPIs)"]
    strat_data = [
        ["ระยะสั้น\n(0 - 6 เดือน)", "1. เปิดใช้งานระบบนำร่องในโรงอาหารกลาง มจพ. 15 ร้านค้า\n2. สร้างฐานผู้ใช้งานนักศึกษาและบุคลากร 3,000 คน\n3. ความพึงพอใจการใช้งานไม่น้อยกว่าร้อยละ 85", "- ลดเวลารอคอยเฉลี่ยลง > 60%\n- ปริมาณออเดอร์ > 800 รายการ/วัน\n- อัตราข้อผิดพลาดของออเดอร์ < 1%"],
        ["ระยะกลาง\n(6 - 12 เดือน)", "1. ขยายบริการครบ 100% ของร้านค้าในโรงอาหารกลาง (30 ร้าน)\n2. เริ่มขยายสู่โรงอาหารอาคาร 40 ปี และโรงอาหารคณะอื่น\n3. ก้าวสู่จุดคุ้มทุน (Break-Even) ทางการเงิน", "- ผู้ใช้งานสะสม > 8,000 คน\n- ยอดคำสั่งซื้อ > 2,000 รายการ/วัน\n- ร้านค้าใช้ระบบวิเคราะห์ข้อมูล 100%"],
        ["ระยะยาว\n(1 - 3 ปี)", "1. ขยายผลสู่ มจพ. วิทยาเขตปราจีนบุรี และระยอง\n2. ขยายสู่สถาบันอุดมศึกษาพันธมิตรในเขตกรุงเทพฯ\n3. พัฒนาระบบ AI แนะนำเมนูอาหารตามหลักโภชนาการ", "- ส่วนแบ่งตลาด > 50% ในสถาบันเป้าหมาย\n- ยอดคำสั่งซื้อ > 10,000 รายการ/วัน\n- รายได้เติบโตยั่งยืน > 3 ล้านบาท/ปี"]
    ]
    add_styled_table(doc, "2.1", "แผนงานและเป้าหมายเชิงกลยุทธ์ของโครงการ Smart Queue Food", strat_headers, strat_data, [Inches(1.2), Inches(3.0), Inches(2.4)])
    add_body_p(doc, "การกำหนดเป้าหมายเชิงกลยุทธ์ดังกล่าวช่วยให้ทีมงานสามารถติดตามความก้าวหน้า ปรับปรุงประสิทธิภาพของซอฟต์แวร์ และบริหารจัดการทรัพยากรได้อย่างมีประสิทธิภาพสูงสุดในทุกช่วงของการพัฒนา")

    # =========================================================================
    # CHAPTER 3: VALUE PROPOSITION & COMPETITIVE ADVANTAGE (เป๊ะ 2 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    add_chapter_title(doc, "3", "คุณค่าที่ส่งมอบและความได้เปรียบทางการแข่งขัน\n(Value Proposition & Competitive Advantage)")

    add_heading_1(doc, "3.1  คุณค่าหลักที่ส่งมอบแก่ผู้มีส่วนได้ส่วนเสีย (Value Propositions)")
    add_numbered_item(doc, "1)", "ประหยัดเวลาการรอคอยอาหารเฉลี่ย 15-20 นาทีต่อมื้อ สามารถสั่งอาหารล่วงหน้าระหว่างเดินเปลี่ยนคาบ ทราบเวลาเสร็จแน่นอน ไม่ต้องยืนรอท่ามกลางความร้อน และจ่ายค่าอาหารตามราคาปกติหน้าร้านโดยไม่มีค่าส่ง", bold_prefix="คุณค่าสำหรับนักศึกษาและบุคลากร: ", space_after=1)
    add_numbered_item(doc, "2)", "สามารถวางแผนการปรุงอาหารล่วงหน้าได้อย่างราบรื่น ลดปัญหาออเดอร์ตกหล่น ลดความแออัดหน้าร้าน เพิ่มขีดความสามารถรับออเดอร์ช่วงเร่งด่วนได้มากขึ้น 20-30% และรับเงินถูกต้องผ่าน PromptPay ไร้ปัญหาเงินทอน", bold_prefix="คุณค่าสำหรับผู้ประกอบการร้านอาหาร: ", space_after=1)
    add_numbered_item(doc, "3)", "ช่วยระบายความแออัดในโรงอาหาร ส่งเสริมสุขอนามัยที่ดี ลดปัญหาการแย่งโต๊ะที่นั่ง และส่งเสริมนโยบาย Smart Campus และสังคมไร้เงินสดอย่างเป็นรูปธรรม", bold_prefix="คุณค่าสำหรับมหาวิทยาลัย: ", space_after=1)

    add_heading_1(doc, "3.2  การวิเคราะห์ผืนผ้าใบคุณค่า (Value Proposition Canvas: VPC)")
    add_body_p(doc, "จากการวิเคราะห์ตามกรอบแนวคิดของ Alexander Osterwalder สรุปความสอดคล้องระหว่าง Customer Profile และ Value Map ได้ดังนี้:")
    add_bullet_item(doc, "การจัดหาอาหารกลางวันรับประทานให้อิ่ม อร่อย ประหยัด และทันเวลาเข้าเรียนหรือเข้าทำงานภาคบ่าย", bold_prefix="Customer Jobs: ", space_after=1)
    add_bullet_item(doc, "การยืนต่อคิวนาน อากาศร้อนอบอ้าว อาหารหมดก่อนถึงคิว ออเดอร์ทำผิด และการไม่มีที่นั่งรับประทาน", bold_prefix="Customer Pains: ", space_after=1)
    add_bullet_item(doc, "มีเวลาพักผ่อนเพิ่มขึ้น ได้รับอาหารตรงเวลา ทราบสถานะคิวที่แน่นอน และการชำระเงินสะดวกรวดเร็ว", bold_prefix="Customer Gains: ", space_after=1)
    add_bullet_item(doc, "ระบบสั่งอาหารล่วงหน้าบน LINE, อัลกอริทึมแสดงเวลารอคอย, ระบบแจ้งเตือนเมื่อปรุงเสร็จ, และชำระเงินดิจิทัลอัตโนมัติ ช่วยแก้ไข Pains และสร้าง Gains ได้อย่างสมบูรณ์", bold_prefix="Pain Relievers & Gain Creators: ", space_after=1)

    add_heading_1(doc, "3.3  การเปรียบเทียบคุณค่าเชิงลึกกับทางเลือกอื่นในตลาด")
    add_body_p(doc, "ตารางที่ 3.1 แสดงการวิเคราะห์เปรียบเทียบความสามารถในการแข่งขันของ Smart Queue Food กับทางเลือกอื่นในตลาด:")

    comp_headers = ["มิติการเปรียบเทียบ", "การสั่งหน้าร้านเดิม", "แอปเดลิเวอรี่ทั่วไป", "ตู้ Kiosk อัตโนมัติ", "Smart Queue Food"]
    comp_data = [
        ["ความสะดวกในการสั่ง", "ต่ำ (ต้องเดินไปหน้าร้าน)", "สูง (สั่งผ่านสมาร์ตโฟน)", "ปานกลาง (ต้องไปหน้าตู้)", "สูงมาก (สั่งผ่าน LINE ได้ทันที)"],
        ["ระยะเวลารอคอยรวม", "20 - 30 นาที", "30 - 45 นาที (รอไรเดอร์)", "15 - 20 นาที", "0 - 3 นาที (เดินมารับตอนเสร็จ)"],
        ["ภาระค่าใช้จ่ายผู้ใช้", "ราคาปกติหน้าร้าน", "ราคาสูงขึ้น (ค่าส่ง +GP)", "ราคาปกติหน้าร้าน", "ราคาปกติหน้าร้าน (ไม่มีค่าส่ง)"],
        ["ค่าธรรมเนียมร้านค้า", "ไม่มี (0%)", "สูงมาก (GP 30 - 35%)", "ค่าเช่า/ซื้อตู้ฮาร์ดแวร์สูง", "ต่ำและเป็นธรรม (GP 3 - 5%)"],
        ["การติดตั้งระบบ", "ไม่ต้องติดตั้ง", "ต้องดาวน์โหลดแอปใหม่", "ต้องติดตั้งตู้ในพื้นที่", "ไม่ต้องติดตั้ง (ใช้งานบน LINE)"],
        ["ความเหมาะสมโรงอาหาร", "เกิดความแออัดสูง", "ไม่เหมาะกับโรงอาหารปิด", "ใช้พื้นที่เยอะ ค่าดูแลสูง", "เหมาะสมสูงสุด (ออกแบบเฉพาะ)"]
    ]
    add_styled_table(doc, "3.1", "การเปรียบเทียบความสามารถในการแข่งขันของ Smart Queue Food กับทางเลือกอื่นในตลาด", comp_headers, comp_data, [Inches(1.4), Inches(1.3), Inches(1.4), Inches(1.3), Inches(1.4)])
    add_body_p(doc, "ผลการเปรียบเทียบชี้ชัดว่า Smart Queue Food ครองความได้เปรียบในการแข่งขันที่โดดเด่น ทั้งในแง่ความสะดวก ประหยัดเวลา ต้นทุนที่เป็นธรรมต่อร้านค้า และความเหมาะสมกับสภาพแวดล้อมของโรงอาหารมหาวิทยาลัยอย่างแท้จริง")

    # =========================================================================
    # CHAPTER 4: PRODUCT CHARACTERISTICS & ARCHITECTURE (เป๊ะ 3 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    add_chapter_title(doc, "4", "คุณลักษณะของผลิตภัณฑ์ บริการ และสถาปัตยกรรมระบบ\n(Product Characteristics & System Architecture)")

    add_heading_1(doc, "4.1  ฟังก์ชันการทำงานหลัก 5 ระบบของ Smart Queue Food")
    add_body_p(doc, "ระบบ Smart Queue Food ได้รับการออกแบบสถาปัตยกรรมระบบและกระบวนการทำงานเพื่อแก้ไขปัญหาคอขวดในโรงอาหารอย่างเป็นระบบ โดยบูรณาการ 5 โมดูลการทำงานหลักเข้าด้วยกัน ดังนี้:")
    add_numbered_item(doc, "1)", "แสดงรายการร้านค้า เมนูอาหาร ภาพประกอบ ราคา และตัวเลือกปรับแต่งอย่างละเอียด เช่น ระดับความเผ็ด การเพิ่มไข่ดาว และหมายเหตุพิเศษ ช่วยให้ผู้ใช้เลือกอาหารและสั่งล่วงหน้าได้อย่างสะดวก", bold_prefix="ระบบแสดงเมนูและสั่งอาหารล่วงหน้า (Pre-ordering & Catalog): ", space_after=1)
    add_numbered_item(doc, "2)", "อัลกอริทึมคำนวณเวลาการรอคอยโดยประมาณ (EWT) โดยนำเวลาปรุงเฉลี่ยของแต่ละเมนูคูณด้วยจำนวนคิวสะสมแบบเรียลไทม์ พร้อมเปิดให้ผู้ใช้เลือกรอบเวลารับอาหารล่วงหน้าได้อย่างแม่นยำ", bold_prefix="ระบบจัดสรรคิวและประเมินเวลารอคอย (Predictive Queue): ", space_after=1)
    add_numbered_item(doc, "3)", "สร้าง Dynamic PromptPay QR Code ที่ฝังยอดเงินตรงตามบิลคำสั่งซื้อโดยอัตโนมัติ พร้อมระบบ Slip Verification API ตรวจสอบสลิปกับธนาคารภายใน 3 วินาที ลดเวลาชำระเงินหน้าร้านให้เป็นศูนย์", bold_prefix="ระบบชำระเงินดิจิทัลไร้เงินสด (PromptPay Payment Gateway): ", space_after=1)
    add_numbered_item(doc, "4)", "ส่งข้อความแจ้งเตือนอัตโนมัติผ่าน LINE Messaging API เข้าสู่แชทของผู้ใช้ 3 ขั้นตอน ได้แก่ ร้านค้ารับออเดอร์, กำลังเริ่มปรุงอาหาร, และอาหารปรุงเสร็จพร้อมรับ เพื่อให้เดินมารับอาหารได้พอดีเวลา", bold_prefix="ระบบแจ้งเตือนสถานะคำสั่งซื้อเรียลไทม์ (Push Notification): ", space_after=1)
    add_numbered_item(doc, "5)", "เว็บแอปพลิเคชันบนแท็บเล็ตประจำร้านค้า แสดงการ์ดออเดอร์เรียงตามลำดับคิวและเวลา พร้อมตัวอักษรขนาดใหญ่และปุ่มกดเปลี่ยนสถานะที่ใช้งานง่าย แม้ในช่วงเวลาเร่งด่วนที่แม่ค้ากำลังปรุงอาหาร", bold_prefix="ระบบหน้าจอจัดการครัวสำหรับร้านค้า (Kitchen Display System: KDS): ", space_after=1)

    add_heading_1(doc, "4.2  สถาปัตยกรรมระบบและโครงสร้างเทคโนโลยี (System Architecture)")
    add_body_p(doc, "รูปที่ 4.1 แสดงสถาปัตยกรรมระบบของ Smart Queue Food ซึ่งออกแบบในรูปแบบ Microservices บนระบบคลาวด์:")

    arch_img = os.path.join(ASSETS_DIR, 'system_architecture.png')
    add_figure(doc, arch_img, "4.1", "แผนภาพสถาปัตยกรรมระบบ Smart Queue Food (System Architecture)", width_inches=3.6)

    add_body_p(doc, "สถาปัตยกรรมระบบแบ่งออกเป็น 4 ระดับการทำงานที่มีความมั่นคงปลอดภัยและความเสถียรสูง ได้แก่:")
    add_numbered_item(doc, "1)", "LINE Front-end Framework (LIFF) สำหรับผู้บริโภค และ Responsive Web Application สำหรับหน้าจอร้านค้า (KDS)", bold_prefix="ระดับที่ 1 Presentation Layer: ", space_after=1)
    add_numbered_item(doc, "2)", "การเข้ารหัสมาตรฐาน HTTPS, ยืนยันตัวตนด้วย LINE Login OAuth 2.1 และ Rate Limiting ป้องกันคำสั่งซื้อซ้ำซ้อน", bold_prefix="ระดับที่ 2 Gateway & Security Layer: ", space_after=1)
    add_numbered_item(doc, "3)", "โมดูลคำนวณคิวอัจฉริยะ (Queue Engine), ระบบตรวจสอบสลิปอัตโนมัติ และระบบกระจายข้อความแจ้งเตือนเรียลไทม์", bold_prefix="ระดับที่ 3 Application & Business Logic: ", space_after=1)
    add_numbered_item(doc, "4)", "Redis Cache สำหรับจัดการลำดับคิวความเร็วสูง และ PostgreSQL สำหรับจัดเก็บข้อมูลธุรกรรมและประวัติคำสั่งซื้อ", bold_prefix="ระดับที่ 4 Data & Cloud Infrastructure: ", space_after=1)

    add_heading_1(doc, "4.3  ภาพจำลองส่วนต่อประสานผู้ใช้งานจริง (UI Prototype & User Experience)")
    add_body_p(doc, "รูปที่ 4.2 แสดงภาพจำลองหน้าจอการทำงานจริงของระบบ Smart Queue Food ทั้ง 4 หน้าจอหลัก:")

    ui_img = os.path.join(ASSETS_DIR, 'ui_mockup.png')
    add_figure(doc, ui_img, "4.2", "ภาพจำลองส่วนต่อประสานผู้ใช้งานจริง (UI Prototype)", width_inches=3.6)

    add_body_p(doc, "การออกแบบส่วนต่อประสานผู้ใช้เน้นความเรียบง่าย สะอาดตา และเข้าใจได้ทันที โดยแบ่งการทำงานออกเป็น 4 หน้าจอ:")
    add_numbered_item(doc, "1)", "แสดงรายการร้านอาหาร รูปภาพ เมนู ราคา และตัวเลือกพิเศษ (เช่น เพิ่มไข่ดาว ไม่ใส่ผัก)", bold_prefix="หน้าจอที่ 1 ค้นหาร้านค้าและเลือกเมนูอาหาร: ", space_after=1)
    add_numbered_item(doc, "2)", "แสดงรายการอาหารที่เลือก ยอดเงินรวม และ Dynamic PromptPay QR Code พร้อมปุ่มแนบสลิป", bold_prefix="หน้าจอที่ 2 สรุปรายการคำสั่งซื้อและการชำระเงิน: ", space_after=1)
    add_numbered_item(doc, "3)", "แสดงหมายเลขคิว เวลารอคอยโดยประมาณ แถบสถานะการปรุง และคำแนะนำการเดินมารับ", bold_prefix="หน้าจอที่ 3 บัตรคิวดิจิทัลและการติดตามสถานะ: ", space_after=1)
    add_numbered_item(doc, "4)", "การ์ดออเดอร์ขนาดใหญ่เรียงตามลำดับเวลา ปุ่มกด 'เริ่มปรุง' และ 'ปรุงเสร็จ' พร้อมส่งเสียงเตือน", bold_prefix="หน้าจอที่ 4 หน้าจอจัดการครัวสำหรับร้านค้า (KDS): ", space_after=1)

    # =========================================================================
    # CHAPTER 5: TARGET CUSTOMERS & MARKET SIZING (เป๊ะ 2 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    add_chapter_title(doc, "5", "กลุ่มลูกค้าเป้าหมายและการวิเคราะห์ตลาด\n(Target Customers & Market Sizing)")

    add_heading_1(doc, "5.1  การแบ่งส่วนตลาด (Market Segmentation)")
    add_body_p(doc, "การแบ่งส่วนตลาดของ Smart Queue Food พิจารณาตาม 4 ปัจจัยหลัก:")
    add_bullet_item(doc, "นักศึกษาและบุคลากรอายุ 18 - 60 ปี คุ้นเคยกับการใช้สมาร์ตโฟนและกระเป๋าเงินดิจิทัล", bold_prefix="เกณฑ์ประชากรศาสตร์: ", space_after=1)
    add_bullet_item(doc, "ประชาคมที่ใช้ชีวิตประจำวันในวิทยาเขตหลัก มจพ. กรุงเทพฯ (ถนนวงศ์สว่าง)", bold_prefix="เกณฑ์ภูมิศาสตร์: ", space_after=1)
    add_bullet_item(doc, "ผู้ที่ซื้ออาหารรับประทานเป็นประจำ มีเวลาพักเที่ยงจำกัด และไม่ชอบการยืนต่อคิวยาว", bold_prefix="เกณฑ์พฤติกรรมศาสตร์: ", space_after=1)
    add_bullet_item(doc, "กลุ่มที่ให้ความสำคัญกับการบริหารเวลาและชื่นชอบความสะดวกสบายของเทคโนโลยี", bold_prefix="เกณฑ์จิตวิทยา: ", space_after=1)

    add_heading_1(doc, "5.2  ข้อมูลจำลองผู้ใช้งาน (Customer Personas)")
    add_body_p(doc, "ตารางที่ 5.1 สรุปข้อมูลจำลองตัวแทนกลุ่มเป้าหมายหลัก 2 กลุ่มของโครงการ:")

    persona_headers = ["ข้อมูลจำลอง", "Persona 1: นักศึกษาปริญญาตรี", "Persona 2: บุคลากร / อาจารย์"]
    persona_data = [
        ["ชื่อ - โปรไฟล์", "นายสมชาย เร่งรีบ (อายุ 20 ปี)", "ดร.กนกพร ผู้บริหารเวลา (อายุ 42 ปี)"],
        ["บทบาท", "นักศึกษาคณะวิศวกรรมศาสตร์ ชั้นปีที่ 2", "อาจารย์ประจำคณะวิทยาศาสตร์ประยุกต์"],
        ["เป้าหมายหลัก", "รับประทานอาหารกลางวันทันเวลาเข้าแล็บ 13:00 น.", "ใช้เวลาพักกลางวันตรวจงานวิจัยและทานอาหาร"],
        ["จุดเจ็บปวด (Pain)", "รอคิวนาน 25 นาที โต๊ะเต็ม ต้องรีบกินจนปวดท้อง", "ไม่มีเวลาเดินไปต่อคิว อารมณ์เสียกับความแออัด"],
        ["การใช้งานระบบ", "สั่งอาหารล่วงหน้าก่อนปล่อยคาบเรียน 10 นาที", "สั่งอาหารให้ปรุงเสร็จพอดีเวลาเดินลงจากอาคาร"]
    ]
    add_styled_table(doc, "5.1", "ตารางสรุปข้อมูลจำลองตัวแทนกลุ่มเป้าหมาย (Customer Personas)", persona_headers, persona_data, [Inches(1.5), Inches(2.6), Inches(2.5)])

    add_heading_1(doc, "5.3  การประมาณการขนาดตลาด (TAM, SAM, SOM)")
    add_body_p(doc, "การประเมินขนาดตลาดตามระเบียบวิธีวิเคราะห์ธุรกิจเทคโนโลยี:")
    add_numbered_item(doc, "1)", "โรงอาหารในสถาบันอุดมศึกษาทั่วประเทศประมาณ 150 แห่ง นักศึกษาและบุคลากรกว่า 1.5 ล้านคน มูลค่าการใช้จ่ายอาหารกลางวันเฉลี่ย 4,500 ล้านบาทต่อปี (คำนวณจากค่าอาหารเฉลี่ย 50 บาท/มื้อ x 200 วันทำการ)", bold_prefix="Total Addressable Market (TAM): ", space_after=1)
    add_numbered_item(doc, "2)", "โรงอาหารในสถาบันอุดมศึกษาเขตกรุงเทพฯ และปริมณฑล 30 แห่ง นักศึกษาและบุคลากรรวมประมาณ 300,000 คน มูลค่าตลาดอาหารกลางวันประมาณ 900 ล้านบาทต่อปี", bold_prefix="Serviceable Available Market (SAM): ", space_after=1)
    add_numbered_item(doc, "3)", "โรงอาหารกลาง มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ (กรุงเทพฯ) นักศึกษาและบุคลากรเป้าหมาย 12,000 คน มูลค่าตลาดอาหารกลางวันประมาณ 36 ล้านบาทต่อปี โดยโครงการตั้งเป้าหมายเจาะตลาดนำร่องร้อยละ 25 ในปีแรก (มูลค่าธุรกรรมผ่านระบบประมาณ 9 ล้านบาทต่อปี)", bold_prefix="Serviceable Obtainable Market (SOM): ", space_after=1)
    add_body_p(doc, "ขนาดตลาดดังกล่าวแสดงให้เห็นถึงศักยภาพการเติบโตที่สูงมาก แม้เริ่มต้นจากโรงอาหารกลางเพียงแห่งเดียว แต่สามารถต่อยอดขยายผลไปยังโรงอาหารอื่นๆ ทั่วประเทศได้อย่างรวดเร็ว")

    # =========================================================================
    # =========================================================================
    # CHAPTER 6: BUSINESS MODEL CANVAS (เป๊ะ 3 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    add_chapter_title(doc, "6", "แบบจำลองผืนผ้าใบธุรกิจ (Business Model Canvas - BMC)\n(Business Model Canvas)")

    add_body_p(doc, "รูปที่ 6.1 แสดงแผนภาพสรุปแบบจำลองผืนผ้าใบธุรกิจ (Business Model Canvas) ทั้ง 9 องค์ประกอบ ซึ่งคณะผู้จัดทำได้วิเคราะห์และเชื่อมโยงคุณค่า เทคโนโลยี และการดำเนินงานเข้าด้วยกันอย่างเป็นรูปธรรม:", space_after=1)

    bmc_img = os.path.join(ASSETS_DIR, 'bmc_graphic.png')
    add_figure(doc, bmc_img, "6.1", "แบบจำลองผืนผ้าใบธุรกิจ 9 ช่อง (Business Model Canvas)", width_inches=2.3)

    add_heading_1(doc, "6.1  พันธมิตรหลัก (Key Partners)")
    add_numbered_item(doc, "1)", "ฝ่ายบริหารอาคารสถานที่ ศูนย์อาหาร มจพ. และสโมสรนักศึกษา", bold_prefix="มหาวิทยาลัย: ", space_after=1)
    add_numbered_item(doc, "2)", "ผู้ประกอบการร้านอาหารปรุงสดในโรงอาหารกลางและอาคาร 40 ปี", bold_prefix="ร้านค้า: ", space_after=1)
    add_numbered_item(doc, "3)", "LINE Thailand (LINE API) และธนาคารพาณิชย์ (PromptPay)", bold_prefix="พันธมิตรเทคโนโลยี: ", space_after=1)

    add_heading_1(doc, "6.2  กิจกรรมหลัก (Key Activities)")
    add_numbered_item(doc, "1)", "พัฒนาระบบ LINE LIFF ปรับปรุงอัลกอริทึมจัดคิว และหน้าจอร้านค้า (KDS)", bold_prefix="การพัฒนาระบบ: ", space_after=1)
    add_numbered_item(doc, "2)", "ประสานงานร้านค้า ติดตั้งแท็บเล็ต อบรมการใช้งาน และดูแลช่วงเร่งด่วน", bold_prefix="การปฏิบัติการหน้างาน: ", space_after=1)
    add_numbered_item(doc, "3)", "จัดกิจกรรมการตลาดและสื่อสารประชาสัมพันธ์ในหมู่นักศึกษาและบุคลากร", bold_prefix="การตลาดและการสื่อสาร: ", space_after=1)

    add_heading_1(doc, "6.3  ทรัพยากรหลัก (Key Resources)")
    add_numbered_item(doc, "1)", "ระบบคลาวด์ อัลกอริทึมจัดคิว และฐานข้อมูลความปลอดภัยสูง", bold_prefix="เทคโนโลยี: ", space_after=1)
    add_numbered_item(doc, "2)", "แท็บเล็ตประจำร้านค้า และป้าย QR Code บนโต๊ะอาหาร มจพ.", bold_prefix="อุปกรณ์กายภาพ: ", space_after=1)
    add_numbered_item(doc, "3)", "ทีมพัฒนาซอฟต์แวร์ และบุคลากร On-site Support ดูแลผู้ใช้งาน", bold_prefix="บุคลากร: ", space_after=1)

    add_heading_1(doc, "6.4  คุณค่าที่ส่งมอบ (Value Propositions)")
    add_body_p(doc, "สำหรับผู้บริโภค: ส่งมอบความสะดวก สั่งอาหารล่วงหน้า จ่ายไร้เงินสด รับอาหารพอดีเวลา ประหยัดเวลา 20-25 นาทีต่อมื้อ", space_after=1)
    add_body_p(doc, "สำหรับร้านค้า: เพิ่มยอดขายชั่วโมงเร่งด่วน ลดความผิดพลาดด้วยจอ KDS และคิดค่าบริการต่ำเป็นธรรม ไม่เป็นภาระต้นทุน", space_after=1)

    add_heading_1(doc, "6.5  ความสัมพันธ์กับลูกค้า (Customer Relationships)")
    add_numbered_item(doc, "1)", "สั่งอาหารและชำระเงินอัตโนมัติผ่าน LINE ตลอด 24 ชั่วโมง สะดวกสบาย", bold_prefix="บริการอัตโนมัติ: ", space_after=1)
    add_numbered_item(doc, "2)", "แจ้งเตือนสถานะอาหาร 3 ขั้นตอนตรงสู่แชท LINE ให้ผู้ใช้รับรู้ความคืบหน้า", bold_prefix="การแจ้งเตือนทันที: ", space_after=1)
    add_numbered_item(doc, "3)", "ทีมแอดมินพร้อมให้ความช่วยเหลือและรับฟังข้อเสนอแนะเพื่อพัฒนาต่อเนื่อง", bold_prefix="การดูแลผู้ใช้งาน: ", space_after=1)

    add_heading_1(doc, "6.6  ช่องทางการเข้าถึง (Channels)")
    add_numbered_item(doc, "1)", "LINE Official Account (LIFF) ใช้งานได้ทันทีไม่ต้องลงแอปเพิ่มเติม", bold_prefix="ช่องทางดิจิทัล: ", space_after=1)
    add_numbered_item(doc, "2)", "ป้าย Standee และสติกเกอร์ QR Code บนโต๊ะอาหารทุกโต๊ะในโรงอาหาร มจพ.", bold_prefix="ช่องทางกายภาพ: ", space_after=1)
    add_numbered_item(doc, "3)", "กลุ่มสังคมออนไลน์ เพจกิจกรรม มจพ. และการบอกต่อแบบปากต่อปาก", bold_prefix="สื่อประชาสัมพันธ์: ", space_after=1)

    add_heading_1(doc, "6.7  กลุ่มลูกค้าเป้าหมาย (Customer Segments)")
    add_numbered_item(doc, "1)", "นักศึกษา มจพ. ทุกชั้นปีที่มีเวลาพักจำกัดและชื่นชอบความสะดวกรวดเร็ว", bold_prefix="กลุ่มนักศึกษา: ", space_after=1)
    add_numbered_item(doc, "2)", "อาจารย์และเจ้าหน้าที่สายสนับสนุนที่ต้องการบริหารเวลาอย่างมีประสิทธิภาพ", bold_prefix="กลุ่มบุคลากร: ", space_after=1)
    add_numbered_item(doc, "3)", "ร้านอาหารปรุงสดในโรงอาหารที่ต้องการขยายยอดขายและยกระดับการจัดการครัว", bold_prefix="กลุ่มร้านค้า: ", space_after=1)

    add_heading_1(doc, "6.8  โครงสร้างต้นทุน (Cost Structure)")
    add_numbered_item(doc, "1)", "ค่าบริการ Cloud Server และ Managed PostgreSQL / Redis สำหรับระบบ", bold_prefix="ต้นทุนระบบคลาวด์: ", space_after=1)
    add_numbered_item(doc, "2)", "ค่าบริการ LINE Messaging API สำหรับส่ง Push Notification แจ้งสถานะ", bold_prefix="ต้นทุน API: ", space_after=1)
    add_numbered_item(doc, "3)", "ค่าจัดซื้อแท็บเล็ตประจำร้านค้า และค่าจัดทำสื่อประชาสัมพันธ์ ป้าย Standee", bold_prefix="ต้นทุนอุปกรณ์และการตลาด: ", space_after=1)

    add_heading_1(doc, "6.9  แหล่งที่มารายได้ (Revenue Streams)")
    add_numbered_item(doc, "1)", "ส่วนแบ่งค่าธรรมเนียมธุรกรรมจากร้านค้า (Micro-transaction Fee 3 - 5%)", bold_prefix="ค่าธรรมเนียมระบบ: ", space_after=1)
    add_numbered_item(doc, "2)", "ระบบสมาชิกรายงานวิเคราะห์ยอดขายและพฤติกรรมลูกค้า (199 บาท/เดือน)", bold_prefix="Merchant Analytics: ", space_after=1)
    add_numbered_item(doc, "3)", "พื้นที่แบนเนอร์โฆษณาและร้านค้าแนะนำบนหน้าแรกของแอปพลิเคชัน", bold_prefix="ค่าโฆษณาประชาสัมพันธ์: ", space_after=1)
    add_body_p(doc, "ความสอดประสานของทั้ง 9 องค์ประกอบใน Business Model Canvas ส่งผลให้โครงการมีรากฐานธุรกิจที่มั่นคงและพร้อมขยายผลเชิงพาณิชย์ได้อย่างแท้จริง", space_after=2)

    # =========================================================================
    # CHAPTER 7: MARKETING & SALES STRATEGY (เป๊ะ 2 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    add_chapter_title(doc, "7", "กลยุทธ์การตลาดและการขาย\n(Marketing & Sales Strategy)")

    add_heading_1(doc, "7.1  การวางตำแหน่งทางการตลาด (Market Positioning Map)")
    add_body_p(doc, "รูปที่ 7.1 แสดงตำแหน่งเชิงกลยุทธ์ของ Smart Queue Food บนแกนความสะดวกรวดเร็วและต้นทุนค่าบริการ:")

    pos_img = os.path.join(ASSETS_DIR, 'positioning_map.png')
    add_figure(doc, pos_img, "7.1", "แผนภาพการวางตำแหน่งผลิตภัณฑ์ในตลาด (Market Positioning Map)", width_inches=3.6)

    add_body_p(doc, "การวิเคราะห์ตำแหน่งเชิงเปรียบเทียบใน 4 มิติทางธุรกิจ:")
    add_numbered_item(doc, "1)", "ใช้เวลารอคอยสูง (20-30 นาที) เหมาะสำหรับช่วงเวลาปกติแต่ล้มเหลวในช่วงเร่งด่วน", bold_prefix="กลุ่มสั่งหน้าร้านเดิม: ", space_after=1)
    add_numbered_item(doc, "2)", "สะดวกรวดเร็วแต่คิดค่า GP สูง 30-35% และมีค่าส่ง ไม่เหมาะกับโรงอาหาร", bold_prefix="กลุ่มแอปเดลิเวอรี่ทั่วไป: ", space_after=1)
    add_numbered_item(doc, "3)", "ลดความผิดพลาดได้แต่ยังมีคิวอุดตันหน้าตู้ และมีต้นทุนค่าฮาร์ดแวร์สูง", bold_prefix="กลุ่มตู้คีออสก์อัตโนมัติ: ", space_after=1)
    add_numbered_item(doc, "4)", "ครองตำแหน่ง High Convenience & Low Cost สั่งผ่าน LINE ได้ทันที ไม่มีค่าส่ง คิดค่าบริการต่ำมาก", bold_prefix="Smart Queue Food: ", space_after=1)

    add_heading_1(doc, "7.2  กลยุทธ์ส่วนประสมทางการตลาด 4Ps สำหรับนวัตกรรมบริการ")
    add_numbered_item(doc, "1)", "ระบบสั่งอาหารล่วงหน้าผ่าน LINE LIFF ที่รวดเร็ว เสถียร ไม่เปลืองพื้นที่ความจำเครื่อง ออกแบบเฉพาะสำหรับโรงอาหารมหาวิทยาลัย", bold_prefix="Product (ผลิตภัณฑ์และบริการ): ", space_after=1)
    add_numbered_item(doc, "2)", "ผู้บริโภคจ่ายราคาปกติเท่าหน้าร้าน ไม่มีค่าธรรมเนียมแอบแฝง ร้านอาหารคิดค่า GP เพียง 3-5% (ถูกกว่าเดลิเวอรี่ทั่วไป 7-10 เท่า)", bold_prefix="Price (ราคา): ", space_after=1)
    add_numbered_item(doc, "3)", "ให้บริการ ณ โรงอาหารกลาง มจพ. และเข้าถึงผ่านสมาร์ตโฟนได้ทุกที่ทุกเวลาบน LINE Official Account", bold_prefix="Place (ช่องทาง): ", space_after=1)
    add_numbered_item(doc, "4)", "แคมเปญเปิดตัว 'มื้อแรก ลด 10 บาท' สำหรับนักศึกษาใหม่ และระบบสะสมแต้ม 'สั่งครบ 10 มื้อ ฟรี 1 เมนู' ร่วมกับร้านค้า", bold_prefix="Promotion (การส่งเสริมการขาย): ", space_after=1)

    add_heading_1(doc, "7.3  กลยุทธ์การเข้าสู่ตลาดและการส่งเสริมการขาย (Go-to-Market Strategy)")
    add_body_p(doc, "กลยุทธ์การเจาะตลาดระยะเริ่มต้นแบ่งออกเป็น 3 ขั้นตอนหลัก:")
    add_numbered_item(doc, "1)", "ร่วมมือกับองค์การบริหารนักศึกษา ติดตั้ง Standee และป้าย QR Code บนทุกโต๊ะในโรงอาหารกลางเพื่อสร้างการรับรู้ในวงกว้าง", bold_prefix="ระยะที่ 1 สร้างการรับรู้ (Awareness): ", space_after=1)
    add_numbered_item(doc, "2)", "จัดทีม On-ground Ambassador ประจำโรงอาหารให้คำแนะนำการใช้งานและแจกโค้ดส่วนลดมื้อแรกเพื่อกระตุ้นการสั่งจริง", bold_prefix="ระยะที่ 2 กระตุ้นการทดลองใช้ (Activation): ", space_after=1)
    add_numbered_item(doc, "3)", "ใช้ระบบคูปองสะสมแต้มดิจิทัลและกิจกรรมโปรโมชันช่วงสอบเพื่อสร้างความคุ้นชินและพฤติกรรมการสั่งซ้ำเป็นประจำ", bold_prefix="ระยะที่ 3 สร้างความภักดี (Retention): ", space_after=1)

    # =========================================================================
    # CHAPTER 8: TECHNOLOGY & INNOVATION STRATEGY (เป๊ะ 2 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    add_chapter_title(doc, "8", "กลยุทธ์ด้านเทคโนโลยีและนวัตกรรม (3 หมวด 10 ยุทธวิธี)\n(Technology & Innovation Strategy)")

    add_heading_1(doc, "8.1  การวิเคราะห์ตามโมเดล Ten Types of Innovation (Larry Keeley)")
    add_body_p(doc, "ตามกรอบทฤษฎี Ten Types of Innovation ของ Larry Keeley ที่ได้ศึกษาในบทเรียนที่ 5 คณะผู้จัดทำได้วิเคราะห์กลยุทธ์นวัตกรรมของ Smart Queue Food ครอบคลุม 3 หมวดหลัก ดังนี้:")
    add_heading_2(doc, "หมวดที่ 1: Configuration (การจัดโครงสร้างและเครือข่ายธุรกิจ)")
    add_numbered_item(doc, "1)", "คิดค่าบริการแบบ Micro-transaction Fee 3-5% ต่ำกว่าตลาดเดลิเวอรี่ และเปิดโมเดล Subscription สำหรับรายงานวิเคราะห์ข้อมูลร้านค้า", bold_prefix="Profit Model (โมเดลกำไร): ", space_after=1)
    add_numbered_item(doc, "2)", "ร่วมมือกับร้านค้าในโรงอาหาร มหาวิทยาลัย และธนาคาร เพื่อสร้างเครือข่ายนิเวศแบบไร้รอยต่อ", bold_prefix="Network (เครือข่ายพันธมิตร): ", space_after=1)
    add_numbered_item(doc, "3)", "บริหารจัดการด้วยทีมพัฒนา Agile DevSecOps ที่คล่องตัวสูง สามารถตอบสนองต่อปัญหาหน้างานได้ทันท่วงที", bold_prefix="Structure (โครงสร้างองค์กร): ", space_after=1)
    add_numbered_item(doc, "4)", "พัฒนาขั้นตอนการสั่งอาหารและการปรุงอาหารให้เป็นระบบคู่ขนาน (Parallel Processing) แทนที่การต่อแถวแบบอนุกรม (Serial)", bold_prefix="Process (กระบวนการดำเนินงาน): ", space_after=1)

    add_heading_2(doc, "หมวดที่ 2: Offering (สมรรถนะและระบบผลิตภัณฑ์)")
    add_numbered_item(doc, "5)", "อัลกอริทึมประเมินเวลาและจัดคิวไดนามิกที่มีความแม่นยำสูง คำนวณจากความเร็วในการปรุงจริงของแต่ละเมนู", bold_prefix="Product Performance (สมรรถนะผลิตภัณฑ์): ", space_after=1)
    add_numbered_item(doc, "6)", "ผสานระบบสั่งอาหาร คิว การจ่ายเงิน PromptPay และการแจ้งเตือนไว้ในจุดเดียวอย่างไร้รอยต่อ", bold_prefix="Product System (ระบบผลิตภัณฑ์): ", space_after=1)

    add_heading_2(doc, "หมวดที่ 3: Experience (การยกระดับประสบการณ์ลูกค้า)")
    add_numbered_item(doc, "7)", "ระบบแจ้งเตือนสถานะอาหารอัตโนมัติ 3 สเต็ป และการรับประกันความถูกต้องของคำสั่งซื้อ", bold_prefix="Service (การบริการเสริม): ", space_after=1)
    add_numbered_item(doc, "8)", "ทำงานบน LINE Official Account ที่ทุกคนคุ้นเคย ไม่ต้องดาวน์โหลดแอปใหม่", bold_prefix="Channel (ช่องทางการเข้าถึง): ", space_after=1)
    add_numbered_item(doc, "9)", "สร้างแบรนด์ที่สะท้อนถึงความทันสมัย สะดวก รวดเร็ว และเป็นมิตรต่อประชาคมชาว มจพ.", bold_prefix="Brand (การสร้างแบรนด์): ", space_after=1)
    add_numbered_item(doc, "10)", "สร้างประสบการณ์การรับประทานอาหารกลางวันที่ผ่อนคลายและไร้ความเครียดจากการยืนรอคิว", bold_prefix="Customer Engagement (การมีส่วนร่วม): ", space_after=1)

    add_heading_1(doc, "8.2  การคุ้มครองทรัพย์สินทางปัญญาและความได้เปรียบทางเทคโนโลยี")
    add_numbered_item(doc, "1)", "จดแจ้งลิขสิทธิ์ซอฟต์แวร์ประเภทวรรณกรรม (โปรแกรมคอมพิวเตอร์) สำหรับซอร์สโค้ดและส่วนต่อประสานผู้ใช้ (UI/UX) ต่อกรมทรัพย์สินทางปัญญา", bold_prefix="ลิขสิทธิ์ซอฟต์แวร์ (Copyright): ", space_after=1)
    add_numbered_item(doc, "2)", "เก็บรักษาอัลกอริทึมจัดสรรคิวไดนามิก (Dynamic Queue Algorithm) เป็นความลับทางการค้า (Trade Secret) ไม่เปิดเผยสู่สาธารณะ", bold_prefix="ความลับทางการค้า (Trade Secret): ", space_after=1)
    add_numbered_item(doc, "3)", "จดทะเบียนเครื่องหมายการค้า 'Smart Queue Food' และตราสัญลักษณ์เพื่อคุ้มครองแบรนด์ในเชิงพาณิชย์", bold_prefix="เครื่องหมายการค้า (Trademark): ", space_after=1)
    add_numbered_item(doc, "4)", "สร้างความได้เปรียบจาก Network Effects และฐานข้อมูลพฤติกรรมการบริโภคในโรงอาหาร ซึ่งสร้างกำแพงป้องกันคู่แข่งรายใหม่ (Moat)", bold_prefix="ความได้เปรียบเชิงโครงข่าย (Network Moat): ", space_after=1)

    # =========================================================================
    # =========================================================================
    # CHAPTER 9: RISK MANAGEMENT & MITIGATION (เป๊ะ 2 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    add_chapter_title(doc, "9", "การประเมินและการบริหารจัดการความเสี่ยง\n(Risk Management & Mitigation)")

    add_heading_1(doc, "9.1  การบ่งชี้ความเสี่ยง 6 ด้านตามบทเรียนที่ 11")
    add_body_p(doc, "ตามที่อาจารย์ผู้สอนได้บรรยายในบทเรียนที่ 11 เรื่องการบริหารความเสี่ยง คณะผู้จัดทำได้ระบุความเสี่ยงของโครงการครอบคลุม 6 มิติหลัก ได้แก่:")
    add_numbered_item(doc, "1)", "ร้านค้ายังไม่คุ้นเคยกับการใช้งานแท็บเล็ตและระบบดิจิทัล", bold_prefix="ด้านการดำเนินงาน (R1): ", space_after=1)
    add_numbered_item(doc, "2)", "สัญญาณอินเทอร์เน็ตในโรงอาหารขัดข้องช่วงเวลาเร่งด่วน", bold_prefix="ด้านเทคโนโลยี (R2): ", space_after=1)
    add_numbered_item(doc, "3)", "ปริมาณคำสั่งซื้อลดลงในช่วงปิดภาคการศึกษาของมหาวิทยาลัย", bold_prefix="ด้านตลาดและความผันผวน (R3): ", space_after=1)
    add_numbered_item(doc, "4)", "การทำโปรโมชันส่งเสริมการขายของแพลตฟอร์มภายนอก", bold_prefix="ด้านการแข่งขัน (R4): ", space_after=1)
    add_numbered_item(doc, "5)", "ข้อผิดพลาดของสลิปโอนเงินหรือระบบตัดจ่ายธุรกรรมขัดข้อง", bold_prefix="ด้านการเงินและความปลอดภัย (R5): ", space_after=1)
    add_numbered_item(doc, "6)", "การเปลี่ยนแปลงระเบียบจัดระเบียบพื้นที่โรงอาหาร มจพ.", bold_prefix="ด้านกลยุทธ์และนโยบาย (R6): ", space_after=1)

    add_heading_1(doc, "9.2  เมทริกซ์การประเมินระดับความเสี่ยง (Risk Assessment Matrix)")
    add_body_p(doc, "รูปที่ 9.1 แสดงเมทริกซ์ประเมินระดับความเสี่ยง (Likelihood x Impact) ของโครงงาน:", space_after=1)

    risk_img = os.path.join(ASSETS_DIR, 'risk_matrix.png')
    add_figure(doc, risk_img, "9.1", "เมทริกซ์การประเมินระดับความเสี่ยง (Risk Assessment Matrix)", width_inches=2.3)

    add_heading_1(doc, "9.3  ตารางประเมินความเสี่ยงและแผนบริหารความต่อเนื่องทางธุรกิจ")
    risk_headers = ["รหัส", "ความเสี่ยง", "โอกาส", "ผลกระทบ", "ระดับ", "มาตรการบรรเทาความเสี่ยง"]
    risk_data = [
        ["R1", "ร้านค้าใช้ระบบไม่คล่อง", "สูง", "ปานกลาง", "สูง (High)", "จัดทีม On-site Support อบรม และทำปุ่มกด KDS ขนาดใหญ่"],
        ["R2", "อินเทอร์เน็ตขัดข้อง", "ปานกลาง", "สูง", "สูง (High)", "ติดตั้ง 4G/5G Router สำรอง และระบบ Offline Mode"],
        ["R3", "ยอดสั่งซื้อลดลงช่วงปิดเทอม", "สูง", "ปานกลาง", "ปานกลาง (Med)", "จัดแคมเปญช่วง Summer และลดค่าใช้จ่ายคลาวด์"],
        ["R4", "การแข่งขันจากเดลิเวอรี่", "ต่ำ", "ปานกลาง", "ต่ำ (Low)", "เน้นจุดแข็งไม่มีค่า GP 35% ค่าอาหารราคาเท่าหน้าร้าน"],
        ["R5", "สลิปโอนเงินปลอม", "ปานกลาง", "สูง", "สูง (High)", "ใช้ระบบ Slip Verification ตรวจสอบกับธนาคารอัตโนมัติ"],
        ["R6", "การปรับระเบียบโรงอาหาร", "ต่ำ", "สูง", "ปานกลาง (Med)", "ทำบันทึกข้อตกลง (MOU) ร่วมกับฝ่ายบริหารอาคาร มจพ."]
    ]
    add_styled_table(doc, "9.1", "ตารางการประเมินความเสี่ยงและมาตรการบริหารจัดการความเสี่ยง", risk_headers, risk_data, [Inches(0.6), Inches(1.8), Inches(0.6), Inches(0.7), Inches(1.0), Inches(2.0)], font_size_pt=12.5, padding_twips=35)

    add_body_p(doc, "แผนบริหารความต่อเนื่องทางธุรกิจ (Business Continuity Plan - BCP):", space_after=1)
    add_numbered_item(doc, "1)", "ติดตั้งระบบ Multi-AZ Failover บนคลาวด์ สลับเซิร์ฟเวอร์สำรองอัตโนมัติใน 30 วินาที", bold_prefix="ด้านเซิร์ฟเวอร์: ", space_after=1)
    add_numbered_item(doc, "2)", "แท็บเล็ตร้านค้ารองรับ Dual-SIM 5G และทำงานใน Local Offline Mode ได้เมื่อเน็ตหลุด", bold_prefix="ด้านเครือข่าย: ", space_after=1)
    add_numbered_item(doc, "3)", "ตรวจสอบยอดเงินผ่าน Mobile Banking ร้านค้าได้ทันทีหากระบบ Slip API ล่าช้า", bold_prefix="ด้านธุรกรรม: ", space_after=1)
    add_numbered_item(doc, "4)", "สำรองฐานข้อมูลอัตโนมัติทุกวัน (Daily Automated Snapshot) ป้องกันข้อมูลสูญหาย", bold_prefix="ด้านความปลอดภัยข้อมูล: ", space_after=1)

    # =========================================================================
    # CHAPTER 10: SUMMARY, ROADMAP & FINANCIALS (เป๊ะ 2 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    add_chapter_title(doc, "10", "บทสรุป แผนการดำเนินงาน และความเป็นไปได้ทางการเงิน\n(Summary, Roadmap & Financial Feasibility)")

    add_heading_1(doc, "10.1  บทสรุปโครงการ (Executive Summary)")
    add_body_p(doc, "โครงงาน 'Smart Queue Food' ประสบความสำเร็จในการประยุกต์ใช้องค์ความรู้ด้านผู้ประกอบการนวัตกรรม เพื่อแก้ไขปัญหาความแออัดและการรอคอยคิวในโรงอาหาร มจพ. โดยบูรณาการ LINE LIFF, Predictive Queue Algorithm, Dynamic PromptPay และ Kitchen Display System เข้าด้วยกัน จนเกิดเป็นแบบจำลองธุรกิจที่มีคุณค่าสูง เข้าถึงง่าย และเป็นธรรมต่อผู้ประกอบการร้านอาหาร")

    add_heading_1(doc, "10.2  แผนงานและเส้นทางการดำเนินโครงการ (Project Roadmap)")
    add_body_p(doc, "ตารางที่ 10.1 แสดงแผนงานและเป้าหมายการดำเนินโครงการตลอดระยะเวลา 12 เดือน:")

    road_headers = ["ระยะเวลา", "กิจกรรมหลักที่ต้องดำเนินการ", "ผลลัพธ์ที่คาดหวัง"]
    road_data = [
        ["เดือนที่ 1 - 2\nระยะพัฒนา", "• พัฒนาระบบ LINE LIFF และหน้าจอ KDS\n• ทดสอบระบบร่วมกับร้านค้าตัวอย่างและทำป้าย QR", "ระบบพร้อมใช้งาน (MVP Ready) ผ่านการทดสอบเสถียรภาพ"],
        ["เดือนที่ 3 - 5\nระยะนำร่อง", "• เปิดทดลองในโรงอาหารกลาง มจพ. (15 ร้านค้า)\n• จัดแคมเปญกระตุ้นยอดสั่งซื้อและปรับจูนระบบคิว", "ผู้ใช้สะสม 3,000 คน ยอด 800 ออเดอร์/วัน เวลารอคอยลดลง > 65%"],
        ["เดือนที่ 6 - 8\nระยะขยายผล", "• ขยายบริการครบทุกร้านในโรงอาหารกลาง (30 ร้าน)\n• เปิดตัวระบบสมาชิก Merchant Analytics Subscription", "ผู้ใช้สะสม 8,000 คน โครงการก้าวสู่จุดคุ้มทุน (Break-Even)"],
        ["เดือนที่ 9 - 12\nระยะสมบูรณ์", "• เชื่อมต่อทุกโรงอาหารในวิทยาเขตกรุงเทพฯ\n• เตรียมแผนขยายสู่ มจพ. ปราจีนบุรี และระยอง", "คำสั่งซื้อเฉลี่ย 2,500 ออเดอร์/วัน สร้างรายได้หมุนเวียนยั่งยืน"]
    ]
    add_styled_table(doc, "10.1", "แผนงานและเส้นทางการดำเนินโครงการ Smart Queue Food", road_headers, road_data, [Inches(1.4), Inches(2.8), Inches(2.4)], font_size_pt=12.5, padding_twips=35)

    add_heading_1(doc, "10.3  การวิเคราะห์จุดคุ้มทุนและความเป็นไปได้ทางการเงิน")
    add_numbered_item(doc, "1)", "ค่าอาหารเฉลี่ย 50 บาท คิดค่าธรรมเนียม 4% (2 บาท/ออเดอร์) ระยะนำร่อง 15 ร้าน ยอดสั่ง 1,000 ออเดอร์/วัน รายได้ค่าธรรมเนียม 52,000 บาท/เดือน รวมค่าสมาชิก Analytics (15 ร้าน x 199 บาท = 2,985 บาท) และค่าโฆษณา รวมรายได้เฉลี่ยเดือนละ 60,000 บาท", bold_prefix="ประมาณการรายได้: ", space_after=1)
    add_numbered_item(doc, "2)", "ค่าบริการคลาวด์ 3,000 บาท/เดือน, ค่า LINE API 2,000 บาท/เดือน, ค่าบำรุงรักษาและการตลาด 10,000 บาท/เดือน รวมต้นทุนคงที่เดือนละ 15,000 บาท กำไรสุทธิจากการดำเนินงานประมาณ 45,000 บาทต่อเดือน", bold_prefix="ต้นทุนการดำเนินงาน: ", space_after=1)
    add_numbered_item(doc, "3)", "เงินลงทุนเริ่มต้นพัฒนาระบบ จัดหาแท็บเล็ต 15 เครื่อง และสื่อการตลาด รวม 120,000 บาท ด้วยกำไรดำเนินงานเดือนละ 45,000 บาท โครงการคืนทุน (Payback Period) ได้ภายในระยะเวลาประมาณ 7 เดือน", bold_prefix="การวิเคราะห์จุดคุ้มทุน (Break-Even): ", space_after=1)

    add_heading_1(doc, "10.4  ปัจจัยแห่งความสำเร็จ (Critical Success Factors)")
    add_numbered_item(doc, "1)", "ความร่วมมือและความไว้วางใจของผู้ประกอบการร้านอาหารในการปรับเปลี่ยนมาใช้ระบบดิจิทัล", space_after=1)
    add_numbered_item(doc, "2)", "ความเสถียรและความแม่นยำของระบบคิวในชั่วโมงเร่งด่วน", space_after=1)
    add_numbered_item(doc, "3)", "การสนับสนุนเชิงนโยบายจากฝ่ายบริหารอาคารสถานที่และศูนย์อาหาร มจพ.", space_after=1)
    add_numbered_item(doc, "4)", "การรักษามาตรฐานการบริการที่สะดวกรวดเร็วจนผู้ใช้งานเกิดความพึงพอใจและใช้งานต่อเนื่อง", space_after=1)

    add_heading_1(doc, "10.5  ข้อเสนอแนะและทิศทางการพัฒนาในอนาคต (Future Outlook)")
    add_numbered_item(doc, "1)", "การพัฒนาระบบ AI แนะนำเมนูอาหารเพื่อสุขภาพตามหลักโภชนาการและข้อมูลประวัติการบริโภคของผู้ใช้", bold_prefix="ระบบแนะนำอัจฉริยะ (AI Recommendation): ", space_after=1)
    add_numbered_item(doc, "2)", "การขยายผลสู่ทุกวิทยาเขตของมหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ (วิทยาเขตปราจีนบุรี และระยอง)", bold_prefix="การขยายผลสู่ทุกวิทยาเขต (Multi-Campus Expansion): ", space_after=1)
    add_body_p(doc, "การดำเนินงานตามแผนยุทธศาสตร์นี้จะยกระดับให้ Smart Queue Food ก้าวสู่การเป็นระบบนิเวศศูนย์อาหารอัจฉริยะต้นแบบของสถาบันอุดมศึกษาไทยอย่างยั่งยืน", space_after=2)

    # =========================================================================
    # REFERENCES (บรรณานุกรม - เป๊ะ 1 หน้าเต็ม สวยงามตามแบบ APA)
    # =========================================================================
    start_chapter_section(doc)
    p_ref_title = doc.add_paragraph()
    format_paragraph(p_ref_title, space_before=14, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_ref_title.paragraph_format.first_line_indent = Inches(0)
    r_ref = p_ref_title.add_run("บรรณานุกรม")
    set_run_font(r_ref, size_pt=18, bold=True)

    references = [
        "สุวรรธนา เทพจิต, วิศลย์ธีรา เมตตานนท์, ธิดาวัลย์ อ่ำแจ้ง, สิริพงศ์ จึงถาวรรณ, และ กิจติมา ลุมภักดี. (2567). เอกสารประกอบการสอนวิชา 080203914 ผู้ประกอบการนวัตกรรม (Innovative Technopreneurs). กรุงเทพมหานคร: มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ.",
        "Afuah, A. (2009). Strategic Innovation: New Game Strategies for Competitive Advantage. London: Routledge.",
        "Dorf, R. C., & Byers, T. H. (2011). Technology Ventures: From Idea to Enterprise (4th ed.). New York: McGraw-Hill.",
        "Keeley, L., Pikkel, R., Quinn, B., & Walters, H. (2013). Ten Types of Innovation: The Discipline of Building Breakthroughs. New Jersey: John Wiley & Sons.",
        "Osterwalder, A., & Pigneur, Y. (2010). Business Model Generation: A Handbook for Visionaries, Game Changers, and Challengers. New Jersey: John Wiley & Sons.",
        "Osterwalder, A., Pigneur, Y., Bernarda, G., & Smith, A. (2014). Value Proposition Design: How to Create Products and Services Customers Want. New Jersey: John Wiley & Sons.",
        "Ries, E. (2011). The Lean Startup: How Today's Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses. New York: Crown Business."
    ]

    for ref in references:
        add_reference_item(doc, ref)

    # =========================================================================
    # APPENDIX A (ภาคผนวก ก - เป๊ะ 1 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    p_appa_t1 = doc.add_paragraph()
    format_paragraph(p_appa_t1, space_before=14, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_appa_t1.paragraph_format.first_line_indent = Inches(0)
    r_a1 = p_appa_t1.add_run("ภาคผนวก ก")
    set_run_font(r_a1, size_pt=18, bold=True)

    p_appa_t2 = doc.add_paragraph()
    format_paragraph(p_appa_t2, space_before=0, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_appa_t2.paragraph_format.first_line_indent = Inches(0)
    r_a2 = p_appa_t2.add_run("ภาพถ่ายโปสเตอร์ Business Model Canvas ต้นฉบับ")
    set_run_font(r_a2, size_pt=16, bold=True)

    add_body_p(doc, "ภาพถ่ายชิ้นงานโปสเตอร์ Business Model Canvas ต้นฉบับที่คณะผู้จัดทำกลุ่ม “พี่หล่อไหมน้องงงง” ได้วิเคราะห์และนำเสนอในชั้นเรียนวิชาผู้ประกอบการนวัตกรรม (Innovative Technopreneurs) มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ:")

    orig_poster = os.path.join(ASSETS_DIR, 'bmc_poster_original.jpg')
    add_figure(doc, orig_poster, "ก.1", "ภาพถ่ายโปสเตอร์ Business Model Canvas ต้นฉบับโครงงาน Smart Queue Food", width_inches=3.6)

    add_body_p(doc, "โปสเตอร์ต้นฉบับนี้แสดงกระบวนการระดมสมอง การวิเคราะห์ปัญหา และการจัดวางโครงสร้างโมเดลธุรกิจของกลุ่ม ซึ่งนำมาสู่การพัฒนาระบบซอฟต์แวร์และรูปเล่มรายงานฉบับสมบูรณ์")

    # =========================================================================
    # APPENDIX B (ภาคผนวก ข - เป๊ะ 1 หน้าเต็ม)
    # =========================================================================
    start_chapter_section(doc)
    p_appb_t1 = doc.add_paragraph()
    format_paragraph(p_appb_t1, space_before=14, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_appb_t1.paragraph_format.first_line_indent = Inches(0)
    r_b1 = p_appb_t1.add_run("ภาคผนวก ข")
    set_run_font(r_b1, size_pt=18, bold=True)

    p_appb_t2 = doc.add_paragraph()
    format_paragraph(p_appb_t2, space_before=0, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
    p_appb_t2.paragraph_format.first_line_indent = Inches(0)
    r_b2 = p_appb_t2.add_run("สรุปผลการสำรวจความคิดเห็นกลุ่มตัวอย่างในโรงอาหาร มจพ.")
    set_run_font(r_b2, size_pt=16, bold=True)

    add_body_p(doc, "ตารางที่ ข.1 สรุปผลการสำรวจความคิดเห็นกลุ่มตัวอย่างนักศึกษาและบุคลากรใน มจพ. (N=120) และผู้ประกอบการร้านอาหารในโรงอาหารกลาง (N=10):")

    survey_headers = ["ประเด็นคำถามการสำรวจ", "กลุ่มตัวอย่างนักศึกษาและบุคลากร (N=120)", "กลุ่มผู้ประกอบการร้านอาหาร (N=10)"]
    survey_data = [
        ["ระยะเวลารอคอยเฉลี่ยช่วงเที่ยง", "- 10 ถึง 15 นาที (ร้อยละ 18)\n- 15 ถึง 25 นาที (ร้อยละ 54)\n- มากกว่า 25 นาที (ร้อยละ 28)", "- เวลาปรุงเฉลี่ย 1.5 - 2 นาทีต่อจาน\n- ออเดอร์สะสมช่วงเที่ยง 15 - 30 คิว"],
        ["ปัญหาที่พบบ่อยที่สุด", "- รอคิวนานจนเข้าเรียนสาย (ร้อยละ 68)\n- โต๊ะที่นั่งไม่เพียงพอ (ร้อยละ 62)\n- ออเดอร์ผิดพลาด/ได้ไม่ตรง (ร้อยละ 34)", "- ลูกค้ายืนมุงหน้าร้านจนสับสน (ร้อยละ 90)\n- จดออเดอร์ไม่ทัน / กระดาษหาย (ร้อยละ 60)\n- ทอนเงินผิด / สแกนช้า (ร้อยละ 50)"],
        ["ความต้องการใช้งานผ่าน LINE", "- สนใจใช้งานอย่างยิ่ง (ร้อยละ 88)\n- ต้องการระบบเตือนเมื่อเสร็จ (ร้อยละ 94)\n- ไม่ต้องการโหลดแอปใหม่ (ร้อยละ 82)", "- ยินดีเข้าร่วมหากระบบใช้งานง่าย (ร้อยละ 80)\n- รับได้กับค่าธรรมเนียม 3 - 5% (ร้อยละ 90)\n- ต้องการจอแสดงผลที่ชัดเจน (ร้อยละ 100)"]
    ]
    add_styled_table(doc, "ข.1", "สรุปผลการสำรวจความคิดเห็นและความพึงพอใจของกลุ่มตัวอย่างใน มจพ.", survey_headers, survey_data, [Inches(1.8), Inches(2.4), Inches(2.4)])

    add_body_p(doc, "ข้อมูลผลสำรวจข้างต้นถูกนำมาใช้เป็นฐานอ้างอิงเชิงประจักษ์ในการออกแบบฟังก์ชันระบบ Smart Queue Food เพื่อตอบสนองความต้องการของผู้ใช้งานและร้านค้าได้อย่างตรงจุด")

    doc.save(DOCX_OUTPUT)
    print("Report docx saved successfully.")
    return doc

def convert_docx_to_pdf(docx_path, pdf_path):
    print(f"Converting {docx_path} to PDF via Word COM...")
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    try:
        wdoc = word.Documents.Open(docx_path)
        wdoc.SaveAs(pdf_path, FileFormat=17)
        wdoc.Close()
    finally:
        word.Quit()
    print(f"Conversion complete: {pdf_path}")

def scan_page_map(pdf_path):
    doc = fitz.open(pdf_path)
    
    # Robust search for start of Chapter 1 body:
    ch1_pno = None
    for pno, page in enumerate(doc):
        text = page.get_text().replace('\u200b', '')
        if "ในสถาบันอุดมศึกษาขนาดใหญ่" in text and "บทที่ 1" in text:
            ch1_pno = pno
            break
    
    if ch1_pno is None:
        ch1_pno = 7 # fallback

    print(f"Detected Chapter 1 Body at PDF Page {ch1_pno + 1}")

    headings = [
        ("ch1", r"บทที่\s*1\b"),
        ("ch1_2", r"1\.2\s+"),
        ("ch1_5", r"1\.5\s+"),
        ("ch2", r"บทที่\s*2\b"),
        ("ch2_4", r"2\.4\s+"),
        ("ch3", r"บทที่\s*3\b"),
        ("ch3_3", r"3\.3\s+"),
        ("ch4", r"บทที่\s*4\b"),
        ("ch4_2", r"4\.2\s+"),
        ("ch4_3", r"4\.3\s+"),
        ("ch5", r"บทที่\s*5\b"),
        ("ch5_3", r"5\.3\s+"),
        ("ch6", r"บทที่\s*6\b"),
        ("ch6_3", r"6\.3\s+"),
        ("ch6_7", r"6\.7\s+"),
        ("ch7", r"บทที่\s*7\b"),
        ("ch7_2", r"7\.2\s+"),
        ("ch8", r"บทที่\s*8\b"),
        ("ch8_2", r"หมวดที่\s*3|8\.2\s+"),
        ("ch9", r"บทที่\s*9\b"),
        ("ch9_3", r"9\.3\s+|ตารางที่\s*9\.1"),
        ("ch10", r"บทที่\s*10\b"),
        ("ch10_3", r"10\.3\s+"),
        ("ch10_4", r"10\.4\s+"),
        ("ref", r"บรรณานุกรม"),
        ("app_a", r"ภาคผนวก\s*ก"),
        ("app_b", r"ภาคผนวก\s*ข"),
        ("tbl_2_1", r"ตารางที่\s*2\.1"),
        ("tbl_3_1", r"ตารางที่\s*3\.1"),
        ("tbl_5_1", r"ตารางที่\s*5\.1"),
        ("tbl_9_1", r"ตารางที่\s*9\.1"),
        ("tbl_10_1", r"ตารางที่\s*10\.1"),
        ("tbl_b_1", r"ตารางที่\s*ข\.1"),
        ("fig_4_1", r"รูปที่\s*4\.1"),
        ("fig_4_2", r"รูปที่\s*4\.2"),
        ("fig_6_1", r"รูปที่\s*6\.1"),
        ("fig_7_1", r"รูปที่\s*7\.1"),
        ("fig_9_1", r"รูปที่\s*9\.1"),
        ("fig_a_1", r"รูปที่\s*ก\.1"),
    ]

    p_map = DEFAULT_PAGE_MAP.copy()
    for key, pattern in headings:
        for pno in range(ch1_pno, len(doc)):
            text = doc[pno].get_text().replace('\u200b', '')
            if re.search(pattern, text):
                arabic_page = str(pno - ch1_pno + 1)
                p_map[key] = arabic_page
                break
    doc.close()
    return p_map

def mirror_files():
    dest_dirs = [
        r'C:\Project\innovative-technopreneurs\00_ไฟล์ส่งงาน_Smart_Queue_Food',
        r'C:\Project\innovative-technopreneurs\Lectures\Project\00_ไฟล์ส่งงาน_Smart_Queue_Food'
    ]
    for d in dest_dirs:
        os.makedirs(d, exist_ok=True)
        docx_dest = os.path.join(d, '01_เล่มรายงาน_Smart_Queue_Food_ฉบับสมบูรณ์.docx')
        pdf_dest = os.path.join(d, '01_เล่มรายงาน_Smart_Queue_Food_ฉบับสมบูรณ์.pdf')
        shutil.copy2(DOCX_OUTPUT, docx_dest)
        shutil.copy2(PDF_OUTPUT, pdf_dest)
        print(f"Copied to: {d}")

def generate_perfect_report():
    print("=========================================================")
    print("STEP 1: Generating Initial Build with Estimated TOC Pages")
    print("=========================================================")
    build_doc()
    convert_docx_to_pdf(DOCX_OUTPUT, PDF_OUTPUT)
    
    print("\n=========================================================")
    print("STEP 2: Scanning Exact Page Numbers from Compiled PDF")
    print("=========================================================")
    exact_map = scan_page_map(PDF_OUTPUT)
    print("Exact scanned page map:")
    for k, v in sorted(exact_map.items()):
        print(f"  {k:10s}: {v}")
        
    print("\n=========================================================")
    print("STEP 3: Rebuilding DOCX with 100% Exact TOC Page Numbers")
    print("=========================================================")
    build_doc(exact_map)
    convert_docx_to_pdf(DOCX_OUTPUT, PDF_OUTPUT)
    
    print("\n=========================================================")
    print("STEP 4: Mirroring Output Files to Submission Folders")
    print("=========================================================")
    mirror_files()
    print("\nSUCCESS: Perfect academic report compiled and mirrored successfully!")

if __name__ == '__main__':
    generate_perfect_report()
