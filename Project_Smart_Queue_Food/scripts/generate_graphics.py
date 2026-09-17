import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = r'C:\Project\innovative-technopreneurs\Project_Smart_Queue_Food\assets'
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'Leelawadee UI'
plt.rcParams['axes.unicode_minus'] = False

# Academic Palette: Black, Charcoal, Slate, Minimal Navy
CLR_DARK = '#0F172A'
CLR_BODY = '#1E293B'
CLR_MUTED = '#475569'
CLR_BORDER = '#94A3B8'
CLR_BG = '#FFFFFF'
CLR_ACCENT = '#1E3A8A'

# ==========================================
# 1. ACADEMIC POSITIONING MAP
# ==========================================
def create_positioning_map():
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
    fig.patch.set_facecolor(CLR_BG)
    ax.set_facecolor(CLR_BG)

    # Clean axes
    ax.axhline(0, color=CLR_BORDER, linewidth=1.2, linestyle='-')
    ax.axvline(0, color=CLR_BORDER, linewidth=1.2, linestyle='-')

    # Subtle zone box for target
    rect = patches.Rectangle((0, 0), 5, 5, color='#F1F5F9', alpha=0.5, zorder=0)
    ax.add_patch(rect)

    points = [
        ("Smart Queue Food\n(ระบบนวัตกรรมที่พัฒนาขึ้น)", 3.8, 3.8, CLR_DARK, 220),
        ("การสั่งซื้อหน้าร้านแบบเดิม\n(Conventional Walk-in)", -3.5, 2.0, CLR_MUTED, 140),
        ("แพลตฟอร์มเดลิเวอรี่ทั่วไป\n(Food Delivery Apps: GP 30-35%)", 2.2, -3.2, CLR_MUTED, 140),
        ("ตู้สั่งอาหารอัตโนมัติหน้าร้าน\n(Self-Service Kiosk)", -2.2, -2.2, CLR_MUTED, 140),
    ]

    for name, x, y, color, size in points:
        if "Smart Queue Food" in name:
            ax.scatter(x, y, s=size, color=CLR_ACCENT, edgecolors=CLR_DARK, linewidth=2, zorder=5)
            bbox_props = dict(boxstyle="square,pad=0.4", fc="#FFFFFF", ec=CLR_ACCENT, lw=1.5)
            ax.annotate(name, (x, y), xytext=(x, y+0.5), ha='center', va='bottom',
                        fontsize=11, fontweight='bold', color=CLR_ACCENT, bbox=bbox_props, zorder=6)
        else:
            ax.scatter(x, y, s=size, color='#FFFFFF', edgecolors=CLR_MUTED, linewidth=1.5, zorder=5)
            bbox_props = dict(boxstyle="square,pad=0.3", fc="#FFFFFF", ec=CLR_BORDER, lw=1)
            y_offset = 0.4 if y > 0 else -0.5
            va_align = 'bottom' if y > 0 else 'top'
            ax.annotate(name, (x, y), xytext=(x, y+y_offset), ha='center', va=va_align,
                        fontsize=9.5, color=CLR_BODY, bbox=bbox_props, zorder=6)

    # Quadrant text
    ax.text(4.7, 4.7, '[โซนความคุ้มค่าและความสะดวกสูงสุด]', ha='right', va='top', fontsize=9.5, color=CLR_ACCENT, fontweight='bold')
    ax.text(-4.7, 4.7, '[โซนดั้งเดิม: รอคิวนาน เสียเวลา]', ha='left', va='top', fontsize=9.5, color=CLR_MUTED)
    ax.text(4.7, -4.7, '[โซนเดลิเวอรี่: ค่าส่งและ GP สูง]', ha='right', va='bottom', fontsize=9.5, color=CLR_MUTED)
    ax.text(-4.7, -4.7, '[โซนคีออสก์: ต้นทุนฮาร์ดแวร์สูง]', ha='left', va='bottom', fontsize=9.5, color=CLR_MUTED)

    ax.set_xlabel('ระดับความสะดวกและการเข้าถึงง่าย (เข้าถึงผ่าน LINE โดยไม่ต้องติดตั้งแอปพลิเคชัน) -->', fontsize=11, color=CLR_DARK, labelpad=8)
    ax.set_ylabel('ระดับความคุ้มค่าด้านราคาและความเหมาะสมกับโรงอาหารมหาวิทยาลัย -->', fontsize=11, color=CLR_DARK, labelpad=8)
    ax.set_title('แผนภาพการวางตำแหน่งผลิตภัณฑ์ในตลาด (Market Positioning Map)', fontsize=13, fontweight='bold', color=CLR_DARK, pad=12)

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(CLR_BORDER)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'positioning_map.png')
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print('Saved academic positioning_map.png')

