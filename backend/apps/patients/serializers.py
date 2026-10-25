from rest_framework import serializers
from .models import Patient
import random

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id', 'code', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Tự sinh mã bệnh nhân BN-XXXXX nếu chưa có
        if not validated_data.get('code'):
            for _ in range(10):
                random_code = f"BN-{random.randint(10000, 99999)}"
                if not Patient.objects.filter(code=random_code).exists():
                    validated_data['code'] = random_code
                    break
        return super().create(validated_data)
