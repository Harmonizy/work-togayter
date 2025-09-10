from django.db import models

class HazardLogStatusChoices(models.TextChoices):
    OPEN = 'O', 'เปิด'
    CLOSE = 'C', 'ปิด'

class LikelihoodChoices(models.IntegerChoices):
    IMPOSSIBLE = 0, "0 - เป็นไปไม่ได้"
    RARE = 1, "1 - เกิดขึ้นได้น้อยมาก"
    UNLIKELY = 2, "2 - ไม่น่าจะเกิด"
    POSSIBLE = 3, "3 - อาจเกิดขึ้นได้"
    LIKELY = 4, "4 - มีแนวโน้มจะเกิด"
    ALMOST_CERTAIN = 5, "5 - เกิดขึ้นแทบแน่นอน"

class SeverityChoices(models.IntegerChoices):
    NONE = 0, "0 - ไม่มีความรุนแรง"
    MINOR = 1, "1 - ความรุนแรงเล็กน้อย"
    MODERATE = 2, "2 - ความรุนแรงปานกลาง"
    SERIOUS = 3, "3 - ความรุนแรงมาก"
    MAJOR = 4, "4 - ความรุนแรงร้ายแรง"
    CRITICAL = 5, "5 - ความรุนแรงวิกฤต"
    
class HazardSourceChoices(models.IntegerChoices):
    REPORT = 1, 'รายงาน'
    INSPECTION = 2, 'ตรวจสอบ'
    MEETING = 3, 'ประชุม'
    SURVEY = 4, 'สำรวจ'

class InspectChoices(models.TextChoices):
    START_INVESTIGATION = 'S', 'เริ่มการสอบสวน'
    DATA_CAPTURE_ONLY = 'D', 'เก็บข้อมูล'


class CAPStatusChoices(models.TextChoices):
    PLANNING = 'P', 'วางแผน'
    IN_PROGRESS = 'I', 'กำลังดำเนินการ'
    COMPLETE = 'C', 'เสร็จสิ้น'

