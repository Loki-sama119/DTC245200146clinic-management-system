from .models import AuditLog

def get_client_ip(request):
    if not request:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

def record_audit(request, action, model_name, object_id=None, details=""):
    try:
        user = request.user if request and request.user.is_authenticated else None
        ip = get_client_ip(request)
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=str(object_id) if object_id else None,
            ip_address=ip,
            details=details
        )
    except Exception:
        pass
