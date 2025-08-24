from __future__ import annotations
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views.decorators.http import require_GET, require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import json
import logging
import urllib.parse
import urllib.request

from .models import Project, Post, Testimonial, ContactSubmission, Tag
from .forms import ContactForm

logger = logging.getLogger(__name__)

def home(request):
    featured_projects = Project.objects.filter(featured=True)[:6]
    latest_posts = Post.objects.filter(published=True)[:6]
    testimonials = Testimonial.objects.all()[:5]
    return render(request, "home.html", {
        "featured_projects": featured_projects,
        "latest_posts": latest_posts,
        "testimonials": testimonials,
    })

def project_list(request):
    tag_slug = request.GET.get("tag")
    qs = Project.objects.all()
    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        qs = qs.filter(tags=active_tag)
    tags = Tag.objects.filter(projects__isnull=False).distinct().order_by("name")
    return render(request, "projects/index.html", {"projects": qs, "tags": tags, "active_tag": active_tag})

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.exclude(id=project.id).filter(tags__in=project.tags.all()).distinct()[:3]
    return render(request, "projects/detail.html", {"project": project, "related": related})

def blog_index(request):
    q = (request.GET.get("q") or "").strip()
    qs = Post.objects.filter(published=True)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(body__icontains=q))
    tags = Tag.objects.filter(posts__isnull=False).distinct().order_by("name")
    return render(request, "blog/index.html", {"posts": qs, "q": q, "tags": tags})

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, "blog/detail.html", {"post": post})

def about(request):
    return render(request, "pages/about.html")

def resume(request):
    return render(request, "pages/resume.html")

def contact(request):
    form = ContactForm()
    return render(request, "pages/contact.html", {"form": form, "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY})

@require_POST
def contact_submit(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    # Rate limit: 3 submissions per hour per IP
    ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
    window_start = timezone.now() - timezone.timedelta(hours=1)
    recent_count = ContactSubmission.objects.filter(ip_address=ip, created_at__gte=window_start).count()
    if recent_count >= 3:
        return JsonResponse({"ok": False, "message": "Rate limit exceeded. Try again later."}, status=429)

    # Optional reCAPTCHA verification
    token = form.cleaned_data.get("recaptcha_token")
    if settings.RECAPTCHA_SECRET_KEY and token:
        try:
            data = urllib.parse.urlencode({
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": token,
                "remoteip": ip,
            }).encode()
            req = urllib.request.Request("https://www.google.com/recaptcha/api/siteverify", data=data)
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read().decode())
                if not result.get("success"):
                    return JsonResponse({"ok": False, "message": "reCAPTCHA failed."}, status=400)
        except Exception as e:
            logger.warning("reCAPTCHA verification error: %s", e)

    submission = ContactSubmission.objects.create(
        name=form.cleaned_data["name"],
        email=form.cleaned_data["email"],
        message=form.cleaned_data["message"],
        ip_address=ip,
    )

    subject = f"Portfolio contact from {submission.name}"
    body = f"Email: {submission.email}\nIP: {submission.ip_address}\n\n{submission.message}"
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL], fail_silently=True)
    except Exception as e:
        logger.warning("Email send failed: %s", e)

    return JsonResponse({"ok": True, "message": "Thanks! I’ll get back to you shortly."})

def search_page(request):
    q = (request.GET.get("q") or "").strip()
    projects = []
    if q:
        projects = Project.objects.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q))[:12]
        posts = Post.objects.filter(published=True).filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(body__icontains=q))[:12]
    else:
        posts = Post.objects.filter(published=True)[:12]
    return render(request, "blog/index.html", {"posts": posts, "q": q, "projects": projects})

@require_GET
def search_json(request):
    q = (request.GET.get("q") or "").strip()
    results = {"projects": [], "posts": []}
    if q:
        for p in Project.objects.filter(Q(title__icontains=q) | Q(excerpt__icontains=q))[:10]:
            results["projects"].append({
                "title": p.title,
                "url": p.get_absolute_url(),
                "excerpt": p.excerpt[:160],
                "cover": p.cover_image,
            })
        for b in Post.objects.filter(published=True).filter(Q(title__icontains=q) | Q(excerpt__icontains=q))[:10]:
            results["posts"].append({
                "title": b.title,
                "url": b.get_absolute_url(),
                "excerpt": b.excerpt[:160],
                "readingTime": b.reading_time_minutes,
            })
    return JsonResponse(results)

def privacy(request):
    return render(request, "pages/privacy.html")

def terms(request):
    return render(request, "pages/terms.html")

def health(request):
    return HttpResponse("ok")

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: /sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")