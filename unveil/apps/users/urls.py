"""URLs for the unveil users app."""

from django.contrib.auth.models import User
from django.urls import path
from ninja import Router

urlpatterns = []

router = Router()


@router.get("/create_account")
def create_account(request, given_username: str, given_password: str, given_email: str):
    """Create a new user account."""
    User.objects.create_user(username=given_username, password=given_password, email=given_email)
    return {"success": True}
