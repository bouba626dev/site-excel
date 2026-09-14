from django.contrib import admin

from .models import Order, Specification


class SpecificationInline(admin.TabularInline):
    """Affiche les spécifications directement sur la page d'une commande."""

    model = Specification
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "activity_preview", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("activity",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [SpecificationInline]

    @admin.display(description="Activité")
    def activity_preview(self, obj):
        preview = obj.activity[:60]
        if len(obj.activity) > 60:
            preview += "..."
        return preview


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "created_at")
    list_filter = ("created_at",)
    search_fields = ("order__activity",)
    readonly_fields = ("created_at",)
