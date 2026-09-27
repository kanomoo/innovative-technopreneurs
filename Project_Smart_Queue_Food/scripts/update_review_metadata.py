from pathlib import Path
root=Path(__file__).resolve().parents[2]
guide=root/'Wiki'/'Final_Project_Report_and_Presentation_Guide.md'
t=guide.read_text(encoding='utf8').replace('updated: 2026-09-09','updated: 2026-09-27').replace('ตุลาคม 2568','ตุลาคม 2569')
t=t.replace('1. *Product/Service Innovation:* นวัตกรรมตัวผลิตภัณฑ์','1. *Configuration:* Profit Model, Network, Structure, Process').replace('2. *Process Innovation:* นวัตกรรมกระบวนการผลิตหรือการให้บริการ','2. *Offering:* Product Performance, Product System').replace('3. *Business Model Innovation:* นวัตกรรมการสร้างรายได้และการจับมือพันธมิตร','3. *Experience:* Service, Channel, Brand, Customer Engagement')
t=t.replace('**3 มิติของนวัตกรรม (3 Innovation Dimensions):**','**3 หมวดของ Ten Types of Innovation ตามบทเรียนที่ 5:**')
anchor='## 📅 กำหนดการส่งงานและการนำเสนอ (Deadlines & Schedule)'
scope='''> **ขอบเขตหลักฐานที่ตรวจ 27 กันยายน 2569:** คำถอดความวันที่ 4 และ 11 กันยายนเป็นเกณฑ์รายงานของวิชา ส่วนบทสัมภาษณ์วันที่ 26 มกราคมเป็น Smart Green Wall คนละโครงการกับ Smart Queue Food ใช้ดูวิธีสัมภาษณ์ได้ แต่ใช้ยืนยันลูกค้าหรือประสิทธิภาพของ Smart Queue Food ไม่ได้ ตัวเลขลดฝุ่นในตัวอย่างเป็นคำเสนอของผู้สัมภาษณ์ ไม่ใช่ผลทดสอบ และความคิดเห็น 2 คนไม่ยืนยันความเป็นไปได้ของธุรกิจทั้งตลาด

**สิ่งที่อาจารย์ระบุ:** ส่ง PDF รายงานและสไลด์ทาง LINE กลุ่มภายในเที่ยง 1 ตุลาคม 2569; พิมพ์ส่งทั้งรายงานและสไลด์ 2 ตุลาคมทุกกลุ่ม; นำเสนอ 2 หรือ 9 ตุลาคม กลุ่มละประมาณ 10 นาทีและถามตอบ 5 นาที ลำดับกลุ่มยังต้องตกลง ไม่ควรถือว่ากลุ่ม 1–9 และ 10–18 ถูกแบ่งตายตัวจากคำถอดความ

**หัวข้อบังคับ 10 ส่วน:** Business Idea, Vision & Mission, Value Proposition, Product/Service, Target Customers, BMC 9 ช่องในหนึ่งหน้าพร้อมคำอธิบาย, Marketing & Sales (Positioning และ 4Ps), Technology & Innovation (เลือกยุทธวิธีที่เหมาะสม), Risk & Mitigation และ Summary รูปแบบ 5 บทของตัวอย่างวิทยานิพนธ์ไม่แทนเกณฑ์รายวิชานี้ และคำบรรยายที่ตรวจไม่ได้กำหนดว่าต้องมีระบบเปิดใช้จริงหรือผลสำรวจจำนวนใด

**คะแนน:** ประโยค “สูงสุด 28... มี 10 ถึง 5...” ในคำถอดความวันที่ 11 กันยายนมีบริบทไม่ครบ จึงยังไม่ใช้เป็นตารางเกณฑ์คะแนนหรือรับประกันคะแนนของรายงาน

'''
if 'ขอบเขตหลักฐานที่ตรวจ 27 กันยายน' not in t:t=t.replace(anchor,scope+anchor)
guide.write_text(t,encoding='utf8')
review=root/'Project_Smart_Queue_Food'/'presentation_review.md'
t=review.read_text(encoding='utf8').replace('รายงานเดิมบทที่ 10.3 ใช้กรณี 8 ร้าน GP 4% ซึ่งต่างจากกรณีในสไลด์ ต้องปรับให้เป็นกรณีเดียวกันหากจะอ้างตัวเลขข้ามเอกสาร','ตรวจทานวันที่ 27 กันยายน 2569: รายงานบทที่ 10.3 ปรับให้เป็นกรณีฐานเดียวกับสไลด์แล้ว คือ 3 ร้าน ราคา 45 บาท GP 3% และ 20 วันต่อเดือน พร้อมแยกต้นทุนที่ยังไม่รวม ไม่ใช้ผลนี้เป็นกำไรสุทธิหรือการคืนทุนที่ยืนยันแล้ว')
review.write_text(t,encoding='utf8')
readme=root/'00_ไฟล์ส่งงาน_Smart_Queue_Food'/'README_คำอธิบายไฟล์ส่งงาน.txt'
t=readme.read_text(encoding='utf8').replace('รายงานบทที่ 10.3 ใช้กรณี 8 ร้าน GP 4% จึงต้องแยกกรณีเมื่อตอบคำถามหรืออ้างตัวเลขข้ามไฟล์','รายงานบทที่ 10.3 ปรับเป็นกรณีเดียวกับสไลด์แล้ว ยังไม่มีผลสัมภาษณ์/ทดลองเฉพาะ Smart Queue Food\n   งบ LINE ต้องตรวจโควตาข้อความจริง และสูตรคืนทุนเป็นการจำลองก่อนรวมต้นทุนที่ยังขาด')
t=t.replace('ปราศจากการอ้างผลการทดสอบระบบที่เกินจริง','ตรวจทานให้แยกสมมติฐานและแผนงานออกจากผลการทดสอบที่ยังไม่มีหลักฐาน')
t=t.replace('ไม่มีไฟล์ซ้ำซ้อน ไม่มีไฟล์ชั่วคราว พร้อมสำหรับการนำไปใช้งาน ส่งตรวจ และขึ้นนำเสนอบนเวทีทันที','ไม่มีไฟล์ชั่วคราว กำหนดส่ง PDF รายงานและสไลด์ภายในเที่ยง 1 ต.ค. 2569 ทาง LINE กลุ่ม\n   พิมพ์ส่งทั้งรายงานและสไลด์ 2 ต.ค. ทุกกลุ่ม; ต้องซ้อมพูด 10 นาทีและตรวจลำดับนำเสนอในชั้นเรียน')
t=t.replace('(35 หน้า)','(37 หน้า)')
readme.write_text(t,encoding='utf8')
print('Updated project guide and delivery metadata')
