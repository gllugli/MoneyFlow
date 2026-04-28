# pyright: reportAttributeAccessIssue=false

from decimal import Decimal

from django.contrib import messages
from django.db.models import Count, DecimalField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

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
            balance=totals["total_credit"] - totals["total_debit"],
        )
        return context


class MovementFormContextMixin:
    page_title = "Nova movimentação | MoneyFlow"
    form_eyebrow = "Novo lançamento"
    form_heading = "Registrar movimentação"
    form_subtitle = (
        "Cadastre entradas e saídas com um formulário simples, rápido e pensado "
        "para manter seu controle financeiro sempre atualizado."
    )
    form_section_description = (
        "Preencha os campos abaixo para adicionar um novo registro ao histórico "
        "e atualizar o painel."
    )
    form_submit_label = "Salvar movimentação"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            page_title=self.page_title,
            form_eyebrow=self.form_eyebrow,
            form_heading=self.form_heading,
            form_subtitle=self.form_subtitle,
            form_section_description=self.form_section_description,
            form_submit_label=self.form_submit_label,
            recent_movements=Movement._default_manager.all()[:4],
        )
        return context


class MovementCreateView(MovementFormContextMixin, CreateView):
    model = Movement
    form_class = MovementForm
    template_name = "movements/movement_form.html"
    success_url = reverse_lazy("movements:movement_list")

    def form_valid(self, form):
        messages.success(self.request, "Movimentação registrada com sucesso.")
        return super().form_valid(form)


class MovementUpdateView(MovementFormContextMixin, UpdateView):
    model = Movement
    form_class = MovementForm
    template_name = "movements/movement_form.html"
    success_url = reverse_lazy("movements:movement_list")
    page_title = "Editar movimentação | MoneyFlow"
    form_eyebrow = "Edição de lançamento"
    form_heading = "Editar movimentação"
    form_subtitle = (
        "Atualize as informações da movimentação selecionada para manter seu "
        "histórico financeiro correto e fácil de acompanhar."
    )
    form_section_description = (
        "Revise os campos abaixo para ajustar este registro sem precisar criar "
        "uma nova movimentação."
    )
    form_submit_label = "Salvar alterações"

    def form_valid(self, form):
        messages.success(self.request, "Movimentação atualizada com sucesso.")
        return super().form_valid(form)


class MovementDeleteView(DeleteView):
    model = Movement
    success_url = reverse_lazy("movements:movement_list")
    http_method_names = ["post"]

    def form_valid(self, form):
        messages.success(self.request, "Movimentação excluída com sucesso.")
        return super().form_valid(form)