# ==========================================
# 2. ACADEMIC SYSTEM ARCHITECTURE
# ==========================================
def create_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    fig.patch.set_facecolor(CLR_BG)
    ax.set_facecolor(CLR_BG)

    layers = [
        ("ระดับที่ 1: ส่วนต่อประสานผู้ใช้งาน (Presentation Layer)", [
            ("ผู้บริโภค (นักศึกษา / บุคลากร)", "LINE Official Account (LIFF Application)\n- สั่งอาหารล่วงหน้า\n- ตรวจสอบสถานะคิว\n- รับการแจ้งเตือนอัตโนมัติ"),
            ("ผู้ประกอบการ (ร้านอาหาร)", "Kitchen Display System (KDS Web App)\n- รับคำสั่งซื้อตามลำดับคิว\n- อัปเดตสถานะการปรุงอาหาร\n- จัดการเมนูและสต็อกวัตถุดิบ")
        ], 5.5),
        ("ระดับที่ 2: ระบบความปลอดภัยและการเชื่อมต่อ (Gateway & Security Layer)", [
            ("HTTPS / LINE Login Authentication", "ยืนยันตัวตนผู้ใช้งานผ่าน LINE UID ปลอดภัยตามมาตรฐานสากล"),
            ("API Rate Limiting & Load Balancer", "บริหารจัดการทราฟฟิกและป้องกันการส่งคำสั่งซื้อซ้ำซ้อนช่วงเร่งด่วน")
        ], 3.7),
        ("ระดับที่ 3: ตรรกะการประมวลผลทางธุรกิจ (Application & Business Logic)", [
            ("Smart Queue Engine", "อัลกอริทึมจัดสรรคิวและประเมินเวลารอคอยแบบไดนามิก"),
            ("Payment Verification Gateway", "สร้าง Dynamic QR PromptPay และตรวจสอบสลิปอัตโนมัติ"),
            ("Notification Dispatcher", "ระบบส่งข้อความแจ้งเตือนเรียลไทม์ผ่าน LINE Messaging API")
        ], 1.8),
        ("ระดับที่ 4: โครงสร้างข้อมูลและคลาวด์ (Data & Cloud Infrastructure)", [
            ("In-Memory Cache (Redis)", "ประมวลผลสถานะคิวคำสั่งซื้อแบบเรียลไทม์ความเร็วสูง"),
            ("Relational Database (PostgreSQL)", "จัดเก็บข้อมูลผู้ใช้ ร้านค้า เมนูอาหาร และประวัติการทำธุรกรรม")
        ], 0.0)
    ]

    for title, boxes, y_pos in layers:
        ax.text(0.5, y_pos + 1.0, title, fontsize=11, fontweight='bold', color=CLR_DARK)
        n_boxes = len(boxes)
        width = (10.0 - (n_boxes - 1) * 0.4) / n_boxes
        for i, (b_title, b_desc) in enumerate(boxes):
            x = 0.5 + i * (width + 0.4)
            rect = patches.Rectangle((x, y_pos), width, 0.85, facecolor='#FFFFFF', edgecolor=CLR_BORDER, linewidth=1.2, zorder=2)
            ax.add_patch(rect)
            
            # Header strip
            header_rect = patches.Rectangle((x, y_pos + 0.58), width, 0.27, facecolor='#F1F5F9', edgecolor=CLR_BORDER, linewidth=1.0, zorder=3)
            ax.add_patch(header_rect)
            ax.text(x + width/2, y_pos + 0.71, b_title, fontsize=10, fontweight='bold', color=CLR_DARK, ha='center', va='center', zorder=4)
            ax.text(x + width/2, y_pos + 0.27, b_desc, fontsize=8.5, color=CLR_BODY, ha='center', va='center', zorder=4)

    # Downward connectors
    arrow_props = dict(arrowstyle="->,head_width=0.3,head_length=0.4", color=CLR_BORDER, lw=1.5)
    ax.annotate('', xy=(5.5, 4.6), xytext=(5.5, 5.45), arrowprops=arrow_props)
    ax.annotate('', xy=(5.5, 2.7), xytext=(5.5, 3.65), arrowprops=arrow_props)
    ax.annotate('', xy=(5.5, 0.9), xytext=(5.5, 1.75), arrowprops=arrow_props)

    ax.set_xlim(0, 11)
    ax.set_ylim(-0.4, 7.0)
    ax.axis('off')
    ax.set_title('แผนภาพสถาปัตยกรรมระบบ Smart Queue Food (System Architecture)', fontsize=13, fontweight='bold', color=CLR_DARK, pad=10)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'system_architecture.png')
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print('Saved academic system_architecture.png')

