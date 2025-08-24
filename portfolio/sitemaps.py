from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, Post

class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.published_at

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.published_at

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ["portfolio:home", "portfolio:projects", "portfolio:blog", "portfolio:about", "portfolio:resume", "portfolio:contact", "portfolio:privacy", "portfolio:terms"]

    def location(self, item):
        return reverse(item)