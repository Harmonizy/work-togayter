from django.apps import AppConfig


class RtafuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common.RTAFUser'
    verbose_name = "A ข้อมูลผู้ใช้งาน ทอ."

    def ready(self):
        import common.RTAFUser.signals