# ==========================================
# 3. ACADEMIC UI MOCKUPS
# ==========================================
def create_ui_mockup():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    fig.patch.set_facecolor(CLR_BG)
    ax.set_facecolor(CLR_BG)

    screens = [
        ("หน้าจอ 1: เลือกเมนูและร้านค้า", [
            ("ร้านอาหารตามสั่งป้าสมศรี", "สถานะ: รอประมาณ 2 คิว (~4 นาที)"),
            ("รายการอาหาร", "1. ข้าวกะเพราหมูกรอบ (50 บาท)\n2. ข้าวหมูกระเทียม (45 บาท)\n3. ข้าวผัดต้มยำทะเล (60 บาท)"),
            ("ตัวเลือกเพิ่มเติม", "[/] เพิ่มไข่ดาว (+10 บาท)\n[/] ระดับความเผ็ด: ปานกลาง\n[ ] ไม่ใส่ผัก")
        ]),
        ("หน้าจอ 2: สรุปคำสั่งซื้อและชำระเงิน", [
            ("สรุปรายการคำสั่งซื้อ", "ข้าวกะเพราหมูกรอบ (+ไข่ดาว)\nยอดรวมสุทธิ: 60.00 บาท"),
            ("ระบบชำระเงิน PromptPay QR", "[ Dynamic PromptPay QR Code ]\nเลขอ้างอิง: SQF-2026-0901\nยอดเงินถูกต้องตามบิล ไม่ต้องระบุเอง"),
            ("สถานะการชำระเงิน", "ตรวจสอบการชำระเงินสำเร็จ (Verified)")
        ]),
        ("หน้าจอ 3: บัตรคิวและติดตามสถานะ", [
            ("หมายเลขคิวของคุณ", "คิวหมายเลข: #A-028\nเวลาสั่ง: 11:45 น. | เวลารับ: 12:00 น."),
            ("ขั้นตอนการดำเนินงาน", "[V] รับคำสั่งซื้อเรียบร้อย\n[>] กำลังปรุงอาหาร (กำลังดำเนินการ)\n[ ] อาหารปรุงเสร็จ พร้อมรับ"),
            ("การแจ้งเตือนผ่าน LINE", "ระบบจะส่งข้อความแจ้งเตือนเมื่ออาหารเสร็จ\nสามารถเดินมารับที่หน้าร้านได้ทันที")
        ]),
        ("หน้าจอ 4: ระบบจัดการครัว (KDS)", [
            ("รายการคิวหน้าร้านค้า", "คิวรอปรุง: 3 รายการ | เสิร์ฟแล้ว: 84 จาน"),
            ("คำสั่งซื้อปัจจุบัน (#A-028)", "- ข้าวกะเพราหมูกรอบ (+ไข่ดาว)\n[ ปุ่มกด: เริ่มปรุง ]  [ ปุ่มกด: เสร็จสิ้น ]"),
            ("การจัดการหน้าร้าน", "- ระบบหยุดรับคิวชั่วคราว\n- ปิดรับเมนูที่วัตถุดิบหมด")
        ])
    ]

    for i, (title, sections) in enumerate(screens):
        x = 0.5 + i * 3.1
        y = 0.4
        w = 2.8
        h = 6.8

        # Phone frame
        phone_body = patches.Rectangle((x, y), w, h, facecolor='#FFFFFF', edgecolor=CLR_DARK, linewidth=2, zorder=2)
        ax.add_patch(phone_body)

        # Header bar
        header_bar = patches.Rectangle((x, y + h - 0.7), w, 0.7, facecolor='#F8FAFC', edgecolor=CLR_BORDER, linewidth=1, zorder=3)
        ax.add_patch(header_bar)
        ax.text(x + w/2, y + h - 0.35, title.split(':')[0], fontsize=10, fontweight='bold', color=CLR_DARK, ha='center', va='center', zorder=4)

        # Title caption below
        ax.text(x + w/2, y - 0.25, title, fontsize=10, fontweight='bold', color=CLR_DARK, ha='center', va='top')

        curr_y = y + h - 0.9
        for sec_title, sec_desc in sections:
            card_h = 1.7
            box = patches.Rectangle((x + 0.15, curr_y - card_h), w - 0.3, card_h, facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1, zorder=3)
            ax.add_patch(box)
            # Section header
            s_head = patches.Rectangle((x + 0.15, curr_y - 0.35), w - 0.3, 0.35, facecolor='#F1F5F9', edgecolor='#CBD5E1', linewidth=1, zorder=3)
            ax.add_patch(s_head)
            ax.text(x + 0.25, curr_y - 0.18, sec_title, fontsize=9, fontweight='bold', color=CLR_DARK, va='center', zorder=4)
            ax.text(x + 0.25, curr_y - 0.5, sec_desc, fontsize=8, color=CLR_BODY, va='top', zorder=4)
            curr_y -= (card_h + 0.2)

    ax.set_xlim(0, 13)
    ax.set_ylim(-0.6, 7.8)
    ax.axis('off')
    ax.set_title('ภาพจำลองส่วนต่อประสานผู้ใช้งานระบบ Smart Queue Food (UI Prototype)', fontsize=13, fontweight='bold', color=CLR_DARK, pad=10)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ui_mockup.png')
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print('Saved academic ui_mockup.png')

