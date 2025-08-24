from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from portfolio.sitemaps import ProjectSitemap, PostSitemap, StaticViewSitemap
from portfolio.views import robots_txt

sitemaps = {
    "projects": ProjectSitemap,
    "posts": PostSitemap,
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("portfolio.urls", namespace="portfolio")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]