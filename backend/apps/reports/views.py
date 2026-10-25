from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from django.db.models import Count
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.appointments.models import Appointment
from apps.medical_records.models import MedicalRecord
from apps.specialties.models import Specialty

class DashboardStatsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()

        total_patients = Patient.objects.filter(is_active=True).count()
        total_doctors = Doctor.objects.filter(is_active=True).count()
        today_appointments = Appointment.objects.filter(appointment_date=today).count()
        pending_appointments = Appointment.objects.filter(status='PENDING').count()
        completed_appointments = Appointment.objects.filter(status='COMPLETED').count()
        total_medical_records = MedicalRecord.objects.count()

        # Thống kê lịch khám theo trạng thái
        status_counts = dict(
            Appointment.objects.values('status')
            .annotate(count=Count('id'))
            .values_list('status', 'count')
        )

        # Thống kê lịch khám theo chuyên khoa
        specialty_counts = list(
            Specialty.objects.annotate(appointment_count=Count('appointments'))
            .values('name', 'appointment_count')
            .order_by('-appointment_count')[:6]
        )

        # Thống kê lịch khám 7 ngày gần nhất
        last_7_days = []
        for i in range(6, -1, -1):
            date = today - timezone.timedelta(days=i)
            count = Appointment.objects.filter(appointment_date=date).count()
            last_7_days.append({
                "date": date.strftime("%d/%m"),
                "count": count
            })

        return Response({
            "metrics": {
                "total_patients": total_patients,
                "total_doctors": total_doctors,
                "today_appointments": today_appointments,
                "pending_appointments": pending_appointments,
                "completed_appointments": completed_appointments,
                "total_medical_records": total_medical_records,
            },
            "status_distribution": status_counts,
            "specialty_distribution": specialty_counts,
            "recent_7_days": last_7_days,
        })