# ==========================================
# 4. ACADEMIC RISK MATRIX
# ==========================================
def create_risk_matrix():
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
    fig.patch.set_facecolor(CLR_BG)
    ax.set_facecolor(CLR_BG)

    # 5x5 subtle grayscale/slate matrix
    matrix_shades = [
        ['#E2E8F0', '#CBD5E1', '#94A3B8', '#64748B', '#475569'],
        ['#F1F5F9', '#E2E8F0', '#CBD5E1', '#94A3B8', '#64748B'],
        ['#F8FAFC', '#F1F5F9', '#E2E8F0', '#CBD5E1', '#94A3B8'],
        ['#FFFFFF', '#F8FAFC', '#F1F5F9', '#E2E8F0', '#CBD5E1'],
        ['#FFFFFF', '#FFFFFF', '#F8FAFC', '#F1F5F9', '#E2E8F0'],
    ]

    for r in range(5):
        for c in range(5):
            rect = patches.Rectangle((c, 4 - r), 1, 1, facecolor=matrix_shades[r][c], edgecolor='#94A3B8', lw=1)
            ax.add_patch(rect)

    risks = [
        ("R1", 2.5, 3.5, "R1: ร้านค้าไม่คุ้นเคยเทคโนโลยี"),
        ("R2", 1.5, 3.2, "R2: สัญญาณเครือข่าย/เน็ตขัดข้อง"),
        ("R3", 3.2, 1.8, "R3: ยอดขายลดลงช่วงปิดภาคเรียน"),
        ("R4", 1.2, 1.5, "R4: การแข่งขันจากแอปภายนอก"),
        ("R5", 2.2, 0.8, "R5: ข้อผิดพลาดการชำระเงิน"),
        ("R6", 0.8, 1.2, "R6: นโยบายสถานที่มหาวิทยาลัย")
    ]

    for code, x, y, full_text in risks:
        ax.scatter(x, y, s=240, color='#0F172A', edgecolors='#FFFFFF', linewidth=1.5, zorder=5)
        ax.text(x, y, code, color='#FFFFFF', fontweight='bold', fontsize=9, ha='center', va='center', zorder=6)
        ax.annotate(full_text, (x, y), xytext=(x+0.16, y+0.12),
                    fontsize=8.5, color=CLR_DARK, fontweight='bold',
                    bbox=dict(boxstyle="square,pad=0.2", fc="#FFFFFF", ec=CLR_BORDER, lw=0.8), zorder=7)

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5])
    ax.set_xticklabels(['1: น้อยมาก', '2: น้อย', '3: ปานกลาง', '4: สูง', '5: รุนแรง'], fontsize=9)
    ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5])
    ax.set_yticklabels(['1: เกิดขึ้นได้ยาก', '2: ไม่น่าจะเกิด', '3: อาจจะเกิดขึ้น', '4: มีโอกาสเกิดสูง', '5: เกิดขึ้นแน่นอน'], fontsize=9)

    ax.set_xlabel('ระดับความรุนแรงของผลกระทบ (Impact Level) -->', fontsize=10.5, color=CLR_DARK, labelpad=8)
    ax.set_ylabel('ระดับโอกาสที่จะเกิดความเสี่ยง (Likelihood Level) -->', fontsize=10.5, color=CLR_DARK, labelpad=8)
    ax.set_title('เมทริกซ์การประเมินระดับความเสี่ยง (Risk Assessment Matrix)', fontsize=13, fontweight='bold', color=CLR_DARK, pad=12)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'risk_matrix.png')
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print('Saved academic risk_matrix.png')

