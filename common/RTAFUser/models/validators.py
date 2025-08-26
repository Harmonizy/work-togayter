from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def is_person_id(pid):

    if(len(pid) != 13 or not pid.isdigit()): return False
    calculate_number = sum([int(pid_num)*(13-i) for (i, pid_num) in enumerate(pid[:12])])
    check_digit = (11 - (calculate_number % 11)) % 10
    return check_digit == int(pid[12])   

def validate_person_id(value):
    if not is_person_id(value):
        raise ValidationError(
            _('เลขประจำตัวประชาชนไม่ถูกต้อง'),
            code='invalid'
        )
    
def validate_af_id(value):
    try:
        if not value.isdigit() or len(value) not in [10, 12]:
            raise ValidationError(
                _('เลข ขรก. ต้องเป็นตัวเลข 10 หรือ 12 หลักเท่านั้น'),
                code='invalid'
            )
    except:
        raise ValidationError(
            _('เลข ขรก. ต้องเป็นตัวเลข 10 หรือ 12 หลักเท่านั้น'),
            code='invalid'
        )