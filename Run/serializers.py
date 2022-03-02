from rest_framework import serializers
from .models import Run

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ['popsize', 'density', 'fips', 'startdate', 'finishdate', 'key', 'user', 'where', 'videopath', 'logpath']