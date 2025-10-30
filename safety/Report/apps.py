from django.apps import AppConfig


class ReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'safety.Report'
    verbose_name = "1. SafetyReport"

    def ready(self):
        import safety.Report.rules
