import pytest
from django.test import TransactionTestCase
from django.urls import reverse


class ContactpageTests(TransactionTestCase):
    @pytest.mark.django_db()
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        assert response.status_code, 200

    def test_url_available_by_name(self):
        response = self.client.get(reverse("contact:contact"))
        assert response.status_code, 200

    def test_template_name_correct(self):
        response = self.client.get(reverse("contact:contact"))
        self.assertTemplateUsed(response, "contact/contact.html")

    def test_template_content(self):
        response = self.client.get(reverse("contact:contact"))
        self.assertContains(response, "Contact Form")
        self.assertNotContains(response, "Not on the page")
