"""Models for the unveil core app."""

from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    account_id = models.CharField(max_length=30, primary_key=True)
    account_creation_date = models.DateTimeField(auto_now_add=True)
    account_last_modified_date = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(upload_to='profile_pictures')


class ArtPost(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=30, primary_key=True)
    post_creation_date = models.DateTimeField(auto_now_add=True)
    post_last_modified_date = models.DateTimeField(auto_now=True)
    post_content = models.TextField()
    post_image = models.ImageField(upload_to='post_images')
    post_title = models.CharField(max_length=30)
    seen_by_user = models.ArrayField(models.CharField(max_length=30))
    likes = models.ArrayField(models.CharField(max_length=30))
    dislikes = models.ArrayField(models.CharField(max_length=30))
    comments = models.ArrayField(models.CharField(max_length=30))
    censored_comments = models.ArrayField(models.CharField(max_length=30))