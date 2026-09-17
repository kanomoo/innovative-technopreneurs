import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r'C:\Project\innovative-technopreneurs\Project_Smart_Queue_Food'
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
PPTX_OUTPUT = os.path.join(BASE_DIR, 'สไลด์นำเสนอ_Smart_Queue_Food_Pitching.pptx')
PDF_OUTPUT = os.path.join(BASE_DIR, 'สไลด์นำเสนอ_Smart_Queue_Food_Pitching.pdf')

FONT_HEADING = 'Leelawadee UI'
FONT_BODY = 'Leelawadee UI'

# Minimal Academic Palette (Clean, High-End Executive)
CLR_BLACK = RGBColor(15, 23, 42)        # #0F172A Dark Navy / Black
CLR_TITLE = RGBColor(30, 41, 59)        # #1E293B
CLR_BODY = RGBColor(51, 65, 85)         # #334155
CLR_MUTED = RGBColor(100, 116, 139)     # #64748B
CLR_BORDER = RGBColor(203, 213, 225)    # #CBD5E1
CLR_BG_CARD = RGBColor(255, 255, 255)   # #FFFFFF
CLR_HEADER_BG = RGBColor(248, 250, 252) # #F8FAFC
CLR_ACCENT = RGBColor(30, 58, 138)      # #1E3A8A Dark Navy

def add_header(slide, title_text, chapter_label="โครงงานธุรกิจนวัตกรรม | มจพ."):
    # Header container
    header_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.85)
    )
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = CLR_HEADER_BG
    header_box.line.color.rgb = CLR_BORDER
    header_box.line.width = Pt(1)

    tf = header_box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.08)
    tf.margin_bottom = Inches(0.08)

    p_badge = tf.paragraphs[0]
    p_badge.text = chapter_label.upper()
    p_badge.font.name = FONT_HEADING
    p_badge.font.size = Pt(10)
    p_badge.font.bold = True
    p_badge.font.color.rgb = CLR_MUTED

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = CLR_BLACK

def add_footer(slide, slide_num, total_slides=15):
    # Footer line
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.015)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = CLR_BORDER
    line.line.fill.background()

    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.03), Inches(11.733), Inches(0.35))
    tf = tx_box.text_frame
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    
    p = tf.paragraphs[0]
    p.text = "วิชา 080203914 ผู้ประกอบการนวัตกรรม (Innovative Technopreneurs) | มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = CLR_MUTED

    p_num = tf.add_paragraph()
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"{slide_num} / {total_slides}"
    p_num.font.name = FONT_BODY
    p_num.font.size = Pt(9.5)
    p_num.font.bold = True
    p_num.font.color.rgb = CLR_BLACK

