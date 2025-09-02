from django.db import models


class RegionChoices(models.TextChoices):
    NORTH = "NT", "ภาคเหนือ"
    CENTRAL = "CT", "ภาคกลาง"
    WEST = "WT", "ภาคตะวันตก"
    EAST = "ET", "ภาคตะวันออก"
    NORTHEAST = "NE", "ภาคตะวันออกเฉียงเหนือ"
    SOUTH = "ST", "ภาคใต้"

