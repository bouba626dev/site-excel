"""Fournit une implémentation simulée de génération de spécification.

Cette version est volontairement simple et statique pour permettre de tester le
flux Django sans dépendre d’une API externe ou d’une vraie IA.
"""


def generate_specification_mock(texte_utilisateur: str) -> dict:
    """Retourne un JSON de spécification factice.

    Le paramètre texte_utilisateur est accepté pour garder la même signature que
    la vraie fonction future, mais l’implémentation actuelle ignore son contenu.
    """
    return {
        "activity": "boutique de vêtements",
        "excel": {
            "sheets": ["Produits", "Ventes", "Dépenses", "Dashboard"]
        },
    }
