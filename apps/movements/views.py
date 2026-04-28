# pyright: reportAttributeAccessIssue=false

from decimal import Decimal

from django.contrib import messages
from django.db.models import Count, DecimalField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.movements.forms import MovementForm
from apps.movements.models import Movement


class MovementListView(ListView):
    model = Movement
    template_name = "movements/movement_list.html"
    context_object_name = "movements"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        money_field = DecimalField(max_digits=12, decimal_places=2)
        movement_manager = Movement._default_manager
        totals = movement_manager.aggregate(
            total_credit=Coalesce(
                Sum("value", filter=Q(movement_type=Movement.MovementType.CREDIT)),
                Value(Decimal("0.00")),
                output_field=money_field,
            ),
            total_debit=Coalesce(
                Sum("value", filter=Q(movement_type=Movement.MovementType.DEBIT)),
                Value(Decimal("0.00")),
                output_field=money_field,
            ),
            movement_count=Count("id"),
        )
        context.update(
            total_credit=totals["total_credit"],
            total_debit=totals["total_debit"],
            movement_count=totals["movement_count"],
        )
        return context


class MovementCreateView(CreateView):
    model = Movement
    form_class = MovementForm
    template_name = "movements/movement_form.html"
    success_url = reverse_lazy("movements:movement_list")

    def form_valid(self, form):
        messages.success(self.request, "Movimentação registrada com sucesso.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_movements"] = Movement._default_manager.all()[:4]
        return context
