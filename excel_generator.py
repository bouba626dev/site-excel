import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from openpyxl import Workbook


def _parse_specification(specification: dict | str) -> dict:
    if isinstance(specification, dict):
        return specification
    if isinstance(specification, str):
        value = specification.strip()
        if not value:
            raise ValueError("La spécification JSON est vide.")
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            try:
                import ast

                parsed = ast.literal_eval(value)
                if isinstance(parsed, dict):
                    return parsed
            except (ValueError, SyntaxError):
                pass
            raise
    raise TypeError("La spécification doit être un dictionnaire ou une chaîne JSON.")


def _sanitize_name(value: Any) -> str:
    text = str(value or "document").strip()
    return "".join(ch if ch.isalnum() or ch in ("_", "-", " ") else "_" for ch in text) or "document"


def generate_excel_file(specification: dict | str, output_dir: str | None = None) -> str:
    """Create an Excel workbook from a specification JSON and return the generated file path.

    Example:
        {"activity": "test", "excel": {"sheets": ["Test"]}}
    """
    specification = _parse_specification(specification)

    excel_spec = specification.get("excel") or {}
    if not isinstance(excel_spec, dict):
        raise TypeError("Le bloc 'excel' doit être un dictionnaire.")

    sheet_names = excel_spec.get("sheets") or ["Sheet"]
    if isinstance(sheet_names, str):
        sheet_names = [sheet_names]
    if not isinstance(sheet_names, Iterable) or isinstance(sheet_names, (bytes, str)):
        raise TypeError("'excel.sheets' doit être une liste de noms de feuilles.")

    sheet_names = [str(name) for name in sheet_names if str(name).strip()]
    if not sheet_names:
        sheet_names = ["Sheet"]

    project_root = Path(__file__).resolve().parent
    base_output_dir = Path(output_dir) if output_dir else project_root / "media" / "generated_files"
    base_output_dir.mkdir(parents=True, exist_ok=True)

    env_output_dir = os.getenv("EXCEL_GENERATOR_OUTPUT_DIR")
    if env_output_dir:
        base_output_dir = Path(env_output_dir)
        base_output_dir.mkdir(parents=True, exist_ok=True)

    activity_name = _sanitize_name(specification.get("activity") or "document")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{activity_name}_{timestamp}.xlsx"
    output_path = base_output_dir / filename

    workbook = Workbook()
    for index, sheet_name in enumerate(sheet_names):
        if index == 0:
            active_sheet = workbook.active
            active_sheet.title = sheet_name
            target_sheet = active_sheet
        else:
            target_sheet = workbook.create_sheet(title=sheet_name)

        target_sheet["A1"] = sheet_name

    workbook.save(output_path)
    return str(output_path)
