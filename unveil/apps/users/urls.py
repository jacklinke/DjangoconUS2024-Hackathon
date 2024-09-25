"""URLs for the unveil users app."""

from django.contrib.auth.models import User
from django.urls import path
from ninja import Router
from ninja.security import django_auth

urlpatterns = []

router = Router()


@router.get("/account/create")
def create_account(request, given_username: str, given_password: str, given_email: str):
    """Create a new user account."""
    User.objects.create_user(username=given_username, password=given_password, email=given_email)
    return {"success": True}


@router.get("/account/test", auth=django_auth)
def test_user(request):
    """Test the authenticated user."""
    return f"Authenticated user {request.auth}"
