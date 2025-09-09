from django.db import models


class RegionChoices(models.TextChoices):
    NORTH = "NT", "ภาคเหนือ"
    CENTRAL = "CT", "ภาคกลาง"
    WEST = "WT", "ภาคตะวันตก"
    EAST = "ET", "ภาคตะวันออก"
    NORTHEAST = "NE", "ภาคตะวันออกเฉียงเหนือ"
    SOUTH = "ST", "ภาคใต้"


# class EventTypeChoices(models.TextChoices):
#     FLIGHT_OPERATION = "FO", "Flight Operation"
#     AIRCREW = "ACW", "Aircrew"
    # AIRCRAFT = "ACF", "Aircraft"
    # AERODROME = "AD", "Aerodrome" 
    # AIR_TRAFFIC_CONTROL = "ATC", "Air Traffic Control"
    # ARMAMENT = "ARM", "Armament"
    # AMBIENCE = "AMB", "Ambience"
    # TRAFFIC_SAFETY = "TF", "การจราจร"
    # FIRE_PREVENTION = "G2", "การป้องกันอัคคีภัย"
    # INDUSTIAL_SAFETY = "G3", "Ground 3"
    # PUBLIC_WORKS_SAFETY = "G4", "Ground 4"
    # ARMAMENT_SAFETY = "G5", "Ground 5"
    # AIRCRAFT_AND_APRON = "G6", "Ground 6"
    # GENERAL_SAFETY = "G7", "Ground 7"