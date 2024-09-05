# Serializer to convert the philosopher data to and from JSON format
from rest_framework import serializers
from .models import Philosopher

class PhilosopherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Philosopher
        fields = '__all__'
