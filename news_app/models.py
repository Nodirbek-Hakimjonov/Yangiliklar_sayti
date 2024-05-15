from django.contrib.auth.models import User
from django.db import models
# from .managers import PublishedManager
# Create your models here.
from django.urls import reverse
from django.utils import timezone
from hitcount.models import HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation


class PublishedManager(models.Manager):
    def get_queryset(self):
         return super().get_queryset().filter(status=News.Status.Published)

class Category(models.Model):
    name=models.CharField(max_length=150)
    def __str__(self):
        return self.name


class News(models.Model):
    class Status(models.TextChoices):
        Draft= "DF","Draft"
        Published="PB", "Published"
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250)
    body=models.TextField()
    image=models.ImageField(upload_to='news/images')
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    publish_time=models.DateTimeField(default=timezone.now)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2,
                            choices=Status.choices,
                            default=Status.Draft)
    objects=models.Manager()
    published=PublishedManager()

    @property
    def get_hit_count(self):
        return HitCount.objects.filter(post=self).count()

    class Meta:
        ordering=["-publish_time"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail_page', args=[self.slug])

class HitCount(models.Model):
    ip_address = models.GenericIPAddressField()
    post = models.ForeignKey("News", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ip_address} => {self.post.title}'

class Contact(models.Model):
    name=models.CharField(max_length=150)
    email=models.EmailField(max_length=150)
    message=models.TextField()

    def __str__(self):
        return self.email

class Comment(models.Model):
    news=models.ForeignKey(News,on_delete=models.CASCADE,
                           related_name='comments')
    user=models.ForeignKey(User,on_delete=models.CASCADE,
                           related_name='comments')
    body=models.TextField()
    created_time=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=['-created_time']

    def __str__(self):
        return f"Comment - {self.body} by {self.user}"
