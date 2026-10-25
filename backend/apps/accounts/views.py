from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, LoginSerializer
from .permissions import IsAdminRole
from apps.audit.utils import record_audit

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response(
                {"detail": "Tên đăng nhập hoặc mật khẩu không chính xác."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"detail": "Tài khoản của bạn đã bị vô hiệu hóa hoặc khóa."},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)
        record_audit(request, "LOGIN", "User", user.id, f"Đăng nhập thành công với vai trò {user.role}")

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })

class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    permission_classes = [IsAdminRole]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def perform_update(self, serializer):
        instance = serializer.instance
        if (instance.username == 'admin' or instance.is_superuser) and serializer.validated_data.get('is_active') is False:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Không thể vô hiệu hóa hoặc khóa tài khoản Quản trị viên tối cao.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.username == 'admin' or instance.is_superuser:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Không thể xóa tài khoản Quản trị viên tối cao.")
        instance.delete()
