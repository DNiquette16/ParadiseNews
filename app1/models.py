from django.db import models
from django.contrib.auth.models import User as AuthUser

# Create your models here.


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
# Feel free to rename the models, but don't rename db_table values or field names.
# Connecting PostgreSQL to Django
class Users(models.Model):
    email = models.TextField()
    password = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'users'

class Posts(models.Model):
    source = models.TextField()
    title = models.TextField()
    description = models.TextField()
    author = models.TextField()
    datetime = models.DateTimeField()
    image = models.TextField(blank=True, null=True)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    link = models.TextField()
    category = models.TextField()

    class Meta:
        managed = False
        db_table = 'posts'

class Likes(models.Model):
    #user = models.ForeignKey('Users', on_delete=models.CASCADE)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    like = models.ForeignKey('Posts', related_name='like_id', on_delete=models.CASCADE, blank=True, null=True)
    dislike = models.ForeignKey('Posts', related_name='dislike_id', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'likes'