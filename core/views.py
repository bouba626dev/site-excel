import json
from pathlib import Path

from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from ai_assistant import generate_specification
from excel_generator import generate_excel_file
from orders.models import Order, Specification


def home(request):
    """Page d'accueil publique du site."""
    if request.method == "POST":
        user_text = request.POST.get("user_text", "").strip()
        if not user_text:
            return render(request, "core/home.html", {"user_text": user_text})

        specification = generate_specification(user_text)
        request.session["generation_result"] = {
            "user_text": user_text,
            "specification_json": json.dumps(specification, ensure_ascii=False, indent=2),
        }
        return redirect(reverse("generation_result"))

    return render(request, "core/home.html")


def generation_result(request):
    """Page affichée après la génération d'un fichier Excel."""
    result = request.session.get("generation_result")
    if result is None:
        return redirect("home")

    order = None
    if request.user.is_authenticated:
        if result.get("order_id"):
            order = Order.objects.filter(id=result["order_id"], user=request.user).first()
        else:
            specification = json.loads(result["specification_json"])
            order = Order.objects.create(
                activity=result["user_text"],
                user=request.user,
                status=Order.Status.EN_ATTENTE_PAIEMENT,
            )
            Specification.objects.create(order=order, content=specification)
            result["order_id"] = order.id
            request.session.modified = True

    return render(request, "core/result.html", {
        **result,
        "order": order,
        "can_confirm_payment": bool(order and order.status == Order.Status.EN_ATTENTE_PAIEMENT),
    })


@login_required
def confirm_payment(request):
    if request.method != "POST":
        return redirect("generation_result")

    result = request.session.get("generation_result", {})
    order = Order.objects.filter(
        id=result.get("order_id"),
        user=request.user,
        status=Order.Status.EN_ATTENTE_PAIEMENT,
    ).first()
    if order is None:
        return redirect("generation_result")

    specification = json.loads(result["specification_json"])
    generated_file_path = generate_excel_file(specification)
    order.status = Order.Status.GENEREE
    order.generated_file_name = Path(generated_file_path).name
    order.save(update_fields=["status", "generated_file_name", "updated_at"])
    result["generated_file_name"] = Path(generated_file_path).name
    request.session.modified = True
    return redirect("generation_result")


@login_required
def history(request):
    """Affiche uniquement les commandes de l'utilisateur connecté."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "core/history.html", {"orders": orders})


@login_required
def download_generated_excel(request, filename):
    """Serve a generated Excel file as a download attachment."""
    order = Order.objects.filter(
        user=request.user,
        status=Order.Status.GENEREE,
        generated_file_name=filename,
    ).first()
    if order is None:
        return redirect("history")

    file_path = Path(__file__).resolve().parent.parent / "media" / "generated_files" / filename

    if not file_path.exists():
        return render(request, "core/home.html", {"specification_json": "Fichier introuvable."})

    response = FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)
    return response
