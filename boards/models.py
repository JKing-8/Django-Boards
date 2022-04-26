import math
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.html import mark_safe
from django.utils.text import Truncator
from markdown import markdown


class Board(models.Model):
    name = models.CharField(max_length=20, unique=True)
    descript = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_by').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255, default=None)
    last_update = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE, default='')
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE, default='')
    views = models.PositiveIntegerField(default=0)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        page = count / 20
        return math.ceil(page)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, default=timezone.now)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    update_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.DO_NOTHING)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
