from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from orders.models import Order


class HistorySecurityTest(TestCase):
    def test_history_and_download_are_limited_to_current_user(self):
        user_model = get_user_model()
        first_user = user_model.objects.create_user("first@example.com", "Password123!safe")
        second_user = user_model.objects.create_user("second@example.com", "Password123!safe")
        first_order = Order.objects.create(
            user=first_user,
            activity="Première activité",
            status=Order.Status.GENEREE,
            generated_file_name="first.xlsx",
        )
        second_order = Order.objects.create(
            user=second_user,
            activity="Deuxième activité",
            status=Order.Status.GENEREE,
            generated_file_name="second.xlsx",
        )

        self.client.force_login(first_user)
        response = self.client.get(reverse("history"))
        content = response.content.decode()
        self.assertContains(response, first_order.activity)
        self.assertNotContains(response, second_order.activity)

        download_response = self.client.get(
            reverse("download_generated_excel", args=[second_order.generated_file_name])
        )
        self.assertRedirects(download_response, reverse("history"))
