"""URLs for the unveil users app."""

from apps.users.models import UserAccount
from django.urls import path
from ninja import Router
from ninja.security import django_auth
from ninja.security import HttpBearer
from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime, timedelta
import jwt

urlpatterns = []

router = Router()


@router.get("/account/create")
def create_account(request, given_name: str, given_password: str, given_email: str):
    """Create a new user account."""
    UserAccount.objects.create_user(name=given_name, password=given_password, email=given_email)
    return {"success": True}


@router.get("/account/test", auth=django_auth)
def test_user(request):
    """Test the authenticated user."""
    return f"Authenticated user {request.auth}"

def create_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            if user_id:
                return user_id
        except jwt.PyJWTError:
            pass
        return None

auth = AuthBearer()

@router.post("/login")
def login(request, username: str, password: str):
    user = authenticate(username=username, password=password)
    if user is not None:
        token = create_token(user)
        return {"token": token}
    return {"error": "Invalid credentials"}