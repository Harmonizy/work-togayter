from django.db import models

class MissionTypeChoices(models.TextChoices):
    AVIATION = "A", "ภาคอากาศ"
    GROUND = "G", "ภาคพื้น"


class ReportTypeChoices(models.TextChoices):
    SIMPLE = 'S', 'รายงานขั้นต้น'
    HAZARD_GROUND = 'HG', 'รายงานอุบัติการณ์ภาคพื้น'
    HAZARD_AVIATION = 'HA', 'รายงานอากาศยานอุบัติการณ์'
    SAFETY_GROUND = 'SG', 'รายงานอุบัติเหตุภาคพื้น'
    SAFETY_AVIATION = 'SA', 'รายงานอากาศยานอุบัติเหตุ'
    OBSERVATION = 'O', 'สังเกตการณ์พฤติกรรม'


class BaseReportTypeChoices(models.TextChoices):
    HAZARD_GROUND = 'HG', 'รายงานอันตราย (ภาคพื้น)'
    HAZARD_AVIATION = 'HA', 'รายงานอันตราย (ภาคอากาศ)'
    SAFETY_GROUND = 'SG', 'รายงานนิรภัยอุบัติการณ์ (ภาคพื้น)'
    SAFETY_AVIATION = 'SA', 'รายงานนิรภัยอุบัติการณ์ (ภาคอากาศ)'


class PriorityChoices(models.TextChoices):
    HIGH = "H", "เร่งด่วน"
    MEDIUM = "M", "ต้องติดตาม"
    LOW = "L", "ปกติ"


class ReportStatusChoices(models.IntegerChoices):
    DRAFT = 1, "ร่าง"
    SUBMITTED = 2, "ส่งแล้ว"
    CHECKING = 3, "รอตรวจสอบ"
    APPROVED = 4, "อนุมัติ"
    REJECTED = 5, "ไม่อนุมัติ"


class DamageTypeChoices(models.IntegerChoices):
    NONE = 0, "ไม่มี"
    MINOR = 1, "เล็กน้อย"
    MAJOR = 2, "มาก"
    BROKEN = 3, "ชั้นจำหน่าย"


class InjuryTypeChoices(models.IntegerChoices):
    SAFE = 1, "ปลอดภัย"
    MINOR = 2, "บาดเจ็บเล็กน้อย"
    SEVERE = 3, "บาดเจ็บสาหัส"
    DEATH = 4, "เสียชีวิต"


class OrganizationExpectationChoice(models.TextChoices): 
    ABOVE = "A", "Above"
    BELOW = "B", "Below"


class BelowTheoryChoice(models.TextChoices):
    SAFETY_BEHAVIOR = "S", "SafetyBehavior"
    VULNERABILITY = "V", "VulnerabilityTheory"
