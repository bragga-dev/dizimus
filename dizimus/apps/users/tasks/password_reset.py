"""
Tasks Celery — redefinição de senha.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email(self, user_id: str, uid: str, token: str) -> None:
    from dizimus.apps.users.models import User
    try:
        user = User.objects.get(pk=user_id)
        reset_url = f"{settings.FRONTEND_URL}/redefinir-senha/{uid}/{token}/"

        send_mail(
            subject="Redefinição de senha — DIZIMUS",
            message=(
                f"Olá, {user.first_name}!\n\n"
                f"Clique no link para redefinir sua senha:\n{reset_url}\n\n"
                "O link expira em 1 hora. Se não foi você, ignore este e-mail."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc)