"""Models for the unveil core app."""

import uuid
from random import randint

from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Model for user profiles."""

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    account = models.OneToOneField(
        "users.UserAccount", on_delete=models.CASCADE, primary_key=True, related_name="profile"
    )

    class ProfileType(models.TextChoices):
        """Choices for the type of profile."""

        ARTIST = "ART", _("Artist")
        AUDIENCE = "AUD", _("Audience")
        BOTH = "BOT", _("Both")

    profile_type = models.CharField(
        max_length=3,
        choices=ProfileType.choices,
        default=ProfileType.AUDIENCE,
    )

    profile_picture = models.ImageField(upload_to="profiles", blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    websites = models.JSONField(default=dict, help_text=_("Websites associated with the user."), blank=True)

    following = models.ManyToManyField("self", through="Follow", symmetrical=False, related_name="followed")

    sentiment = models.ManyToManyField("core.Artwork", through="Sentiment", related_name="sentiment_by")
    comments = models.ManyToManyField("core.Artwork", through="Comment", related_name="commented_by")
    views = models.ManyToManyField("core.Artwork", through="View", related_name="viewed_by")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class for the Profile model."""

        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.account.email

    def get_following_count(self):
        """Get the number of profiles that the profile is following."""
        return self.following.count()

    def get_followers_count(self):
        """Get the number of profiles that are following the profile."""
        return self.followed.count()

    def get_likes_count(self):
        """Get the number of likes that the profile has given."""
        return self.sentiment.filter(status=Sentiment.LikeChoices.LIKE).count()

    def get_dislikes_count(self):
        """Get the number of dislikes that the profile has given."""
        return self.sentiment.filter(status=Sentiment.LikeChoices.DISLIKE).count()


class Follow(models.Model):
    """A Through-Model for following relationships."""

    following_profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE, related_name="follow_by")
    followed_profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE, related_name="follow_to")

    created_at = models.DateTimeField(auto_now_add=True)

    is_favorite = models.BooleanField(default=False)

    class Meta:
        """Meta class for the Follow model."""

        verbose_name = "Follow"
        verbose_name_plural = "Follows"

        constraints = [
            models.UniqueConstraint(fields=["following_profile", "followed_profile"], name="unique_following")
        ]

    def __str__(self):
        return f"{self.following_profile} follows {self.followed_profile}"


class Sentiment(models.Model):
    """A Through-Model for sentiment about an artwork.

    If a profile likes an artwork, a Sentiment object is created with the status as Like.
    If a profile dislikes an artwork, a Sentiment object is created with the status as Dislike.
    If there is no sentiment, the profile has not interacted with the artwork.
    """

    profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE, related_name="profile_sentiment")
    artwork = models.ForeignKey("core.Artwork", on_delete=models.CASCADE, related_name="artwork_sentiment")

    class LikeChoices(models.TextChoices):
        """Choices for the like status."""

        LIKE = "LIK", _("Like")
        DISLIKE = "DIS", _("Dislike")

    status = models.CharField(
        max_length=3,
        choices=LikeChoices.choices,
        default=LikeChoices.LIKE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for the Sentiment model."""

        verbose_name = "Sentiment"
        verbose_name_plural = "Sentiments"

        constraints = [models.UniqueConstraint(fields=["profile", "artwork"], name="unique_sentiment")]

    def __str__(self):
        if self.status == self.LikeChoices.LIKE:
            return f"{self.profile} liked {self.artwork}"
        return f"{self.profile} disliked {self.artwork}"


class Comment(models.Model):
    """A Through-Model for non-threaded comments."""

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE, help_text=_("The profile of the commenter."))
    artwork = models.ForeignKey("core.Artwork", on_delete=models.CASCADE)

    body = models.TextField()

    is_censored = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class for the Comment model."""

        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"])]

    def __str__(self):
        return f"{self.profile} commented on {self.artwork}"


class View(models.Model):
    """A Through-Model for views of artworks."""

    profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE)
    artwork = models.ForeignKey("core.Artwork", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for the View model."""

        constraints = [models.UniqueConstraint(fields=["profile", "artwork"], name="unique_view")]
        verbose_name = "View"
        verbose_name_plural = "Views"

    def __str__(self):
        return f"{self.profile} viewed {self.artwork}"


class ArtworkQuerySet(models.QuerySet):
    """Custom QuerySet for the Artwork model."""

    def get_random_artwork_for_profile(self, profile, limit=5):
        """Get a random artwork that the profile has not viewed.

        Usage:

        ```python
        profile = Profile.objects.get(pk=1)
        # or
        profile = request.user.profile

        artwork = Artwork.objects.get_random_for_profile(profile, limit=5)
        ```
        """
        max_id = self.all().aggregate(max_id=Max("id"))["max_id"] or 1
        print(f"Max ID: {max_id}")
        artwork_list = []
        run_count = 0
        while True:
            run_count += 1
            pk = randint(1, max_id)
            artwork = self.filter(pk=pk).filter(viewed_by=profile).first()
            if artwork:
                artwork_list.append(artwork)
            # Break if the loop runs for too long (e.g. all artworks have been viewed) or if the limit is reached
            if run_count == limit * 3 or len(artwork_list) == limit:
                break
        return artwork_list

    def get_ordered_artwork_for_profile(self, profile, start=0, limit=5):
        """Get unseen artworks for the profile in chronological order.

        Usage:

        ```python
        profile = Profile.objects.get(pk=1)
        # or
        profile = request.user.profile

        artworks = Artwork.objects.get_artwork_for_profile(profile, start=0, limit=5)
        ```
        """
        return self.exclude(viewed_by=profile)[start : start + limit]

    def get_popular(self):
        """Get the most popular artworks."""
        return self.annotate(like_count=models.Count("liked_by")).order_by("-like_count")

    def get_recent(self, limit=5):
        """Get the most recent artworks."""
        return self.order_by("-created_at")[:limit]


class Artwork(models.Model):
    """Model for artwork."""

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    class Orientation(models.TextChoices):
        """Choices for the orientation of the artwork."""

        PORTRAIT = "POR", _("Portrait")
        LANDSCAPE = "LAN", _("Landscape")
        SQUARE = "SQU", _("Square")
        NOT_SPECIFIED = "NSP", _("Not Specified")

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, help_text=_("The profile of the artist."))

    title = models.CharField(max_length=30)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images")
    orientation = models.CharField(
        max_length=3,
        choices=Orientation.choices,
        default=Orientation.NOT_SPECIFIED,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = ArtworkQuerySet.as_manager()

    class Meta:
        """Meta class for the Artwork model."""

        verbose_name = "Artwork"
        verbose_name_plural = "Artworks"
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["profile", "title"], name="unique_artwork")]

    def __str__(self):
        return self.title

    def get_like_count(self):
        """Get the number of likes for the artwork."""
        return self.sentiment_by.filter(status=Sentiment.LikeChoices.LIKE).count()

    def get_dislike_count(self):
        """Get the number of dislikes for the artwork."""
        return self.sentiment_by.filter(status=Sentiment.LikeChoices.DISLIKE).count()

    def get_comment_count(self):
        """Get the number of comments for the artwork."""
        return self.commented_by.count()

    def get_view_count(self):
        """Get the number of views for the artwork."""
        return self.viewed_by.count()

    def get_comment(self):
        """Get the comments for the artwork."""
        return self.commented_by.all()
