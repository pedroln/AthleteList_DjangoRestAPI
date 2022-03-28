from athletes.models import Athletes 
from rest_framework import serializers

class AthleteSerializer (serializers.ModelSerializer):
    class Meta:
        model = Athletes
        fields = ['id', 
        'Name', 'Sex', 
        'Age', 
        'Height', 
        'Weight', 
        'Team',
        'NOC',
        'Games',
        'Year',
        'Season',
        'City',
        'Sport',
        'Event',
        'Medal' ]

        