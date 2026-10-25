from rest_framework import serializers
from .models import Specialty

class SpecialtySerializer(serializers.ModelSerializer):
    doctors_count = serializers.SerializerMethodField()

    class Meta:
        model = Specialty
        fields = ['id', 'name', 'code', 'description', 'is_active', 'doctors_count', 'created_at', 'updated_at']

    def get_doctors_count(self, obj):
        return obj.doctors.filter(is_active=True).count()
