from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import Tag, Project, ProjectImage, Post, Testimonial
from django.db import transaction

class Command(BaseCommand):
    help = "Seed demo content (projects, posts, testimonials)"

    @transaction.atomic
    def handle(self, *args, **options):
        tags = ["Python", "Django", "UI/UX", "Accessibility", "Performance", "Security", "JavaScript"]
        tag_objs = {}
        for t in tags:
            tag_objs[t], _ = Tag.objects.get_or_create(name=t, defaults={"slug": t.lower()})

        # Projects
        Project.objects.all().delete()
        projects_data = [
            ("Campus Navigator App", "cover-1@2x.jpg"),
            ("AI Study Planner", "cover-2@2x.jpg"),
            ("Design System Kit", "cover-3@2x.jpg"),
            ("Portfolio Redesign", "cover-4@2x.jpg"),
            ("Open Source CLI", "cover-5@2x.jpg"),
            ("STEM Club Site", "cover-6@2x.jpg"),
        ]
        for idx, (title, cover) in enumerate(projects_data, start=1):
            p = Project.objects.create(
                title=title,
                slug=title.lower().replace(" ", "-"),
                excerpt="A premium case study of impact, craft, and results.",
                content="Challenge, solution, and measurable outcomes. Beautifully documented.",
                cover_image=f"portfolio/img/placeholders/{cover}",
                featured=idx <= 3,
                roles="Developer, Designer",
                tools="Django, Tailwind, JS",
                published_at=timezone.now() - timezone.timedelta(days=idx * 7),
            )
            p.tags.add(tag_objs["Django"], tag_objs["UI/UX"], tag_objs["Performance"])
            ProjectImage.objects.create(project=p, image_url=f"portfolio/img/placeholders/{cover}", alt_text=title)

        # Posts
        Post.objects.all().delete()
        posts = [
            "How I Built a Blazing Fast Portfolio",
            "Designing for Accessibility at 17",
            "Django Tips: Clean Settings & Security",
            "Client-side Search with Server Fallback",
            "Microinteractions with IntersectionObserver",
            "Launching on a Budget: Performance First",
        ]
        for idx, title in enumerate(posts, start=1):
            post = Post.objects.create(
                title=title,
                slug=title.lower().replace(" ", "-"),
                excerpt="Thoughts on building great software and design.",
                body=" ".join(["Quality work demands clarity and care."] * (200 + idx * 50)),
                published=True,
                published_at=timezone.now() - timezone.timedelta(days=idx * 5),
            )
            post.tags.add(tag_objs["Python"], tag_objs["Django"], tag_objs["Performance"])

        # Testimonials
        Testimonial.objects.all().delete()
        testimonials = [
            ("Alex P.", "Startup Founder", 5, "Delivered beyond expectations, fast and polished."),
            ("Jamie L.", "Teacher", 5, "Professional, proactive, and very talented."),
            ("Chris D.", "Mentor", 5, "A rare blend of design and engineering skills."),
            ("Taylor S.", "Teammate", 4, "Great communicator and team player."),
            ("Morgan K.", "Client", 5, "Premium results with exceptional attention to detail."),
        ]
        for name, role, rating, content in testimonials:
            Testimonial.objects.create(author_name=name, author_role=role, rating=rating, content=content)

        self.stdout.write(self.style.SUCCESS("Demo content seeded."))