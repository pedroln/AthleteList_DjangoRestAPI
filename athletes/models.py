from django.db import models
from django.utils.translation import gettext as _ 

class Athletes(models.Model):
    Name = models.CharField("Name", max_length = 255)
    Sex = models.CharField("Sex", max_length = 255)
    Age = models.CharField("Age", max_length=255)
    Height = models.CharField("Height", max_length=255)
    Weight = models.CharField("Weight", max_length=255)
    Team = models.CharField("Team", max_length = 255)
    NOC = models.CharField("NOC", max_length = 255)
    Games = models.CharField("Games", max_length = 255)
    Year = models.CharField("Year", max_length=255)
    Season = models.CharField("Season", max_length = 255)
    City = models.CharField("City", max_length = 255)
    Sport = models.CharField("Sport", max_length = 255)
    Event = models.CharField("Event", max_length = 255)
    Medal = models.CharField("Medal", max_length = 255)

    
