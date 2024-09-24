from django.test import TestCase
from django.urls import reverse


class AboutPageTests(TestCase):
    def setUp(self):
        url = reverse("index")
        self.response = self.client.get(url)

    def test_page_status_code(self):
        assert self.response.status_code, 200

    def test_page_template(self):
        self.assertTemplateUsed(self.response, "articles/list.html")

    def test_page_contains_correct_html(self):
        self.assertContains(self.response, '<div class="col-9 col-md-10">')

    def test_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")
