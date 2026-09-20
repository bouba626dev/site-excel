from django.db import models
from django.conf import settings


class Order(models.Model):
    """Demande client : description de l'activité et suivi du statut."""

    class Status(models.TextChoices):
        EN_ATTENTE = "en_attente", "En attente"
        EN_ATTENTE_PAIEMENT = "en_attente_paiement", "En attente de paiement"
        GENEREE = "generee", "Générée"
        PAYEE = "payee", "Payée"
        TELECHARGEE = "telechargee", "Téléchargée"

    activity = models.TextField(
        verbose_name="Activité",
        help_text="Description de l'activité telle que saisie par le client.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
        verbose_name="Utilisateur",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.EN_ATTENTE,
        verbose_name="Statut",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour",
    )

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]

    def __str__(self):
        preview = self.activity[:50]
        if len(self.activity) > 50:
            preview += "..."
        return f"Commande #{self.pk} — {preview}"


class Specification(models.Model):
    """JSON structuré produit par l'IA pour une commande donnée."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="specifications",
        verbose_name="Commande",
    )
    content = models.JSONField(
        verbose_name="Contenu JSON",
        help_text="Spécification structurée (feuilles, colonnes, formules, etc.).",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    class Meta:
        verbose_name = "Spécification"
        verbose_name_plural = "Spécifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Spécification #{self.pk} — Commande #{self.order_id}"
