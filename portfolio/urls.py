from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.project_list, name="projects"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("blog/", views.blog_index, name="blog"),
    path("blog/<str:slug>/", views.blog_detail, name="post_detail"),
    path("about/", views.about, name="about"),
    path("resume/", views.resume, name="resume"),
    path("contact/", views.contact, name="contact"),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("search/", views.search_page, name="search_page"),
    path("search.json", views.search_json, name="search_json"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("health/", views.health, name="health"),
]