def add_academic_card(slide, left, top, width, height, title, items):
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CLR_BG_CARD
    card.line.color.rgb = CLR_BORDER
    card.line.width = Pt(1)

    # Card title strip
    title_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.6))
    title_bar.fill.solid()
    title_bar.fill.fore_color.rgb = CLR_HEADER_BG
    title_bar.line.color.rgb = CLR_BORDER
    title_bar.line.width = Pt(1)
    
    p_t = title_bar.text_frame.paragraphs[0]
    p_t.alignment = PP_ALIGN.LEFT
    title_bar.text_frame.margin_left = Inches(0.2)
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(14.5)
    p_t.font.bold = True
    p_t.font.color.rgb = CLR_BLACK

    # Content
    content_box = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.65), width - Inches(0.3), height - Inches(0.75))
    tf = content_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.05)

    for i, itm in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(4)
        if isinstance(itm, tuple):
            prefix, text = itm
            r1 = p.add_run()
            r1.text = prefix
            r1.font.name = FONT_BODY
            r1.font.bold = True
            r1.font.size = Pt(12)
            r1.font.color.rgb = CLR_BLACK

            r2 = p.add_run()
            r2.text = text
            r2.font.name = FONT_BODY
            r2.font.size = Pt(12)
            r2.font.color.rgb = CLR_BODY
        else:
            p.text = itm
            p.font.name = FONT_BODY
            p.font.size = Pt(12)
            p.font.color.rgb = CLR_BODY

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(255, 255, 255)
    bg1.line.fill.background()

    # Outer academic frame
    frame = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    frame.fill.solid()
    frame.fill.fore_color.rgb = CLR_HEADER_BG
    frame.line.color.rgb = CLR_BORDER
    frame.line.width = Pt(1.5)

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(3.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p0 = tf1.paragraphs[0]
    p0.text = "รายงานนำเสนอโครงงานธุรกิจนวัตกรรม (PITCH DECK)"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = CLR_MUTED

    p_main = tf1.add_paragraph()
    p_main.space_before = Pt(8)
    p_main.text = "Smart Queue Food"
    p_main.font.name = FONT_HEADING
    p_main.font.size = Pt(36)
    p_main.font.bold = True
    p_main.font.color.rgb = CLR_BLACK

    p_sub = tf1.add_paragraph()
    p_sub.space_before = Pt(4)
    p_sub.text = "ระบบสั่งอาหารและจัดการคิวอัจฉริยะในโรงอาหารมหาวิทยาลัยผ่าน LINE Official Account"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(17)
    p_sub.font.color.rgb = CLR_BODY

    # Team & Course details on cover
    tb_meta = s1.shapes.add_textbox(Inches(1.2), Inches(3.8), Inches(11.0), Inches(2.6))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True

    p_m1 = tf_m.paragraphs[0]
    p_m1.text = "วิชา: 080203914 ผู้ประกอบการนวัตกรรม (Innovative Technopreneurs) ภาคเรียนที่ 1 ปีการศึกษา 2569"
    p_m1.font.name = FONT_BODY
    p_m1.font.size = Pt(13.5)
    p_m1.font.bold = True
    p_m1.font.color.rgb = CLR_BLACK

    p_m2 = tf_m.add_paragraph()
    p_m2.space_before = Pt(4)
    p_m2.text = "คณะผู้จัดทำ: กลุ่ม “พี่หล่อไหมน้องงงง” (กลุ่มที่ 1) คณะเทคโนโลยีและการจัดการอุตสาหกรรม มจพ."
    p_m2.font.name = FONT_BODY
    p_m2.font.size = Pt(13)
    p_m2.font.color.rgb = CLR_BODY

    p_m3 = tf_m.add_paragraph()
    p_m3.space_before = Pt(2)
    p_m3.text = "สมาชิก: นายจิณณะ, นายปภาวิณ, นายดนุสรณ์, นายนัทธพงศ์, นายภัทรพล, น.ส.กนกวรรณ, น.ส.ณัฐธิดา, นายปรัชญา"
    p_m3.font.name = FONT_BODY
    p_m3.font.size = Pt(11.5)
    p_m3.font.color.rgb = CLR_MUTED

    p_m4 = tf_m.add_paragraph()
    p_m4.space_before = Pt(4)
    p_m4.text = "เสนอ: อาจารย์ผู้สอนประจำวิชา | เวลาการนำเสนอ: 10 นาที (ถาม-ตอบ 5 นาที)"
    p_m4.font.name = FONT_BODY
    p_m4.font.size = Pt(12)
    p_m4.font.bold = True
    p_m4.font.color.rgb = CLR_BLACK

    s1.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (0:00 - 1:00 นาที):\n"
        "กราบเรียนอาจารย์ผู้สอนและสวัสดีเพื่อนๆ ทุกคนครับ กลุ่ม “พี่หล่อไหมน้องงงง” ขอเสนอโครงการธุรกิจนวัตกรรม "
        "“Smart Queue Food: ระบบสั่งอาหารและจัดการคิวอัจฉริยะในโรงอาหารมหาวิทยาลัยผ่าน LINE Official Account” "
        "ซึ่งได้รับการพัฒนาขึ้นเพื่อแก้ไขปัญหาความแออัดและการรอคอยคิวนานในโรงอาหาร มจพ. ครับ"
    )

    # =========================================================================
    # SLIDE 2: THE PROBLEM
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. ปัญหาและความจำเป็นในการพัฒนา (Problem Statement)")
    add_footer(s2, 2)

    add_academic_card(s2, Inches(0.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "ระยะเวลารอคอยเฉลี่ย 20-30 นาที", [
                          ("• สภาพปัญหาช่วงเที่ยง: ", "11:30 - 13:00 น. มีนักศึกษาและบุคลากรมากกว่า 5,000 คนเข้าโรงอาหารพร้อมกัน"),
                          ("• การสูญเสียเวลาเรียน: ", "หมดเวลาพักไปกับการยืนรอคิวกลางอากาศร้อน ต้องรีบกินเพื่อเข้าเรียนคาบบ่าย"),
                          ("• ความล่าช้าในการเรียน: ", "ส่งผลให้นักศึกษาเข้าเรียนสาย และอาจารย์เริ่มสอนล่าช้า")
                      ])

    add_academic_card(s2, Inches(4.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "ความแออัดในพื้นที่กายภาพ", [
                          ("• แถวคิวยาวกีดขวาง: ", "คิวยาวล้นออกมาขวางทางเดินและโต๊ะอาหาร เกิดความแออัด"),
                          ("• โต๊ะที่นั่งไม่เพียงพอ: ", "เกิดปัญหาการแย่งชิงที่นั่งและไม่มีที่นั่งรับประทานอาหาร"),
                          ("• ปัญหาด้านสุขอนามัย: ", "ความหนาแน่นสะสมความร้อน อากาศไม่ถ่ายเท และไม่ถูกสุขอนามัย")
                      ])

    add_academic_card(s2, Inches(8.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "ความผิดพลาดในการจัดการครัว", [
                          ("• การจดกระดาษผิดพลาด: ", "คำสั่งซื้อตกหล่น ลำดับคิวสับสน ทำอาหารผิดเงื่อนไข"),
                          ("• คอขวดการชำระเงิน: ", "แม่ค้าต้องสลับมือมาตรวจสลิปโอนเงินหน้าร้าน ทำให้คิวสะดุด"),
                          ("• สูญเสียโอกาสการขาย: ", "ลูกค้าเห็นคิวยาวจึงเปลี่ยนใจไม่ซื้อ ร้านค้าเสียรายได้ 25-30%")
                      ])

    s2.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (1:00 - 2:00 นาที):\n"
        "ทุกท่านคงทราบดีว่าทุกเที่ยงในโรงอาหาร มจพ. จะเกิดปัญหาคิวยาวมาก นักศึกษาต้องรออาหารเฉลี่ย 20 ถึง 30 นาที "
        "พื้นที่โรงอาหารแออัด โต๊ะนั่งไม่พอ และฝั่งแม่ค้าเองก็จดออเดอร์ไม่ทัน ทำอาหารสลับคิว "
        "นี่คือปัญหาที่เกิดขึ้นซ้ำๆ ทุกวันและจำเป็นต้องได้รับการแก้ไขด้วยนวัตกรรมครับ"
    )

    # =========================================================================
    # SLIDE 3: THE SOLUTION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. แนวคิดนวัตกรรม Smart Queue Food (The Innovation Solution)")
    add_footer(s3, 3)

    add_academic_card(s3, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.4),
                      "หลักการทำงานของระบบ", [
                          ("• ทำงานบน LINE Official (LIFF): ", "เข้าถึงได้ทันทีโดยไม่ต้องดาวน์โหลดหรือติดตั้งแอปพลิเคชันเพิ่มเติม"),
                          ("• ระบบสั่งอาหารล่วงหน้า (Pre-order): ", "เลือกสั่งเมนูอาหารได้ตั้งแต่ก่อนเลิกเรียน พร้อมระบุเวลารับ"),
                          ("• อัลกอริทึมคำนวณคิว (Predictive ETA): ", "ประเมินเวลารอคอยแบบเรียลไทม์จากจำนวนคิวและความเร็วการปรุง"),
                          ("• ชำระเงินไร้เงินสด (PromptPay QR): ", "สร้าง QR Code ตรวจสอบยอดเงินและยืนยันสลิปอัตโนมัติ"),
                          ("• การแจ้งเตือนอัตโนมัติ: ", "ระบบส่งข้อความแจ้งเตือนผ่าน LINE เมื่ออาหารปรุงเสร็จพร้อมรับ")
                      ])

    add_academic_card(s3, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4),
                      "ผลลัพธ์และคุณค่าที่เกิดขึ้นจริง", [
                          ("1. ลดระยะเวลารอคอยลง 70%: ", "จากเดิม 20-30 นาที เหลือเพียง 0-3 นาที เดินมาถึงรับอาหารได้ทันที"),
                          ("2. คืนเวลาคุณภาพให้นักศึกษา: ", "มีเวลารับประทานอาหารอย่างผ่อนคลาย ไม่ต้องเร่งรีบ ไม่เข้าเรียนสาย"),
                          ("3. ครัวร้านค้าทำงานเป็นระบบ: ", "มีหน้าจอ KDS แสดงลำดับคิวชัดเจน ขจัดปัญหาออเดอร์ตกหล่น"),
                          ("4. เพิ่มยอดขายให้ร้านค้า 25%: ", "รองรับออเดอร์ล่วงหน้าได้มากขึ้นในชั่วโมงเร่งด่วน"),
                          ("5. สนับสนุนนโยบาย Smart Campus: ", "ลดความแออัดในโรงอาหารและส่งเสริมสังคมไร้เงินสดใน มจพ.")
                      ])

    s3.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (2:00 - 3:00 นาที):\n"
        "คำตอบของเราคือ Smart Queue Food ซึ่งเป็นระบบสั่งอาหารและจัดการคิวบน LINE Official Account "
        "ที่ทุกคนมีอยู่ในสมาร์ตโฟนอยู่แล้ว นักศึกษาสามารถสั่งอาหารล่วงหน้า จ่ายเงิน PromptPay "
        "และรอรับการแจ้งเตือนเมื่ออาหารเสร็จ ลดระยะเวลาการรอคอยลงได้ถึง 70% ครับ"
    )

    # =========================================================================
    # SLIDE 4: HOW IT WORKS (4 STEPS)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. ขั้นตอนการใช้งานระบบ 4 ขั้นตอน (Workflow & How It Works)")
    add_footer(s4, 4)

    step_data = [
        ("ขั้นตอนที่ 1\nเปิด LINE & สั่งเมนู", "สแกน QR หรือเข้า LINE OA เลือกดูร้านอาหาร ตรวจสอบคิวคงค้าง และสั่งอาหารพร้อมปรับแต่งตัวเลือกตามต้องการ"),
        ("ขั้นตอนที่ 2\nชำระเงิน PromptPay QR", "ระบบสร้าง Dynamic QR Code พร้อมยอดเงินตรงตามบิล สแกนชำระเงินผ่าน Mobile Banking และตรวจสอบสลิปอัตโนมัติใน 3 วินาที"),
        ("ขั้นตอนที่ 3\nรับบัตรคิว & รอแจ้งเตือน", "ได้รับหมายเลขคิวและแถบสถานะการปรุง สามารถนั่งอ่านหนังสือหรือเดินมาโรงอาหารอย่างสบายใจ"),
        ("ขั้นตอนที่ 4\nรับอาหารทันใจ ไร้คิว", "เมื่ออาหารปรุงเสร็จ LINE แจ้งเตือน ผู้ใช้เดินมารับอาหารที่จุดรับหน้าร้านได้ทันทีโดยไม่ต้องยืนรอคิว")
    ]

    for i, (stitle, sdesc) in enumerate(step_data):
        left_pos = Inches(0.8 + i * 2.95)
        card_s = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, Inches(1.6), Inches(2.8), Inches(5.1))
        card_s.fill.solid()
        card_s.fill.fore_color.rgb = CLR_BG_CARD
        card_s.line.color.rgb = CLR_BORDER
        card_s.line.width = Pt(1)

        # Header block
        h_block = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, Inches(1.6), Inches(2.8), Inches(1.0))
        h_block.fill.solid()
        h_block.fill.fore_color.rgb = CLR_HEADER_BG
        h_block.line.color.rgb = CLR_BORDER
        h_block.line.width = Pt(1)
        
        p_h = h_block.text_frame.paragraphs[0]
        p_h.alignment = PP_ALIGN.CENTER
        p_h.text = stitle
        p_h.font.name = FONT_HEADING
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = CLR_BLACK

        # Desc
        tx_d = s4.shapes.add_textbox(left_pos + Inches(0.15), Inches(2.7), Inches(2.5), Inches(3.8))
        p_d = tx_d.text_frame.paragraphs[0]
        tx_d.text_frame.word_wrap = True
        p_d.text = sdesc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = CLR_BODY

    s4.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (3:00 - 4:00 นาที):\n"
        "กระบวนการทำงานมี 4 ขั้นตอนสั้นๆ: สั่งเมนูผ่าน LINE, สแกนจ่ายเงิน PromptPay, รับบัตรคิวดูเวลานับถอยหลัง, "
        "และเดินไปรับอาหารทันทีเมื่อได้รับการแจ้งเตือน ใช้เวลาสั่งเพียง 1 นาทีครับ"
    )

    # =========================================================================
    # SLIDE 5: UI MOCKUP
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. ส่วนต่อประสานผู้ใช้งานจริง (UI/UX Prototype Screens)")
    add_footer(s5, 5)

    ui_path = os.path.join(ASSETS_DIR, 'ui_mockup.png')
    if os.path.exists(ui_path):
        s5.shapes.add_picture(ui_path, Inches(0.8), Inches(1.35), width=Inches(11.733))

    s5.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (4:00 - 4:45 นาที):\n"
        "นี่คือหน้าจอ UI Prototype ที่ออกแบบขึ้น หน้าจอ 1 คือการเลือกร้านและเมนู, หน้าจอ 2 คือการชำระเงิน PromptPay QR, "
        "หน้าจอ 3 คือบัตรคิวดิจิทัล และหน้าจอ 4 สำคัญมากครับ คือหน้าจอ Kitchen Display System สำหรับแม่ค้า "
        "ซึ่งมีปุ่มกดขนาดใหญ่ ใช้งานง่าย ไม่ซับซ้อนครับ"
    )

    # =========================================================================
    # SLIDE 6: SYSTEM ARCHITECTURE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. สถาปัตยกรรมระบบและโครงสร้างเทคโนโลยี (System Architecture)")
    add_footer(s6, 6)

    arch_path = os.path.join(ASSETS_DIR, 'system_architecture.png')
    if os.path.exists(arch_path):
        s6.shapes.add_picture(arch_path, Inches(0.8), Inches(1.35), width=Inches(11.733))

    s6.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (4:45 - 5:30 นาที):\n"
        "สถาปัตยกรรมระบบเป็นแบบ Microservices 4 ชั้น ชั้นหน้าบ้านทำงานบน LINE LIFF ผ่าน LINE Login "
        "ชั้นตรรกะมี Smart Queue Engine และระบบตรวจสลิป และชั้นข้อมูลใช้ Redis In-memory Cache "
        "เพื่อความรวดเร็วในการประมวลผลคิวในระดับมิลลิวินาทีครับ"
    )

    # =========================================================================
    # SLIDE 7: CUSTOMER SEGMENTS & PERSONAS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. กลุ่มลูกค้าเป้าหมายและการวิเคราะห์เพอร์โซนา (Customer Personas)")
    add_footer(s7, 7)

    add_academic_card(s7, Inches(0.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "Persona 1: นักศึกษา", [
                          ("• นายกิตติศักดิ์ (นัท) 20 ปี: ", "นักศึกษาคณะวิศวกรรมศาสตร์ ชั้นปีที่ 2"),
                          ("• พฤติกรรม: ", "มีเรียนแล็บช่วงเช้า เลิก 11:50 น. มีเวลาพักน้อย"),
                          ("• ปัญหา: ", "รอคิวนานจนไม่มีเวลากินข้าว เข้าเรียนสาย"),
                          ("• ประโยชน์: ", "สั่งล่วงหน้า เดินมาถึงได้กินทันที ประหยัดเวลา")
                      ])

    add_academic_card(s7, Inches(4.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "Persona 2: อาจารย์/บุคลากร", [
                          ("• ผศ.ดร.พรรณนิภา (อ.ปุ๊ก) 38 ปี: ", "อาจารย์คณะวิทยาศาสตร์ประยุกต์"),
                          ("• พฤติกรรม: ", "มีประชุมและเตรียมสอน มักซื้ออาหารไปทานที่ห้องพัก"),
                          ("• ปัญหา: ", "ไม่ชอบยืนเบียดในโรงอาหารที่เสียงดังและร้อน"),
                          ("• ประโยชน์: ", "สั่งจากห้องพักครู แจ้งเตือนค่อยลงไปรับ")
                      ])

    add_academic_card(s7, Inches(8.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "Persona 3: ร้านอาหาร", [
                          ("• ป้าสมศรี ทวีโชค 54 ปี: ", "เจ้าของร้านอาหารตามสั่ง โรงอาหารกลาง มจพ."),
                          ("• พฤติกรรม: ", "ปรุงอาหารเร็ว แต่ไม่ถนัดสมาร์ตโฟนซับซ้อน"),
                          ("• ปัญหา: ", "จดออเดอร์ไม่ทัน ทอนเงินผิด ลูกค้ามุงหน้าร้าน"),
                          ("• ประโยชน์: ", "จอ KDS ใช้งานง่าย ครัวเป็นระบบ ยอดขายเพิ่มขึ้น")
                      ])

    s7.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (5:30 - 6:15 นาที):\n"
        "กลุ่มเป้าหมายของเราเป็นแบบ Two-Sided Market คือฝั่งผู้บริโภค ได้แก่ นักศึกษาและอาจารย์ "
        "และฝั่งผู้ประกอบการ คือร้านค้าในโรงอาหาร ซึ่งทั้งสองฝ่ายได้รับประโยชน์ร่วมกันอย่างชัดเจนครับ"
    )

    # =========================================================================
    # SLIDE 8: THE BUSINESS MODEL CANVAS (9 BLOCKS)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. แบบจำลองผืนผ้าใบธุรกิจ (Business Model Canvas - BMC 9 ช่อง)")
    add_footer(s8, 8)

    bmc_path = os.path.join(ASSETS_DIR, 'bmc_graphic.png')
    if os.path.exists(bmc_path):
        s8.shapes.add_picture(bmc_path, Inches(0.8), Inches(1.35), width=Inches(11.733))

    s8.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (6:15 - 7:15 นาที):\n"
        "นี่คือหัวใจสำคัญของโครงการ คือ Business Model Canvas ทั้ง 9 ช่อง ที่พัฒนาต่อยอดมาจากภาพสเก็ตช์โปสเตอร์ "
        "โครงสร้างรายได้ของเรายุติธรรมมาก คิดค่า GP เพียง 3-5% ร่วมกับค่าสมาชิกรายงานสถิติ "
        "และคุณค่าหลักคือการประหยัดเวลาและลดความแออัดในโรงอาหารครับ"
    )

    # =========================================================================
    # SLIDE 9: VALUE PROPOSITION & POSITIONING MAP
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "8. การวางตำแหน่งทางการตลาด (Market Positioning Map)")
    add_footer(s9, 9)

    pos_path = os.path.join(ASSETS_DIR, 'positioning_map.png')
    if os.path.exists(pos_path):
        s9.shapes.add_picture(pos_path, Inches(0.8), Inches(1.35), width=Inches(7.0))

    add_academic_card(s9, Inches(8.1), Inches(1.4), Inches(4.4), Inches(5.4),
                      "ความได้เปรียบทางการแข่งขัน", [
                          ("1. ตำแหน่ง Sweet Spot: ", "Smart Queue Food อยู่ในตำแหน่งความสะดวกสูงสุดและราคาประหยัดสูงสุด"),
                          ("2. เทียบกับร้านค้าเดิม: ", "ราคาเท่ากัน แต่ลดระยะเวลาการรอคอยลงได้มากกว่า 70%"),
                          ("3. เทียบกับ Food Delivery: ", "แอปเดลิเวอรี่คิด GP 30-35% และมีค่าส่งแพง ไม่เหมาะกับนักศึกษา"),
                          ("4. เทียบกับตู้ Kiosk: ", "ตู้สั่งอาหารมีต้นทุนฮาร์ดแวร์สูง และผู้ใช้ยังต้องยืนต่อคิวหน้าตู้อยู่ดี")
                      ])

    s9.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (7:15 - 8:00 นาที):\n"
        "จากแผนภาพ Positioning Map ระบบของเราอยู่ในจุดที่มีคุณค่าสูงสุด คือสะดวกมากเพราะเข้าผ่าน LINE ได้ทันที "
        "และราคาประหยัดเพราะไม่มีการบวกราคาอาหารเพิ่มเหมือนแอปเดลิเวอรี่ทั่วไปครับ"
    )

    # =========================================================================
    # SLIDE 10: 4Ps MARKETING MIX
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "9. กลยุทธ์ส่วนประสมทางการตลาด 4Ps (Marketing Mix Strategy)")
    add_footer(s10, 10)

    p_boxes = [
        ("Product (ผลิตภัณฑ์และบริการ)", [
            ("• ระบบบน LINE LIFF: ", "เร็ว เสถียร ไม่เปลืองหน่วยความจำเครื่อง"),
            ("• ฟังก์ชันหลัก: ", "สั่งล่วงหน้า จัดคิวไดนามิก จ่ายเงิน PromptPay"),
            ("• ออกแบบเฉพาะ: ", "หน้าจอ KDS ใช้งานง่ายสำหรับร้านอาหาร")
        ]),
        ("Price (ราคา)", [
            ("• ผู้บริโภค: ", "จ่ายราคาปกติเท่าหน้าร้าน ไม่มีค่าธรรมเนียม"),
            ("• ร้านอาหาร: ", "คิดค่า GP เพียง 3-5% (ถูกกว่าแอปทั่วไป 7-10 เท่า)"),
            ("• ระบบรายงานสถิติ: ", "ค่าบริการสมาชิก 199 บาท/เดือน")
        ]),
        ("Place (ช่องทางจัดจำหน่าย)", [
            ("• พื้นที่บริการ: ", "โรงอาหารกลาง และโรงอาหารทุกจุดใน มจพ."),
            ("• ช่องทางดิจิทัล: ", "LINE Official Account เข้าถึงได้ 24 ชั่วโมง"),
            ("• จุดสัมผัสจริง: ", "ป้ายสแกน QR Code ทุกโต๊ะอาหารในโรงอาหาร")
        ]),
        ("Promotion (การส่งเสริมการตลาด)", [
            ("• แคมเปญเปิดตัว: ", "แคมเปญ 'มื้อแรก ลด 10 บาท' สำหรับนักศึกษา"),
            ("• การสร้างความภักดี: ", "ระบบสะสมแต้ม 10 มื้อ แลกรับฟรี 1 มื้อ"),
            ("• การสื่อสาร: ", "ร่วมมือกับเพจสโมสรนักศึกษา และชุมชน มจพ.")
        ])
    ]

    for i, (ptitle, pitems) in enumerate(p_boxes):
        left_pos = Inches(0.8 + (i % 2) * 5.95)
        top_pos = Inches(1.4 + (i // 2) * 2.7)
        add_academic_card(s10, left_pos, top_pos, Inches(5.75), Inches(2.55), ptitle, pitems)

    s10.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (8:00 - 8:40 นาที):\n"
        "กลยุทธ์ 4Ps ของเราเน้นการเข้าถึงง่าย ราคาเป็นมิตรต่อนักศึกษาและร้านค้า "
        "โดยมีโปรโมชันแนะนำการใช้งานและระบบสะสมแต้มเพื่อกระตุ้นให้เกิดการใช้งานประจำครับ"
    )

    # =========================================================================
    # SLIDE 11: INNOVATION STRATEGY (10 TACTICS)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10. กลยุทธ์นวัตกรรม 3 หมวด 10 ยุทธวิธี (Doblin's Ten Types)")
    add_footer(s11, 11)

    add_academic_card(s11, Inches(0.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "1. หมวดการกำหนดค่า (Configuration)", [
                          ("• Profit Model: ", "เปลี่ยนจากการขายขาดซอฟต์แวร์ มาเป็น Micro-transaction fee ร้อยละ 3-5 ร่วมกับค่าบริการ Subscription"),
                          ("• Network: ", "เชื่อมโยงความร่วมมือกับ LINE Thailand, ธนาคาร PromptPay และฝ่ายบริหารอาคาร มจพ.")
                      ])

    add_academic_card(s11, Inches(4.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "2. หมวดการนำเสนอ (Offering)", [
                          ("• Product Performance: ", "อัลกอริทึมจัดการคิวแบบคาดการณ์เวลาล่วงหน้า (Predictive ETA) แม่นยำระดับนาที"),
                          ("• Product System: ", "การผสาน LIFF Web App, Merchant KDS และ Dynamic PromptPay เข้าเป็นระบบเดียวแบบไร้รอยต่อ")
                      ])

    add_academic_card(s11, Inches(8.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "3. หมวดประสบการณ์ (Experience)", [
                          ("• Service: ", "ยกระดับบริการโรงอาหารให้มีระบบแจ้งเตือนส่วนบุคคล ไม่ต้องยืนรอเฝ้าหน้าร้าน"),
                          ("• Channel: ", "ให้บริการผ่าน LINE Official ซึ่งทุกคนเปิดใช้งานเป็นประจำ"),
                          ("• Customer Engagement: ", "ระบบสะสมแต้ม การรีวิวร้านค้า และการจัดอันดับเมนูยอดนิยม")
                      ])

    s11.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (8:40 - 9:15 นาที):\n"
        "จากการเรียนในบทที่ 5 เรื่อง Ten Types of Innovation เราเลือกใช้ยุทธวิธีที่สอดคล้องกับเรามากที่สุด "
        "ได้แก่ โมเดลกำไรแบบ Micro-fee, การเชื่อมโยง Network ของ LINE และ PromptPay, "
        "การสร้าง Product System ที่สมบูรณ์ และการยกระดับ Service Experience ของผู้ใช้ครับ"
    )

    # =========================================================================
    # SLIDE 12: RISK MANAGEMENT
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "11. การบริหารจัดการความเสี่ยง 6 มิติ (Risk Management)")
    add_footer(s12, 12)

    risk_path = os.path.join(ASSETS_DIR, 'risk_matrix.png')
    if os.path.exists(risk_path):
        s12.shapes.add_picture(risk_path, Inches(0.8), Inches(1.35), width=Inches(7.0))

    add_academic_card(s12, Inches(8.1), Inches(1.4), Inches(4.4), Inches(5.4),
                      "มาตรการบริหารจัดการความเสี่ยง", [
                          ("• R1 ร้านค้าไม่ชินเทคโนโลยี: ", "ออกแบบ Simple UI ปุ่มใหญ่ มีทีม Support ช่วยประกบ 7 วันแรก"),
                          ("• R2 ระบบเครือข่ายขัดข้อง: ", "มีโหมด Offline สั่งงานผ่าน Local Wi-Fi ได้ต่อเนื่อง ไม่สะดุด"),
                          ("• R3 ยอดขายตกช่วงปิดเทอม: ", "จัดแคมเปญรองรับภาคฤดูร้อน และขยายสู่ร้านค้ารอบรั้ว มจพ."),
                          ("• R4 การแข่งขันจากแอปภายนอก: ", "รักษาจุดแข็งค่า GP ต่ำ 3-5% ไม่มีค่าส่ง อาหารราคาเท่าหน้าร้าน"),
                          ("• R5 การชำระเงินผิดพลาด: ", "ใช้ Dynamic QR Code เช็คยอดและเลขอ้างอิงอัตโนมัติ 100%")
                      ])

    s12.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (9:15 - 9:45 นาที):\n"
        "ตามที่อาจารย์สอนในบทที่ 11 เรื่องความเสี่ยง เหมือนกรณีตัวอย่างร้านกาแฟที่ยอดขายตก "
        "เราได้วิเคราะห์ความเสี่ยง 6 มิติ พร้อมวางมาตรการรับมือเชิงรุก เช่น หากร้านค้าไม่คุ้นเคย เรามีทีมช่วยสอน "
        "และหากอินเทอร์เน็ตล่ม เรามีระบบ Offline Fallback รองรับครับ"
    )

    # =========================================================================
    # SLIDE 13: FINANCIALS & BREAK-EVEN
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "12. ประมาณการทางการเงินและจุดคุ้มทุน (Financial Feasibility)")
    add_footer(s13, 13)

    add_academic_card(s13, Inches(0.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "โครงสร้างรายได้ (Revenue)", [
                          ("• ค่าคอมมิชชันคำสั่งซื้อ: ", "ร้อยละ 4 จากยอดขาย (ประมาณ 2.00 บาทต่อออเดอร์)"),
                          ("• ยอดสั่งซื้อเป้าหมาย: ", "1,000 ออเดอร์/วัน (15 ร้านค้า) = 52,000 บาท/เดือน"),
                          ("• ค่าสมาชิก Merchant Analytics: ", "15 ร้านค้า x 199 บาท = 2,985 บาท/เดือน"),
                          ("• ค่าโฆษณาและสื่อโปรโมต: ", "5,000 บาท/เดือน"),
                          ("• รวมรายได้เฉลี่ย: ", "ประมาณ 60,000 บาท/เดือน")
                      ])

    add_academic_card(s13, Inches(4.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "ต้นทุนดำเนินงาน (OPEX)", [
                          ("• ค่าบริการคลาวด์เซิร์ฟเวอร์: ", "3,000 บาท/เดือน"),
                          ("• ค่าบริการ LINE Messaging API: ", "2,000 บาท/เดือน"),
                          ("• ค่าบำรุงรักษาและการตลาด: ", "10,000 บาท/เดือน"),
                          ("• รวมต้นทุนดำเนินงานคงที่: ", "15,000 บาท/เดือน"),
                          ("• กำไรจากการดำเนินงานสุทธิ: ", "ประมาณ 45,000 บาท/เดือน")
                      ])

    add_academic_card(s13, Inches(8.8), Inches(1.4), Inches(3.7), Inches(5.4),
                      "การวิเคราะห์จุดคุ้มทุน (Break-Even)", [
                          ("• เงินลงทุนเริ่มต้น (CAPEX): ", "120,000 บาท (พัฒนาระบบ + แท็บเล็ต 15 เครื่อง + สื่อการตลาด)"),
                          ("• ระยะเวลาคืนทุน (Payback): ", "ประมาณ 6 ถึง 7 เดือน หลังเปิดให้บริการเต็มรูปแบบ"),
                          ("• ศักยภาพการเติบโต: ", "เมื่อขยายสู่ 30 ร้านค้า กำไรสุทธิจะเพิ่มขึ้นเป็น 90,000+ บาท/เดือน")
                      ])

    s13.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (9:45 - 10:15 นาที):\n"
        "ในด้านตัวเลขทางการเงิน ด้วยยอดคำสั่งซื้อ 1,000 ออเดอร์ต่อวัน เราจะมีรายได้ประมาณ 60,000 บาทต่อเดือน "
        "หักต้นทุนคงที่ 15,000 บาท เหลือกำไรสุทธิ 45,000 บาทต่อเดือน "
        "สามารถคืนทุนเงินลงทุนเริ่มต้น 120,000 บาท ได้ภายในเวลาเพียง 7 เดือนครับ"
    )

    # =========================================================================
    # SLIDE 14: ROADMAP
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "13. แผนงานการดำเนินงานและการขยายผล (Implementation Roadmap)")
    add_footer(s14, 14)

    phases = [
        ("ระยะที่ 1: นำร่อง (เดือน 1 - 5)", "• พัฒนาระบบ MVP บน LINE LIFF\n• นำร่อง 15 ร้านค้าในโรงอาหารกลาง มจพ.\n• ผู้ใช้งานสะสม 3,000 คน\n• ยอด 800 ออเดอร์/วัน"),
        ("ระยะที่ 2: ขยายผล (เดือน 6 - 12)", "• ขยายครบทุกร้านในโรงอาหารกลาง (30 ร้าน)\n• ขยายสู่โรงอาหารอาคาร 40 ปี\n• ก้าวสู่จุดคุ้มทุน (Break-Even)\n• ผู้ใช้งานสะสม 10,000 คน"),
        ("ระยะที่ 3: เติบโต (ปีที่ 2 - 3)", "• เชื่อมต่อ มจพ. ปราจีนบุรี และระยอง\n• ขยายสู่มหาวิทยาลัยพันธมิตร 3-5 แห่ง\n• ร้านค้าในระบบ > 120 ร้านค้า\n• ยอด 8,000 ออเดอร์/วัน")
    ]

    for i, (ptitle, pdesc) in enumerate(phases):
        left_pos = Inches(0.8 + i * 3.95)
        add_academic_card(s14, left_pos, Inches(1.6), Inches(3.8), Inches(5.1), ptitle, [pdesc])

    s14.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอ (10:15 - 10:45 นาที):\n"
        "แผนงานของเราจะเริ่มจากการนำร่อง 15 ร้านค้าในโรงอาหารกลาง มจพ. ก่อนขยายให้ครบทุกโรงอาหาร "
        "และเป้าหมายระยะยาวคือการขยายสู่เครือข่ายมหาวิทยาลัยพันธมิตรทั่วประเทศครับ"
    )

    # =========================================================================
    # SLIDE 15: CONCLUSION & Q&A
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    bg15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg15.fill.solid()
    bg15.fill.fore_color.rgb = CLR_HEADER_BG
    bg15.line.fill.background()

    frame15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    frame15.fill.solid()
    frame15.fill.fore_color.rgb = RGBColor(255, 255, 255)
    frame15.line.color.rgb = CLR_BORDER
    frame15.line.width = Pt(1.5)

    tb15 = s15.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.5), Inches(3.8))
    tf15 = tb15.text_frame
    tf15.word_wrap = True

    p0 = tf15.paragraphs[0]
    p0.text = "SMART QUEUE FOOD | นวัตกรรมเพื่อโรงอาหารมหาวิทยาลัย"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = CLR_MUTED

    p1 = tf15.add_paragraph()
    p1.space_before = Pt(8)
    p1.text = "เปลี่ยนเวลาต่อคิว ให้เป็นเวลาคุณภาพ"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(34)
    p1.font.bold = True
    p1.font.color.rgb = CLR_BLACK

    p2 = tf15.add_paragraph()
    p2.space_before = Pt(12)
    p2.text = "ขอขอบพระคุณอาจารย์ผู้สอนและผู้รับฟังทุกท่าน\nยินดีรับฟังข้อเสนอแนะและพร้อมตอบข้อซักถาม (Q&A Session)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(17)
    p2.font.color.rgb = CLR_BODY

    s15.notes_slide.notes_text_frame.text = (
        "สคริปต์นำเสนอสรุป (10:45 - 11:00 นาที):\n"
        "Smart Queue Food จะช่วยคืนเวลาคุณภาพให้กับทุกคนใน มจพ. "
        "กลุ่ม “พี่หล่อไหมน้องงงง” ขอขอบพระคุณอาจารย์เป็นอย่างยิ่ง และพร้อมรับฟังข้อเสนอแนะและตอบคำถามครับ ขอบคุณครับ"
    )

    prs.save(PPTX_OUTPUT)
    print("Academic presentation saved successfully at:", PPTX_OUTPUT)

if __name__ == '__main__':
    build_deck()
