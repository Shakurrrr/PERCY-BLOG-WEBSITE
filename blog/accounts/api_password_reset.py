# accounts/api_password_reset.py
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

User = get_user_model()
token_gen = PasswordResetTokenGenerator()

# --- serializers ---
class PasswordResetRequestSer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)

# --- views ---
class PasswordResetRequest(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = PasswordResetRequestSer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"]

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # don’t leak which emails exist
            return Response({"detail": "If that account exists, a reset mail was sent."})

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_gen.make_token(user)

        # dev: print a link; prod: send a real email with your frontend URL
        reset_url = f"{request.scheme}://{request.get_host()}/reset?uid={uid}&token={token}"
        send_mail(
            subject="Password reset",
            message=f"Reset your password: {reset_url}",
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[email],
            fail_silently=True,
        )
        return Response({"detail": "If that account exists, a reset mail was sent.",
                         "dev_reset_url": reset_url})  # remove in prod

class PasswordResetConfirm(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = PasswordResetConfirmSer(data=request.data)
        ser.is_valid(raise_exception=True)
        uid, token, new_pw = ser.validated_data.values()

        try:
            uid_int = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_int)
        except Exception:
            return Response({"detail": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if not token_gen.check_token(user, token):
            return Response({"detail": "Invalid or expired token"}, status=400)

        user.set_password(new_pw)
        user.save()
        return Response({"detail": "Password updated"})
