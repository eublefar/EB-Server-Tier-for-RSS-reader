from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Source(models.Model):
    source_name = models.CharField(max_length=200)
    source_address = models.CharField(max_length=600)
    is_public = models.BooleanField()
    modified = models.DateField(default = None, null=True)
    def __str__(self):
        return self.source_name

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    def __str__(self):
        return self.category_name

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.event_name

class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    article_name = models.CharField(max_length=600)
    article_address = models.CharField(max_length=600)
    pub_date = models.DateTimeField('date published')
    is_public = models.BooleanField()
    article_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    article_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.article_name

class User_source(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #TODO:Ustawienia uzytkownika
    def __str__(self):
          return "%s's profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
