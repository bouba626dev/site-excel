from pathlib import Path

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from orders.models import Order, Specification


class ChatGenerationFlowTest(TestCase):
    def test_post_creates_order_spec_and_excel_and_show_download_link(self):
        payload = {"user_text": "Je veux créer une boutique de vêtements"}

        with patch("core.views.generate_specification", return_value={
            "activity": "boutique de vêtements",
            "excel": {"sheets": ["Produits", "Ventes", "Dépenses", "Dashboard"]},
        }):
            response = self.client.post(reverse("home"), payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [(reverse("generation_result"), 302)])
        self.assertEqual(Order.objects.count(), 0)

        signup_response = self.client.post(reverse("signup"), {
            "email": "client@example.com",
            "password1": "UnMotDePasseSolide123!",
            "password2": "UnMotDePasseSolide123!",
        }, follow=True)
        self.assertEqual(signup_response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.activity, payload["user_text"])
        self.assertEqual(order.user.email, "client@example.com")
        self.assertEqual(order.status, Order.Status.EN_ATTENTE_PAIEMENT)

        specification = Specification.objects.get(order=order)
        self.assertEqual(specification.content["activity"], "boutique de vêtements")
        self.assertIn("Produits", specification.content["excel"]["sheets"])

        confirm_response = self.client.post(reverse("confirm_payment"), {}, follow=True)
        self.assertEqual(confirm_response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.GENEREE)
        generated_file_name = confirm_response.context["generated_file_name"]
        self.assertTrue((Path("media/generated_files") / generated_file_name).exists())
        self.assertIn("télécharger le fichier excel", confirm_response.content.decode("utf-8").lower())
