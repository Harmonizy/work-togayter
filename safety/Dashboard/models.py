from django.db import models

class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="ชื่อหมวดหมู่")
    color = models.CharField(max_length=7, blank=True, help_text="Hex color code (e.g. #ff0000)")

    class Meta:
        verbose_name = verbose_name_plural = "2. หมวดหมู่เหตุการณ์"
        
    def __str__(self):
        return self.name


class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "1. ปฏิทินเหตุการณ์"
        
    def __str__(self):
        return f"{self.date}-{self.time} :: {self.title}"


class ThailandHoliday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=100)
    
    annual_repeat = models.BooleanField(default=True, help_text="If checked, this holiday recurs annually on the same date.")

    class Meta:
        verbose_name = verbose_name_plural = "3. วันหยุดราชการ"
        
    def __str__(self):
        return f"{self.name} ({self.date})"
