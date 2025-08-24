from django.test import TestCase
from django.urls import reverse

class ContactFormTests(TestCase):
    def test_contact_post_rate_limit(self):
        url = reverse("portfolio:contact_submit")
        for _ in range(3):
            r = self.client.post(url, {"name": "A", "email": "a@example.com", "message": "Hello"}, follow=True)
            self.assertEqual(r.status_code, 200)
        r = self.client.post(url, {"name": "A", "email": "a@example.com", "message": "Hello again"})
        self.assertEqual(r.status_code, 429)