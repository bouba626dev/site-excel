from pathlib import Path

from django.test import TestCase
from django.urls import reverse

from orders.models import Order, Specification


class ChatGenerationFlowTest(TestCase):
    def test_post_creates_order_spec_and_excel_and_show_download_link(self):
        payload = {"user_text": "Je veux créer une boutique de vêtements"}

        response = self.client.post(reverse("home"), payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.activity, payload["user_text"])
        self.assertEqual(order.status, Order.Status.GENEREE)

        specification = Specification.objects.get(order=order)
        self.assertEqual(specification.content["activity"], "boutique de vêtements")
        self.assertIn("Produits", specification.content["excel"]["sheets"])

        generated_file_name = response.context["generated_file_name"]
        self.assertTrue((Path("media/generated_files") / generated_file_name).exists())
        self.assertIn("télécharger le fichier excel", response.content.decode("utf-8").lower())
