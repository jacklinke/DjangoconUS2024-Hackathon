"""Models for the unveil core app."""

from random import randint

from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Model for user profiles."""

    class ProfileType(models.TextChoices):
        """Choices for the type of profile."""

        ARTIST = "ART", _("Artist")
        AUDIENCE = "AUD", _("Audience")
        BOTH = "BOT", _("Both")

    account = models.OneToOneField(
        "users.UserAccount", on_delete=models.CASCADE, primary_key=True, related_name="profile"
    )
    profile_type = models.CharField(
        max_length=3,
        choices=ProfileType.choices,
        default=ProfileType.AUDIENCE,
    )

    profile_picture = models.ImageField(upload_to="profiles")
    bio = models.TextField()
    location = models.CharField(max_length=30)
    websites = models.JSONField(default=dict, help_text=_("Websites associated with the user."))

    following = models.ManyToManyField("self", through="Follow", symmetrical=False, related_name="followed")

    likes = models.ManyToManyField("core.Artwork", through="Like", related_name="liked_by")
    dislikes = models.ManyToManyField("core.Artwork", through="Dislike", related_name="disliked_by")
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
        return self.likes.count()

    def get_dislikes_count(self):
        """Get the number of dislikes that the profile has given."""
        return self.dislikes.count()


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

        constraints = [models.UniqueConstraint(fields=["follower", "following"], name="unique_following")]

    def __str__(self):
        return f"{self.following_profile} follows {self.followed_profile}"


class Like(models.Model):
    """A Through-Model for likes."""

    profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE)
    artwork = models.ForeignKey("core.Artwork", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for the Like model."""

        verbose_name = "Like"
        verbose_name_plural = "Likes"

        constraints = [models.UniqueConstraint(fields=["profile", "artwork"], name="unique_like")]

    def __str__(self):
        return f"{self.profile} liked {self.artwork}"


class Dislike(models.Model):
    """A Through-Model for dislikes."""

    profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE)
    artwork = models.ForeignKey("core.Artwork", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for the Dislike model."""

        verbose_name = "Dislike"
        verbose_name_plural = "Dislikes"

        constraints = [models.UniqueConstraint(fields=["profile", "artwork"], name="unique_dislike")]

    def __str__(self):
        return f"{self.profile} disliked {self.artwork}"


class Comment(models.Model):
    """A Through-Model for non-threaded comments."""

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
        constraints = [models.UniqueConstraint(fields=["profile", "artwork", "comment"], name="unique_comment")]

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

    def get_random_for_profile(self, profile):
        """Get a random artwork that the profile has not viewed.

        Usage:

        ```python
        profile = Profile.objects.get(pk=1)
        artwork = Artwork.objects.get_random_for_profile(profile)
        ```
        """
        max_id = self.all().aggregate(max_id=Max("id"))["max_id"]
        while True:
            pk = randint(1, max_id)
            category = self.filter(pk=pk).filter(viewed_by=profile).first()
            if category:
                return category


class Artwork(models.Model):
    """Model for artwork."""

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
        return self.liked_by.count()

    def get_dislike_count(self):
        """Get the number of dislikes for the artwork."""
        return self.disliked_by.count()

    def get_comment_count(self):
        """Get the number of comments for the artwork."""
        return self.commented_by.count()

    def get_view_count(self):
        """Get the number of views for the artwork."""
        return self.viewed_by.count()

    def get_comment(self):
        """Get the comments for the artwork."""
        return self.commented_by.all()
