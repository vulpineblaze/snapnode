from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Node(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True)
    name = models.CharField(max_length=160)
    desc = models.TextField(max_length=1600)
    date_created = models.DateTimeField('date created',auto_now_add=True)
    date_updated = models.DateTimeField('date updated',auto_now=True)
    def __unicode__(self):              # __unicode__ on Python 2
        return str(self.name)


<<<<<<< HEAD
class Glue(models.Model):
    parent = models.ForeignKey("parent")
    child = models.ForeignKey("child")
    name = models.CharField(max_length=160)
    date_created = models.DateTimeField('date created',auto_now_add=True)
    date_updated = models.DateTimeField('date updated',auto_now=True)
    def __unicode__(self):              # __unicode__ on Python 2
        return str(self.name)
=======
>>>>>>> 9ffd7e2b0eb73d2d5ab19ad634beddf7c840cbb8

  
  
  
 
class UserProfile(models.Model):
    """ UserProfile model in a OneToOneField with User so that addl fields can be attached to Users (aka. picutre) """
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username