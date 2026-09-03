from .models import AuditLog


def create_audit_log(
    request,
    action,
    object_type,
    object_id,
    details=None
):
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        object_type=object_type,
        object_id=str(object_id),
        details=details or {},
        ip_address=request.META.get('REMOTE_ADDR')
    )
