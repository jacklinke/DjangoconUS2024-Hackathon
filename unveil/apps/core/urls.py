"""URLs for the unveil core app."""

from django.urls import path
from django.contrib.auth.models import User
from ninja import NinjaAPI
from core.models import Artwork, Comment, Profile
from ninja.files import UploadedFile

urlpatterns = [
]

api = NinjaAPI()


#TODO Look up how to properly integrate the Profile model into this endpoint
@api.post("/upload_image")
def upload_image(request, image: UploadedFile, title: str, content: str, orientation: str):
    user = request.user
    profile = user.profile
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    # Assuming you have a model called Artwork with fields: user, image, title, content, orientation, and profile
    artwork = Artwork(user=user, image=image, title=title, content=content, orientation=orientation, profile=profile)
    artwork.save()

    return {"success": True, "artwork_id": artwork.id}


@api.get("/post_comment")
def post_comment(request, artwork_id: int, comment: str):
    user = request.user
    profile = user.profile
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}
    else:
        artwork = Artwork.objects.get(id=artwork_id)
        comment = Comment(user=user, artwork=artwork, comment=comment, profile=profile)
        comment.save()
        return {"success": True, "comment_id": comment.id}

@api.get("/like_artwork")
def like_artwork(request, artwork_id: int):
    user = request.user
    profile = user.profile
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}
    else:
        artwork = Artwork.objects.get(id=artwork_id)
        artwork.like(user)
        return {"success": True}

@api.get("/dislike_artwork")
def dislike_artwork(request, artwork_id: int):
    user = request.user
    profile = user.profile
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}
    else:
        artwork = Artwork.objects.get(id=artwork_id)
        artwork.dislike(user)
        return {"success": True}


@api.get("/get_follower_count")
def get_follower_count(request, profile_id: int):
    profile = Profile.objects.get(id=profile_id)
    return {"success": True, "follower_count": profile.get_followers_count()}

@api.get("/get_following_count")
def get_following_count(request, profile_id: int):
    profile = Profile.objects.get(id=profile_id)
    return {"success": True, "following_count": profile.get_following_count()}

@api.get("/get_likes_count")
def get_likes_count(request, artwork_id: int):
    artwork = Artwork.objects.get(id=artwork_id)
    return {"success": True, "likes_count": artwork.get_likes_count()}  

@api.get("/get_dislikes_count")
def get_dislikes_count(request, artwork_id: int):
    artwork = Artwork.objects.get(id=artwork_id)
    return {"success": True, "dislikes_count": artwork.get_dislikes_count()}

@api.get('/get_comments')
def get_comments(request, artwork_id: int):
    artwork = Artwork.objects.get(id=artwork_id)
    return {"success": True, "comments": artwork.get_comments()}

@api.get("/get_views_count")
def get_views_count(request, artwork_id: int):
    artwork = Artwork.objects.get(id=artwork_id)
    return {"success": True, "views_count": artwork.get_views_count()}




