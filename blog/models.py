from django.db import models
from django.utils import timezone #timezone is a module that provides a way to represent timezones
from django.contrib.auth.models import User #User is a model that represents a user
from django.urls import reverse


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250) # title of the post
    slug = models.SlugField(max_length=250, unique_for_date='publish') # slug of the post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') # author of the post
    body = models.TextField() # body of the post
    publish = models.DateTimeField(default=timezone.now) # publish date of the post
    created = models.DateTimeField(auto_now_add=True) # date the post was create
    updated = models.DateTimeField(auto_now=True) # date the post was update
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT) # status of the post
    objects = models.Manager() # manager for the post
    published = PublishManager()

    class Meta:
        ordering = ['-publish'] # order the post by publish date
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title # return the title of the post

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month,
                                                 self.publish.day, self.slug]) # return absolute url

