"""URLs for the unveil users app."""

from django.urls import path
from ninja import NinjaAPI
from django.contrib.auth.models import User

urlpatterns = []

api = NinjaAPI()


@api.get("/create_account")
def create_account(request, given_username: str, given_password: str, given_email: str):
    user = User.objects.create_user(username=given_username, password=given_password, email=given_email)
    return {"success": True}
