from __future__ import annotations
from django.db import models
from django.urls import reverse
from django.utils import timezone
import math

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=64, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, max_length=160)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    cover_image = models.CharField(max_length=255, blank=True, help_text="Path under static/")
    featured = models.BooleanField(default=False)
    roles = models.CharField(max_length=140, blank=True, help_text="e.g., Developer, Designer")
    tools = models.CharField(max_length=200, blank=True, help_text="Comma-separated tools")
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-published_at"]
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["-published_at"])]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("portfolio:project_detail", args=[self.slug])

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image_url = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=140, blank=True)

    class Meta:
        ordering = ["id"]

class Post(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, max_length=160)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-published_at"]
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["-published_at"])]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("portfolio:post_detail", args=[self.slug])

    @property
    def reading_time_minutes(self) -> int:
        words = len(self.body.split())
        return max(1, math.ceil(words / 200))

class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(max_length=140, blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.author_name} ({self.rating}/5)"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    solved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["ip_address", "-created_at"])]

    def __str__(self) -> str:
        return f"{self.email} @ {self.created_at:%Y-%m-%d %H:%M}"