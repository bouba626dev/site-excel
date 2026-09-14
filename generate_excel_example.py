import json
from pathlib import Path

from excel_generator import generate_excel_file


def main():
    specification = {
        "activity": "test",
        "excel": {"sheets": ["Test"]},
    }

    output_path = generate_excel_file(specification)
    print(f"Fichier généré : {output_path}")
    print(f"Existe : {Path(output_path).exists()}")


if __name__ == "__main__":
    main()
