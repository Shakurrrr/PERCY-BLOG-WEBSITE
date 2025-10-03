# blog/views_auth.py
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

COOKIE_SECURE   = not settings.DEBUG
COOKIE_SAMESITE = "Lax"      # use "None" only if cross-site + HTTPS
ACCESS_MAX_AGE  = 60 * 60 * 24
REFRESH_MAX_AGE = 60 * 60 * 24 * 7

class CookieLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access  = refresh.access_token

        resp = Response({"detail": "ok"})
        resp.set_cookie("access_token", str(access),
                        max_age=ACCESS_MAX_AGE, httponly=True, secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE)
        resp.set_cookie("refresh_token", str(refresh),
                        max_age=REFRESH_MAX_AGE, httponly=True, secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE)
        return resp

class CookieLogout(APIView):
    def post(self, request):
        resp = Response({"detail": "logged out"})
        resp.delete_cookie("access_token")
        resp.delete_cookie("refresh_token")
        return resp
