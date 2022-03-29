from django.db import models
from django.utils.translation import gettext as _ 

class Athletes(models.Model):
    Name = models.CharField("Name", max_length = 255)
    Sex = models.CharField("Sex", max_length = 255)
    Age = models.CharField("Sex", max_length = 255)
    Height = models.CharField("Height", max_length = 255, blank = True, default = "nan")
    Weight = models.CharField("Weight", max_length = 255, blank = True, default = "nan")
    Team = models.CharField("Team", max_length = 255)
    NOC = models.CharField("NOC", max_length = 255)
    Games = models.CharField("Games", max_length = 255)
    Year = models.IntegerField("Year")
    Season = models.CharField("Season", max_length = 255)
    City = models.CharField("City", max_length = 255)
    Sport = models.CharField("Sport", max_length = 255)
    Event = models.CharField("Event", max_length = 255)
    Medal = models.CharField("Medal", max_length = 255, blank = True, default = "nan")


class Regions(models.Model):
    NOC = models.CharField("NOC", max_length = 255)
    Region = models.CharField("Region", max_length = 255)
    Notes = models.CharField("Notes" , max_length = 255)

    
