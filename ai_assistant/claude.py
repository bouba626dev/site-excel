import json
import os

from anthropic import Anthropic


SYSTEM_PROMPT = """Tu transformes une demande métier en spécification Excel.
Réponds uniquement avec un objet JSON valide, sans markdown, exactement sous cette forme:
{
  "activity": "description courte de l'activité",
  "excel": {"sheets": ["Nom de feuille 1", "Nom de feuille 2"]}
}
Propose entre 2 et 6 noms de feuilles utiles et concis."""


def generate_specification(texte_utilisateur: str) -> dict:
    """Demande à Claude une spécification Excel structurée."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY n'est pas configurée.")

    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest"),
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": texte_utilisateur}],
    )
    text = "".join(block.text for block in message.content if getattr(block, "type", None) == "text").strip()
    specification = json.loads(text)

    if not isinstance(specification, dict) or not isinstance(specification.get("excel"), dict):
        raise ValueError("Claude a retourné une spécification Excel invalide.")
    if not specification.get("activity") or not specification["excel"].get("sheets"):
        raise ValueError("La spécification Excel retournée est incomplète.")
    return specification