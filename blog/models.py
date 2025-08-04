from django.db import models
from django.utils import timezone
# from django.db.models.functions import Now
from django.conf import settings

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB' , 'Published'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , related_name ="blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    # publish = models.DateTimeField(db_default=Now())  ==>> moadel balaii ba in tafavot k az function khode data base estefade mikone
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2 , choices = Status , default = Status.DRAFT)


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
        return self.title