from django.core.management.base import BaseCommand
from common.RTAFUser.models import Affiliation

class Command(BaseCommand):
    help = 'Import affiliations directly from a dictionary into the Affiliation model'

    def handle(self, *args, **kwargs):
        affiliations_data = [
                        {"id": 1, "hris_code": "002", "short_name": "สลก.ทอ.", "full_name": "สำนักงานเลขานุการกองทัพอากาศ"},
                        {"id": 2, "hris_code": "003", "short_name": "สบ.ทอ.", "full_name": "กรมสารบรรณทหารอากาศ"},
                        {"id": 3, "hris_code": "004", "short_name": "กพ.ทอ.", "full_name": "กรมกำลังพลทหารอากาศ"},
                        {"id": 4, "hris_code": "005", "short_name": "ขว.ทอ.", "full_name": "กรมข่าวทหารอากาศ"},
                        {"id": 5, "hris_code": "006", "short_name": "ยก.ทอ.", "full_name": "กรมยุทธการทหารอากาศ"},
                        {"id": 6, "hris_code": "007", "short_name": "กบ.ทอ.", "full_name": "กรมส่งกำลังบำรุงทหารอากาศ"},
                        {"id": 7, "hris_code": "010", "short_name": "กร.ทอ.", "full_name": "กรมกิจการพลเรือนทหารอากาศ"},
                        {"id": 8, "hris_code": "211", "short_name": "ทสส.ทอ.", "full_name": "กรมเทคโนโลยีสารสนเทศและการสื่อสารทหารอากาศ"},
                        {"id": 9, "hris_code": "009", "short_name": "สปช.ทอ.", "full_name": "สำนักงานปลัดบัญชีทหารอากาศ"},
                        {"id": 10, "hris_code": "042", "short_name": "กง.ทอ.", "full_name": "กรมการเงินทหารอากาศ"},
                        {"id": 11, "hris_code": "008", "short_name": "จร.ทอ.", "full_name": "กรมจเรทหารอากาศ"},
                        {"id": 12, "hris_code": "212", "short_name": "สตน.ทอ.", "full_name": "สำนักงานตรวจสอบภายในทหารอากาศ"},
                        {"id": 13, "hris_code": "213", "short_name": "สนภ.ทอ.", "full_name": "สำนักงานนิรภัยทหารอากาศ"},
                        {"id": 14, "hris_code": "214", "short_name": "สธน.ทอ.", "full_name": "สำนักงานพระธรรมนูญทหารอากาศ"},
                        {"id": 15, "hris_code": "595", "short_name": "คปอ.", "full_name": "กองบัญชาการควบคุมการปฏิบัติทางอากาศ"},
                        {"id": 16, "hris_code": "026", "short_name": "อย.", "full_name": "หน่วยบัญชาการอากาศโยธิน"},
                        {"id": 17, "hris_code": "039", "short_name": "รร.การบิน", "full_name": "โรงเรียนการบิน"},
                        {"id": 18, "hris_code": "015", "short_name": "บน.1", "full_name": "กองบิน 1"},
                        {"id": 19, "hris_code": "012", "short_name": "บน.2", "full_name": "กองบิน 2"},
                        {"id": 20, "hris_code": "019", "short_name": "บน.4", "full_name": "กองบิน 4"},
                        {"id": 21, "hris_code": "126", "short_name": "บน.5", "full_name": "กองบิน 5"},
                        {"id": 22, "hris_code": "013", "short_name": "บน.6", "full_name": "กองบิน 6"},
                        {"id": 23, "hris_code": "064", "short_name": "บน.7", "full_name": "กองบิน 7"},
                        {"id": 24, "hris_code": "016", "short_name": "บน.21", "full_name": "กองบิน 21"},
                        {"id": 25, "hris_code": "017", "short_name": "บน.23", "full_name": "กองบิน 23"},
                        {"id": 26, "hris_code": "020", "short_name": "บน.41", "full_name": "กองบิน 41"},
                        {"id": 27, "hris_code": "021", "short_name": "บน.46", "full_name": "กองบิน 46"},
                        {"id": 28, "hris_code": "024", "short_name": "บน.56", "full_name": "กองบิน 56"},
                        {"id": 29, "hris_code": "", "short_name": "สกบ.ทอ.", "full_name": "สำนักงานการบินกองทัพอากาศ"},
                        {"id": 30, "hris_code": "496", "short_name": "ศซบ.ทอ.", "full_name": "ศูนย์ไซเบอร์กองทัพอากาศ"},
                        {"id": 32, "hris_code": "066", "short_name": "บน.3", "full_name": "กองบิน 3"},
                        {"id": 34, "hris_code": "028", "short_name": "ชอ.", "full_name": "กรมช่างอากาศ"},
                        {"id": 35, "hris_code": "215", "short_name": "สอ.ทอ.", "full_name": "กรมสื่อสารอิเล็กทรอนิกส์ทหารอากาศ"},
                        {"id": 36, "hris_code": "030", "short_name": "สพ.ทอ.", "full_name": "กรมสรรพาวุธทหารอากาศ"},
                        {"id": 37, "hris_code": "034", "short_name": "พอ.", "full_name": "กรมแพทย์ทหารอากาศ"},
                        {"id": 38, "hris_code": "031", "short_name": "พธ.ทอ.", "full_name": "กรมพลาธิการทหารอากาศ"},
                        {"id": 39, "hris_code": "032", "short_name": "ชย.ทอ.", "full_name": "กรมช่างโยธาทหารอากาศ"},
                        {"id": 40, "hris_code": "033", "short_name": "ขส.ทอ.", "full_name": "กรมขนส่งทหารอากาศ"},
                        {"id": 41, "hris_code": "498", "short_name": "ศซว.ทอ.", "full_name": "ศูนย์ซอฟต์แวร์กองทัพอากาศ"},
                        {"id": 42, "hris_code": "037", "short_name": "ยศ.ทอ.", "full_name": "กรมยุทธศึกษาทหารอากาศ"},
                        {"id": 43, "hris_code": "040", "short_name": "รร.นนก.", "full_name": "โรงเรียนนายเรืออากาศนวมินทกษัตริยา​ธิ​​ราช"},
                        {"id": 45, "hris_code": "041", "short_name": "สก.ทอ.", "full_name": "กรมสวัสดิการทหารอากาศ"},
                        {"id": 46, "hris_code": "049", "short_name": "สน.ผบ.ดม.", "full_name": "สำนักงานผู้บังคับทหารอากาศดอนเมือง"},
                        {"id": 47, "hris_code": "217", "short_name": "สวบ.ทอ.", "full_name": "สถาบันเวชศาสตร์การบินกองทัพอากาศ​"},
                        {"id": 48, "hris_code": "", "short_name": "สง.ปรมน.ทอ.", "full_name": "สำนักงานประสานภารกิจด้านความมั่นคงกับกองอำนวยการรักษาความมั่นคงภายในราชอาณาจักรกองทัพอากาศ"},
                        {"id": 49, "hris_code": "", "short_name": "สยล.ทอ.", "full_name": "สำนักงานยุทธศาสตร์และหลักนิยมกองทัพอากาศ(เพื่อพลาง)​"},
                        {"id": 50, "hris_code": "", "short_name": "สพร.ทอ.", "full_name": "สำนักงานพัฒนาระบบราชการกองทัพอากาศ"},
                        {"id": 51, "hris_code": "", "short_name": "ศกอ.", "full_name": "ศูนย์การสงครามทางอากาศ"},
                        {"id": 52, "hris_code": "", "short_name": "ศฮพ.", "full_name": "ศูนย์อำนวยการเฮลิคอปเตอร์พระราชพาหนะ"},
                        {"id": 53, "hris_code": "", "short_name": "ศบพ.", "full_name": "ศูนย์อำนวยการเครื่องบินพระราชพาหนะ​"},
                        {"id": 54, "hris_code": "", "short_name": "ผนน.บก.ทอ.", "full_name": "แผนกสนับสนุนกองบัญชาการกองทัพอากาศ"},
                        {"id": 55, "hris_code": "001", "short_name": "บก.ทอ.", "full_name": "กองบัญชาการกองทัพอากาศ"},
                        {"id": 58, "hris_code": "495", "short_name": "ศปอว.ทอ.", "full_name": "ศูนย์ปฏิบัติการทาง​อวกาศกองทัพอากาศ​​"},
                        {"id": 59, "hris_code": "216", "short_name": "ศวอ.ทอ.", "full_name": "ศูนย์วิจัยพัฒนาวิทยาศาสตร์เทคโนโลยีการบินและอวกาศกองทัพอากาศ"},
                        {"id": 61, "hris_code": "", "short_name": "วทอ.ยศ.ทอ.", "full_name": "วทอ.ยศ.ทอ."},
                        {"id": 62, "hris_code": "", "short_name": "รร.สธ.ทอ.ยศ.ทอ.", "full_name": "รร.สธ.ทอ.ยศ.ทอ."},
                        {"id": 63, "hris_code": "499", "short_name": "สบน.ทอ.", "full_name": "สำนักงานการบินกองทัพอากาศ​"},
                        {"id": 64, "hris_code": "", "short_name": "นขต.ทอ.", "full_name": "นขต.ทอ."},
                    ]

        for data in affiliations_data:
            id = data.get("id")
            hris_code = data.get("hris_code")
            short_name = data.get("short_name")
            full_name = data.get("full_name")
            is_rtaf_directed = True 
            
            affiliation, created = Affiliation.objects.update_or_create(
                id=id,
                hris_code=hris_code,
                defaults={
                    'short_name': short_name,
                    'full_name': full_name,
                    'is_rtaf_directed': is_rtaf_directed,
                    'super_affiliation': None,  
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created affiliation: {short_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated affiliation: {short_name}'))

        self.stdout.write(self.style.SUCCESS('Data import complete'))
