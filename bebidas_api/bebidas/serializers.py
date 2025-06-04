from rest_framework import serializers
from .models import Bebida

class BebidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bebida
        fields = '__all__'
