"""URLs for the unveil core app."""

from typing import Optional

from apps.core.models import Artwork, Comment, Follow, Profile, Sentiment, View
from ninja import Router
from ninja.files import UploadedFile

urlpatterns = []

router = Router()


@router.post("/artwork/create")
def upload_image(request, image: UploadedFile, title: str, content: str, orientation: str):
    """Upload an artwork to the server."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    profile = user.profile

    artwork = Artwork(user=user, image=image, title=title, content=content, orientation=orientation, profile=profile)
    artwork.save()

    return {"success": True, "artwork_uuid": artwork.uuid}


@router.get("/artwork/get")
def get_single_artwork(request, artwork_uuid: str):
    """Get an artwork by ID."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        artwork = Artwork.objects.get(uuid=artwork_uuid)
    except Artwork.DoesNotExist:
        return {"success": False, "error": "Artwork does not exist"}

    # If the artwork is not owned by the user and has already been viewed by the user, return an error.
    if not artwork.profile == user.profile and artwork.viewed_by.all().filter(profile=user.profile).exists():
        return {"success": False, "error": "Artwork already viewed"}

    # Artwork exists, and is either owned by the user or has not been viewed by the user.
    return {"success": True, "artwork": artwork}


@router.get("/artwork/random")
def get_random_artwork(request, limit: Optional[int] = 5):
    """Get random artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    artwork = Artwork.objects.get_random_artwork_for_profile(profile=user.profile, limit=limit)

    return {"success": True, "artwork": list(artwork)}


@router.get("/artwork/ordered")
def get_ordered_artwork(request, start: Optional[int] = 0, limit: Optional[int] = 5):
    """Get ordered artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    artwork = Artwork.objects.get_ordered_artwork_for_profile(profile=user.profile, start=start, limit=limit)

    return {"success": True, "artwork": list(artwork)}


@router.post("/artwork/comments/create")
def post_comment(request, artwork_uuid: str, body: str):
    """Post a comment on an artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    profile = user.profile

    try:
        artwork = Artwork.objects.get(uuid=artwork_uuid)
    except Artwork.DoesNotExist:
        return {"success": False, "error": "Artwork does not exist"}
    comment = Comment(profile=profile, artwork=artwork, body=body)
    comment.save()
    return {"success": True, "comment_uuid": comment.uuid}


@router.get("/artwork/comments/list")
def get_comments(request, artwork_uuid: str):
    """Get comments for an artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        artwork = Artwork.objects.get(uuid=artwork_uuid)
        comments = Comment.objects.filter(artwork=artwork)
    except Comment.DoesNotExist:
        return {"success": False, "error": "Artwork does not exist"}
    return {"success": True, "comments": list(comments)}


@router.get("/artwork/views")
def get_views(request, artwork_uuid: str):
    """Get the profiles that have viewed an artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        artwork = Artwork.objects.get(uuid=artwork_uuid)
    except Artwork.DoesNotExist:
        return {"success": False, "error": "Artwork does not exist"}
    views = View.objects.filter(artwork=artwork)
    return {"success": True, "views": list(views)}


@router.get("/artwork/views/count")
def get_views_count(request, artwork_uuid: str):
    """Get the number of views for an artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        artwork = Artwork.objects.get(uuid=artwork_uuid)
    except Artwork.DoesNotExist:
        return {"success": False, "error": "Artwork does not exist"}
    return {"success": True, "views_count": artwork.get_views_count()}


@router.post("/artwork/like")
def like_artwork(request, artwork_uuid: str):
    """Like an artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    artwork = Artwork.objects.get(uuid=artwork_uuid)
    Sentiment.objects.create(profile=user.profile, artwork=artwork, status=Sentiment.LikeChoices.LIKE)
    return {"success": True}


@router.post("/artwork/dislike")
def dislike_artwork(request, artwork_uuid: str):
    """Dislike an artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    artwork = Artwork.objects.get(uuid=artwork_uuid)
    Sentiment.objects.create(profile=user.profile, artwork=artwork, status=Sentiment.LikeChoices.DISLIKE)
    return {"success": True}


@router.get("/artwork/likes/count")
def get_likes_count(request, artwork_uuid: str):
    """Get the number of likes for an artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        artwork = Artwork.objects.get(uuid=artwork_uuid)
    except Artwork.DoesNotExist:
        return {"success": False, "error": "Artwork does not exist"}
    return {"success": True, "likes_count": artwork.get_likes_count()}


@router.get("/artwork/dislikes/count")
def get_dislikes_count(request, artwork_uuid: str):
    """Get the number of dislikes for an artwork."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        artwork = Artwork.objects.get(uuid=artwork_uuid)
    except Artwork.DoesNotExist:
        return {"success": False, "error": "Artwork does not exist"}
    return {"success": True, "dislikes_count": artwork.get_dislikes_count()}


@router.post("/profile/create")
def create_profile(request, name: str, bio: str):
    """Create a new profile."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    profile = Profile(user=user, name=name, bio=bio)
    profile.save()
    return {"success": True, "profile_uuid": profile.uuid}


@router.post("/profile/follow")
def follow_profile(request, profile_uuid: str):
    """Follow a profile."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        profile = Profile.objects.get(uuid=profile_uuid)
    except Profile.DoesNotExist:
        return {"success": False, "error": "Profile does not exist"}
    Follow.objects.create(following_profile=user.profile, followed_profile=profile)
    return {"success": True}


@router.post("/profile/unfollow")
def unfollow_profile(request, profile_uuid: str):
    """Unfollow a profile."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        profile = Profile.objects.get(uuid=profile_uuid)
    except Profile.DoesNotExist:
        return {"success": False, "error": "Profile does not exist"}
    Follow.objects.get(following_profile=user.profile, followed_profile=profile).delete()
    return {"success": True}


@router.get("/profile/follows/count")
def get_follower_count(request, profile_uuid: str):
    """Get the number of followers for a profile."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        profile = Profile.objects.get(uuid=profile_uuid)
    except Profile.DoesNotExist:
        return {"success": False, "error": "Profile does not exist"}
    return {"success": True, "follower_count": profile.get_followers_count()}


@router.get("/profile/following/count")
def get_following_count(request, profile_uuid: str):
    """Get the number of profiles a profile is following."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        profile = Profile.objects.get(uuid=profile_uuid)
    except Profile.DoesNotExist:
        return {"success": False, "error": "Profile does not exist"}
    return {"success": True, "following_count": profile.get_following_count()}


@router.get("/profile/following")
def get_following(request, profile_uuid: str):
    """Get the profiles that a profile is following."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        profile = Profile.objects.get(uuid=profile_uuid)
    except Profile.DoesNotExist:
        return {"success": False, "error": "Profile does not exist"}
    following = Follow.objects.filter(following_profile=profile)
    return {"success": True, "following": list(following)}


@router.get("/profile/followers")
def get_followers(request, profile_uuid: str):
    """Get the profiles that are following a profile."""
    user = request.user
    if not user.is_authenticated:
        return {"success": False, "error": "User not authenticated"}

    try:
        profile = Profile.objects.get(uuid=profile_uuid)
    except Profile.DoesNotExist:
        return {"success": False, "error": "Profile does not exist"}
    followers = Follow.objects.filter(followed_profile=profile)
    return {"success": True, "followers": list(followers)}
