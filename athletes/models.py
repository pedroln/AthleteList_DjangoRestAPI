from django.db import models
from django.utils.translation import gettext as _ 

class Athletes(models.Model):
    Name = models.CharField(_("Name"), max_length = 255)
    Sex = models.CharField(_("Sex"), max_length = 255)
    Age = models.CharField(_("Age"), max_length = 255)
    Height = models.CharField(_("Height"), max_length = 255)
    Weight = models.CharField(_("Weight"), max_length = 255)
    Team = models.CharField(_("Team"), max_length = 255)
    NOC = models.CharField(_("NOC"), max_length = 255)
    Games = models.CharField(_("Games"), max_length = 255)
    Year = models.CharField(_("Year"), max_length = 255)
    Season = models.CharField(_("Season"), max_length = 255)
    City = models.CharField(_("City"), max_length = 255)
    Sport = models.CharField(_("Sport"), max_length = 255)
    Event = models.CharField(_("Event"), max_length = 255)
    Medal = models.CharField(_("Medal"), max_length = 255)

    
