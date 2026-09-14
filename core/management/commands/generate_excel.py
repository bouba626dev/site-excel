import json

from django.core.management.base import BaseCommand

from excel_generator import _parse_specification, generate_excel_file


class Command(BaseCommand):
    help = "Génère un fichier Excel à partir d'une spécification JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "--json",
            dest="specification_json",
            default='{"activity": "test", "excel": {"sheets": ["Test"]}}',
            help="Spécification JSON ou dictionnaire Python en chaîne.",
        )

    def handle(self, *args, **options):
        specification_json = options["specification_json"]
        try:
            specification = _parse_specification(specification_json)
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError("La valeur --json doit être un JSON valide ou un dictionnaire Python.") from exc

        output_path = generate_excel_file(specification)
        self.stdout.write(self.style.SUCCESS(f"Fichier généré : {output_path}"))
