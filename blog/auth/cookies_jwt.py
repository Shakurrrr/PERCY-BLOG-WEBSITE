# auth/cookie_jwt.py
from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw = request.COOKIES.get("access_token")
        if raw:
            validated = self.get_validated_token(raw)
            return (self.get_user(validated), validated)
        return None
