from django.contrib import admin
from .models import Tag, Project, ProjectImage, Post, Testimonial, ContactSubmission

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "featured", "published_at")
    list_filter = ("featured", "published_at", "tags")
    search_fields = ("title", "excerpt", "content")
    inlines = [ProjectImageInline]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "published", "published_at")
    list_filter = ("published", "published_at", "tags")
    search_fields = ("title", "excerpt", "body")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "rating", "created_at")
    search_fields = ("author_name", "content")

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("email", "ip_address", "created_at", "solved")
    list_filter = ("solved", "created_at")
    search_fields = ("email", "message")