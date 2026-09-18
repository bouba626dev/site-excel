import json
from pathlib import Path

from django.http import FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from ai_assistant import generate_specification_mock
from excel_generator import generate_excel_file
from orders.models import Order, Specification


def home(request):
    """Page d'accueil publique du site."""
    if request.method == "POST":
        user_text = request.POST.get("user_text", "").strip()
        if not user_text:
            return render(request, "core/home.html", {"user_text": user_text})

        specification = generate_specification_mock(user_text)
        order = Order.objects.create(
            activity=user_text,
            status=Order.Status.EN_ATTENTE,
        )
        Specification.objects.create(order=order, content=specification)

        generated_file_path = generate_excel_file(specification)
        order.status = Order.Status.GENEREE
        order.save(update_fields=["status"])

        request.session["generation_result"] = {
            "user_text": user_text,
            "specification_json": json.dumps(specification, ensure_ascii=False, indent=2),
            "generated_file_name": Path(generated_file_path).name,
        }
        return redirect(reverse("generation_result"))

    return render(request, "core/home.html")


def generation_result(request):
    """Page affichée après la génération d'un fichier Excel."""
    result = request.session.pop("generation_result", None)
    if result is None:
        return redirect("home")
    return render(request, "core/result.html", result)


def download_generated_excel(request, filename):
    """Serve a generated Excel file as a download attachment."""
    file_path = Path(__file__).resolve().parent.parent / "media" / "generated_files" / filename

    if not file_path.exists():
        return render(request, "core/home.html", {"specification_json": "Fichier introuvable."})

    response = FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)
    return response
