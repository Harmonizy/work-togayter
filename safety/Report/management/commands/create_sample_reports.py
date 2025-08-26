import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from safety.Data.models import (
    Event, Aircraft, AircraftSystem, FlightPhase, Location, GroundSafetyCategory
)
from common.RTAFUser.models import RTAFUser, Affiliation, Squadron
from safety.Report.models import (
    BaseReport, GroundReport, AviationReport, SafetyReport,
    SafetyReportAircraftSystem, SafetyReportFlightPhase, SafetyReportEvent
)
from safety.Report.choices import (
    MissionTypeChoices, ReportTypeChoices, DamageTypeChoices, InjuryTypeChoices, ReportStatusChoices
)

# หัวข้อภาษาไทยจำลอง
TITLES = [
    "เครื่องยนต์ขัดข้องระหว่างการบิน",
    "พบสิ่งแปลกปลอมในระบบไฮดรอลิก",
    "เกิดเหตุลื่นล้มในโรงเก็บเครื่องบิน",
    "สัญญาณเตือนไฟไหม้ทำงานผิดพลาด",
    "อุปกรณ์ภาคพื้นชำรุดระหว่างซ่อมบำรุง",
    "พบเสียงผิดปกติจากห้องนักบิน",
    "ฝนตกหนักทำให้รันเวย์ลื่น",
    "ระบบอิเล็กทรอนิกส์ไม่ตอบสนอง",
    "พนักงานได้รับบาดเจ็บจากอุปกรณ์",
    "ตรวจพบรอยรั่วที่ปีกซ้าย",
    "ระบบสื่อสารระหว่างนักบินขัดข้อง",
    "ไฟแสดงผลไม่ทำงานขณะขึ้นบิน",
    "เกิดประกายไฟจากระบบไฟฟ้า",
    "บุคคลภายนอกเข้าสู่เขตหวงห้าม",
    "พบคราบน้ำมันที่บริเวณลานจอด",
    "เครื่องบินหยุดทำงานกลางอากาศ",
    "ความผิดพลาดในการเติมน้ำมัน",
    "อุปกรณ์ช่วยชีวิตหายไปจากที่จัดเก็บ",
    "เครื่องกำเนิดไฟฟ้าสำรองไม่ทำงาน",
    "เครื่องบินลงจอดผิดรันเวย์"
]


def random_date():
    return timezone.now().date() - timedelta(days=random.randint(0, 180))


def create_user():
    user, _ = RTAFUser.objects.get_or_create(
        username="demo_user",
        defaults={"first_name": "ผู้ทดสอบ", "last_name": "ระบบ"}
    )
    return user


class Command(BaseCommand):
    help = "สร้างข้อมูลตัวอย่างรายงานนิรภัยจำนวน 20 รายงานต่อประเภท"

    def handle(self, *args, **kwargs):
        user = create_user()

        # ดึงข้อมูลที่จำเป็นจาก DB
        events = list(Event.objects.all())
        aircrafts = list(Aircraft.objects.all())
        systems = list(AircraftSystem.objects.all())
        phases = list(FlightPhase.objects.all())
        locations = list(Location.objects.all())
        categories = list(GroundSafetyCategory.objects.all())
        affiliations = list(Affiliation.objects.all())
        squadrons = list(Squadron.objects.all())

        if not (events and aircrafts and systems and phases and locations and categories):
            self.stdout.write(self.style.ERROR("❌ กรุณาเพิ่มข้อมูลอ้างอิง เช่น Event, Aircraft, Location ฯลฯ ก่อน"))
            return

        for i in range(20):
            title = random.choice(TITLES)

            # ------------------ GroundReport ------------------
            base_ground = BaseReport.objects.create(
                title=title,
                description="รายงานนี้จัดทำขึ้นเพื่อการทดสอบ",
                fiscal_year=(timezone.now().year + 543) % 100,
                event_date=random_date(),
                event_time=timezone.now().time(),
                recorder=user,
                status=random.choice(ReportStatusChoices.values)
            )

            GroundReport.objects.create(
                base_report=base_ground,
                affiliation=random.choice(affiliations),
                location="ลานจอดเครื่องบิน ทอ.ดอนเมือง",
                category=random.choice(categories),
                anonymous=random.choice([True, False])
            )

            # ------------------ AviationReport ------------------
            base_aviation = BaseReport.objects.create(
                title=random.choice(TITLES),
                description="เหตุการณ์ที่เกิดขึ้นระหว่างการบิน",
                fiscal_year=(timezone.now().year + 543) % 100,
                event_date=random_date(),
                event_time=timezone.now().time(),
                recorder=user,
                status=random.choice(ReportStatusChoices.values)
            )

            aviation = AviationReport.objects.create(
                base_report=base_aviation,
                squadron=random.choice(squadrons),
                aircraft=random.choice(aircrafts),
                anonymous=random.choice([True, False])
            )

            aviation.system.set(random.sample(systems, k=random.randint(1, len(systems))))
            aviation.flight_phase.set(random.sample(phases, k=random.randint(1, len(phases))))

            # ------------------ SafetyReport ------------------
            base_safety = BaseReport.objects.create(
                title=random.choice(TITLES),
                description="รายงานนิรภัยอุบัติการณ์",
                fiscal_year=(timezone.now().year + 543) % 100,
                event_date=random_date(),
                event_time=timezone.now().time(),
                recorder=user,
                status=random.choice(ReportStatusChoices.values)
            )

            safety = SafetyReport.objects.create(
                base_report=base_safety,
                squadron=random.choice(squadrons),
                mission_type=random.choice(MissionTypeChoices.values),
                report_type=random.choice(ReportTypeChoices.values),
                aircraft=random.choice(aircrafts),
                damage_level=random.choice(DamageTypeChoices.values),
                injury_type=random.choice(InjuryTypeChoices.values),
                location=random.choice(locations),
                latitude=random.uniform(13.5, 17.5),
                longitude=random.uniform(100.5, 104.5),
            )

            for s in random.sample(systems, k=random.randint(1, 3)):
                SafetyReportAircraftSystem.objects.create(safety_report=safety, aircraft_system=s)

            for p in random.sample(phases, k=random.randint(1, 2)):
                SafetyReportFlightPhase.objects.create(safety_report=safety, flight_phase=p)

            for e in random.sample(events, k=random.randint(1, 3)):
                SafetyReportEvent.objects.create(safety_report=safety, event=e)

        self.stdout.write(self.style.SUCCESS("✅ สร้างข้อมูลตัวอย่างรายงานสำเร็จแล้ว (20 รายงานต่อประเภท)"))