# ==========================================
# 5. ACADEMIC BUSINESS MODEL CANVAS
# ==========================================
def create_bmc_graphic():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=300)
    fig.patch.set_facecolor(CLR_BG)
    ax.set_facecolor(CLR_BG)

    # Exact Strategyzer layout in clean academic black and white
    blocks = [
        ("Key Partners\n(พันธมิตรหลัก)", 0.2, 3.0, 2.6, 5.0, [
            "- ร้านอาหารในโรงอาหาร มจพ.",
            "- ผู้ให้บริการ PromptPay / QR",
            "- มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ",
            "- แพลตฟอร์ม LINE Official Account"
        ]),
        ("Key Activities\n(กิจกรรมหลัก)", 2.9, 5.5, 2.6, 2.5, [
            "- พัฒนาระบบสั่งอาหารผ่าน LINE",
            "- จัดการคิวและรอบเวลารับอาหาร",
            "- ส่งคำสั่งซื้อแบบเรียลไทม์ให้ร้านค้า",
            "- ประสานงานและอบรมร้านอาหาร"
        ]),
        ("Key Resources\n(ทรัพยากรหลัก)", 2.9, 3.0, 2.6, 2.4, [
            "- ระบบ LINE Official Account (LIFF)",
            "- ฐานข้อมูลเมนูและคำสั่งซื้อ",
            "- เซิร์ฟเวอร์และโครงสร้างพื้นฐานคลาวด์",
            "- ทีมนักพัฒนาระบบและฝ่ายสนับสนุน"
        ]),
        ("Value Propositions\n(คุณค่าที่ส่งมอบ)", 5.6, 3.0, 2.8, 5.0, [
            "- ลดระยะเวลาต่อคิวและรอคอยอาหาร",
            "- สามารถสั่งเมนูอาหารล่วงหน้าได้",
            "- แสดงระยะเวลาคาดการณ์เสร็จแม่นยำ",
            "- ร้านค้าจัดการคำสั่งซื้อได้เป็นระบบ",
            "- ลดความแออัดในโรงอาหารช่วงพักเที่ยง",
            "- ระบบชำระเงินดิจิทัลไร้เงินสดสะดวกรวดเร็ว"
        ]),
        ("Customer Relationships\n(ความสัมพันธ์กับลูกค้า)", 8.5, 5.5, 2.6, 2.5, [
            "- แจ้งเตือนสถานะออเดอร์ผ่าน LINE อัตโนมัติ",
            "- ติดตามสถานะคำสั่งซื้อแบบเรียลไทม์",
            "- ระบบรีวิวและให้คะแนนร้านอาหาร",
            "- สิทธิประโยชน์สะสมแต้มแลกอาหารฟรี"
        ]),
        ("Channels\n(ช่องทางการเข้าถึง)", 8.5, 3.0, 2.6, 2.4, [
            "- LINE Official Account (LIFF)",
            "- ป้าย QR Code ตามโต๊ะอาหารและหน้าร้าน",
            "- ประชาสัมพันธ์ผ่านเพจ มจพ. และโซเชียลมีเดีย"
        ]),
        ("Customer Segments\n(กลุ่มลูกค้าเป้าหมาย)", 11.2, 3.0, 2.6, 5.0, [
            "- นักศึกษาภายในมหาวิทยาลัย (กลุ่มหลัก)",
            "  * ผู้มีเวลาพักเที่ยงจำกัด",
            "- อาจารย์และบุคลากรทางการศึกษา",
            "- ร้านอาหารในโรงอาหารมหาวิทยาลัย",
            "  * ต้องการจัดระบบครัวและเพิ่มยอดขาย"
        ]),
        ("Cost Structure\n(โครงสร้างต้นทุน)", 0.2, 0.4, 6.8, 2.5, [
            "- ต้นทุนการพัฒนาระบบซอฟต์แวร์และแอปพลิเคชัน",
            "- ค่าบริการคลาวด์เซิร์ฟเวอร์และฐานข้อมูล (Cloud Hosting & Database)",
            "- ค่าบำรุงรักษาและบริหารจัดการระบบ (System Maintenance)",
            "- ค่าบริการแพ็กเกจข้อความ LINE OA และสื่อประชาสัมพันธ์"
        ]),
        ("Revenue Streams\n(แหล่งที่มารายได้)", 7.1, 0.4, 6.7, 2.5, [
            "- ค่าธรรมเนียมจากร้านอาหารต่อคำสั่งซื้อ (Transaction Commission 3-5%)",
            "- ค่าบริการสมาชิกรายงานสถิติร้านค้า (Merchant Subscription 199 บ./เดือน)",
            "- ค่าโฆษณาและแบนเนอร์โปรโมตร้านอาหาร/เมนูแนะนำภายในระบบ"
        ])
    ]

    for title, x, y, w, h, items in blocks:
        # Box
        rect = patches.Rectangle((x, y), w, h, facecolor='#FFFFFF', edgecolor=CLR_DARK, linewidth=1.2, zorder=2)
        ax.add_patch(rect)
        # Header strip
        head = patches.Rectangle((x, y + h - 0.65), w, 0.65, facecolor='#F8FAFC', edgecolor=CLR_DARK, linewidth=1.0, zorder=3)
        ax.add_patch(head)
        ax.text(x + w/2, y + h - 0.33, title, fontsize=9.5, fontweight='bold', color=CLR_DARK, ha='center', va='center', zorder=4)

        # Items
        item_y = y + h - 0.85
        for itm in items:
            ax.text(x + 0.12, item_y, itm, fontsize=8.5, color=CLR_BODY, va='top', zorder=4)
            item_y -= 0.35

    ax.text(0.2, 8.2, 'THE BUSINESS MODEL CANVAS: SMART QUEUE FOOD', fontsize=14, fontweight='bold', color=CLR_DARK)
    ax.text(13.8, 8.2, 'วิชา: 080203914 ผู้ประกอบการนวัตกรรม มจพ.', fontsize=10, color=CLR_MUTED, ha='right')

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.6)
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'bmc_graphic.png')
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print('Saved academic bmc_graphic.png')

if __name__ == '__main__':
    create_positioning_map()
    create_system_architecture()
    create_ui_mockup()
    create_risk_matrix()
    create_bmc_graphic()
    print('All academic graphics generated successfully!')
