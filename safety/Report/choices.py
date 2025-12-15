from django.db import models


class ReportTypeChoices(models.TextChoices):
    SIMPLE = 'S', 'รายงานขั้นต้น'
    OBSERVATION = 'O', 'สังเกตการณ์พฤติกรรม'

    HAZARD_GROUND = 'HG', 'รายงานอันตรายภาคพื้น'
    SAFETY_GROUND = 'SG', 'รายงานอุบัติการณ์ภาคพื้น'
    MINOR_ACCIDENT_GROUND = 'MIG', 'รายงานอุบัติเหตุภาคพื้นย่อย'
    MAJOR_ACCIDENT_GROUND = 'MJG', 'รายงานอุบัติเหตุภาคพื้นร้ายแรง'

    HAZARD_AVIATION = 'HA', 'รายงานอากาศยานอุบัติการณ์'
    SAFETY_AVIATION = 'SA', 'รายงานอากาศยานอุบัติเหตุ'


class GroundSafetyCategoryChoices(models.IntegerChoices):
    OPERATOR = 1, 'สาขานิรภัยอุตสาหการ'
    AIRPORT = 2, 'สาขานิรภัยอากาศยานและลานจอด'
    INDUSTRIAL = 3, 'สาขานิรภัยสาธารณูปการ'
    FIRE_PREVENTION = 4, 'สาขานิรภัยการป้องกันอัคคีภัย'
    ARMAMENT = 5, 'สาขานิรภัยการสรรพาวุธ'
    TRAFFIC = 6, 'สาขานิรภัยการจราจร'
    GENERAL = 7, 'สาขานิรภัยทั่วไป'


class BaseReportTypeChoices(models.TextChoices):
    HAZARD_GROUND = 'HG', 'รายงานอันตราย (ภาคพื้น)'
    HAZARD_AVIATION = 'HA', 'รายงานอันตราย (การบิน)'
    SAFETY_GROUND = 'SG', 'รายงานนิรภัยอุบัติการณ์ (ภาคพื้น)'
    SAFETY_AVIATION = 'SA', 'รายงานนิรภัยอุบัติการณ์ (การบิน)'


class PriorityChoices(models.TextChoices):
    HIGH = "H", "เร่งด่วน"
    MEDIUM = "M", "ต้องติดตาม"
    LOW = "L", "ปกติ"


class ReportStatusChoices(models.IntegerChoices):
    DRAFT = 1, "ร่าง"
    APPROVED = 2, "อนุมัติ"
    REJECTED = 3, "ไม่อนุมัติ"
    DELETED = 4, "ลบ"


class DamageTypeChoices(models.IntegerChoices):
    NONE = 0, "ไม่มี"
    MINOR = 1, "เล็กน้อย"
    MAJOR = 2, "มาก"
    BROKEN = 3, "ชั้นจำหน่าย"


class InjuryLevelChoices(models.IntegerChoices):
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


class RoleTypeChoices(models.TextChoices):
    INJURY = "I", "ผู้บาดเจ็บ"
    DEATH = "D", "ผู้เสียชีวิต"
    PILOT = "P", "นักบิน"
    PASSENGER = "G", "ผู้โดยสาร"
    TEACHER = "T", "ครูการบิน"
    STUDENT = "S", "ศิษย์การบิน"


class AccidentTypeChoices(models.IntegerChoices):
    ACCIDENT = 1, "ย่อย"
    INCIDENT = 2, "ร้ายแรง"


# -------------------------------------------------------------------------------
# 6A
# --------------------------------------------------------------------------------


class QuestionCategoryChoices(models.IntegerChoices):
    AIRCREW = 1, "ผู้ทำการในอากาศ (Aircrew)"
    AIRCRAFT = 2, "อากาศยาน (Aircraft)"
    AIRPORT = 3, "สนามบิน (Airport)"
    ATC = 4, "การควบคุมจราจรทางอากาศ (Air Traffic Control)"
    ARMAMENT = 5, "ยุทโธปกรณ์ (Armament)" 
    AMBIENT = 6, "สภาพแวดล้อม (Ambient)"


class AnswerChoices(models.IntegerChoices):
    YES = 1, "Y"
    NO = 2, "N"