from django.db import models

class Config(models.Model):
    key = models.CharField(verbose_name="Key", max_length=120, unique=True, null = False, blank = False)
    value = models.CharField(verbose_name="Value", max_length=255, null = False, blank = False)
    description = models.CharField(verbose_name="Description", max_length=255, null = True, blank = True)

    def __str__(self):
        return self.key
    
    @classmethod
    def load(cls, key, default=None):
        obj, created = cls.objects.get_or_create(key = key)
        if created:
            obj.value = default
            obj.save()
        return obj.value
    
    @classmethod
    def set(cls, key, value):
        obj, _ = cls.objects.get_or_create(key = key)
        obj.value = value
        obj.save()