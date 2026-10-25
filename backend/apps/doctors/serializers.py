from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Doctor
from apps.accounts.serializers import UserSerializer
from apps.specialties.serializers import SpecialtySerializer
import random

User = get_user_model()

class DoctorSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    full_name = serializers.SerializerMethodField()

    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'user_details', 'code', 'specialty', 'specialty_name',
            'room_number', 'phone', 'email', 'consultation_fee', 'bio',
            'is_active', 'full_name', 'created_at', 'updated_at',
            'username', 'password', 'first_name', 'last_name'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'required': False}
        }

    def get_full_name(self, obj):
        name = f"{obj.user.last_name} {obj.user.first_name}".strip()
        return name if name else obj.user.username

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', 'Doc@123')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')

        user = validated_data.get('user')
        if not user and username:
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError({"username": f"Tên đăng nhập '{username}' đã tồn tại."})
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=validated_data.get('email', ''),
                phone=validated_data.get('phone', ''),
                role=User.Role.DOCTOR
            )
            validated_data['user'] = user

        if not validated_data.get('code'):
            for _ in range(10):
                code = f"BS-{random.randint(1000, 9999)}"
                if not Doctor.objects.filter(code=code).exists():
                    validated_data['code'] = code
                    break

        return super().create(validated_data)

    def update(self, instance, validated_data):
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        phone = validated_data.get('phone', None)
        email = validated_data.get('email', None)

        if first_name is not None or last_name is not None or phone is not None or email is not None:
            user = instance.user
            if first_name is not None: user.first_name = first_name
            if last_name is not None: user.last_name = last_name
            if phone is not None: user.phone = phone
            if email is not None: user.email = email
            user.save()

        return super().update(instance, validated_data)
