from django.db import models


class Order(models.Model):
    """Demande client : description de l'activité et suivi du statut."""

    class Status(models.TextChoices):
        EN_ATTENTE = "en_attente", "En attente"
        GENEREE = "generee", "Générée"
        PAYEE = "payee", "Payée"
        TELECHARGEE = "telechargee", "Téléchargée"

    activity = models.TextField(
        verbose_name="Activité",
        help_text="Description de l'activité telle que saisie par le client.",
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
