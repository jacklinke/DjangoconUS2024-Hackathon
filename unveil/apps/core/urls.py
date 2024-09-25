"""URLs for the unveil core app."""

from apps.core.models import Artwork, Comment, Follow, Profile, Sentiment, View
from django.contrib.auth.models import User
from django.urls import path
from ninja import NinjaAPI
from ninja.files import UploadedFile

urlpatterns = []

api = NinjaAPI()


@api.post("/artwork/upload")
def upload_image(request, image: UploadedFile, title: str, content: str, orientation: str):
    """Upload an artwork to the server."""
    user = request.user
    profile = user.profile
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    # Assuming you have a model called Artwork with fields: user, image, title, content, orientation, and profile
    artwork = Artwork(user=user, image=image, title=title, content=content, orientation=orientation, profile=profile)
    artwork.save()

    return {"success": True, "artwork_id": artwork.id}


@api.post("/artwork/comments/post")
def post_comment(request, artwork_id: int, comment: str):
    """Post a comment on an artwork."""
    user = request.user
    profile = user.profile
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}
    else:
        artwork = Artwork.objects.get(id=artwork_id)
        comment = Comment(user=user, artwork=artwork, comment=comment, profile=profile)
        comment.save()
        return {"success": True, "comment_id": comment.id}


@api.get("/artwork/comments/get")
def get_comments(request, artwork_id: int):
    """Get comments for an artwork."""
    comments = Comment.objects.filter(artwork_id=artwork_id)
    return {"success": True, "comments": comments}


@api.get("/artwork/like")
def like_artwork(request, artwork_id: int):
    """Like an artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}
    else:
        Sentiment.objects.create(profile=user.profile, artwork_id=artwork_id, status=Sentiment.LikeChoices.LIKE)
        return {"success": True}


@api.get("/artwork/dislike")
def dislike_artwork(request, artwork_id: int):
    """Dislike an artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}
    else:
        Sentiment.objects.create(profile=user.profile, artwork_id=artwork_id, status=Sentiment.LikeChoices.DISLIKE)
        return {"success": True}


@api.get("/profile/follows/count")
def get_follower_count(request, profile_id: int):
    """Get the number of followers for a profile."""
    profile = Profile.objects.get(id=profile_id)
    return {"success": True, "follower_count": profile.get_followers_count()}


@api.get("/profile/following/count")
def get_following_count(request, profile_id: int):
    """Get the number of profiles a profile is following."""
    profile = Profile.objects.get(id=profile_id)
    return {"success": True, "following_count": profile.get_following_count()}


@api.get("/profile/follow")
def follow_profile(request, profile_id: int):
    """Follow a profile."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}
    else:
        profile = Profile.objects.get(id=profile_id)
        Follow.objects.create(following_profile=user.profile, followed_profile=profile)
        return {"success": True}


@api.get("/profile/unfollow")
def unfollow_profile(request, profile_id: int):
    """Unfollow a profile."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}
    else:
        profile = Profile.objects.get(id=profile_id)
        Follow.objects.get(following_profile=user.profile, followed_profile=profile).delete()
        return {"success": True}


@api.get("/profile/following")
def get_following(request, profile_id: int):
    """Get the profiles that a profile is following."""
    profile = Profile.objects.get(id=profile_id)
    following = Follow.objects.filter(following_profile=profile)
    return {"success": True, "following": following}


@api.get("/profile/followers")
def get_followers(request, profile_id: int):
    """Get the profiles that are following a profile."""
    profile = Profile.objects.get(id=profile_id)
    followers = Follow.objects.filter(followed_profile=profile)
    return {"success": True, "followers": followers}


@api.get("/artwork/views")
def get_views(request, artwork_id: int):
    """Get the profiles that have viewed an artwork."""
    artwork = Artwork.objects.get(id=artwork_id)
    views = View.objects.filter(artwork=artwork)
    return {"success": True, "views": views}


@api.get("/artwork/likes/count")
def get_likes_count(request, artwork_id: int):
    """Get the number of likes for an artwork."""
    artwork = Artwork.objects.get(id=artwork_id)
    return {"success": True, "likes_count": artwork.get_likes_count()}


@api.get("/artwork/dislikes/count")
def get_dislikes_count(request, artwork_id: int):
    """Get the number of dislikes for an artwork."""
    artwork = Artwork.objects.get(id=artwork_id)
    return {"success": True, "dislikes_count": artwork.get_dislikes_count()}


@api.get("/artwork/views/count")
def get_views_count(request, artwork_id: int):
    """Get the number of views for an artwork."""
    artwork = Artwork.objects.get(id=artwork_id)
    return {"success": True, "views_count": artwork.get_views_count()}
