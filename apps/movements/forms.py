from decimal import Decimal, InvalidOperation

from django import forms
from django.utils import timezone

from apps.movements.models import Movement


class MovementForm(forms.ModelForm):
    value = forms.CharField(
        label="Valor",
        help_text="Informe apenas números positivos; o tipo define o impacto no saldo.",
        widget=forms.TextInput(
            attrs={
                "inputmode": "numeric",
                "autocomplete": "off",
                "placeholder": "R$ 0,00",
                "data-currency-input": "true",
            }
        ),
    )

    class Meta:
        model = Movement
        fields = ["description", "movement_type", "value", "date"]
        labels = {
            "description": "Descrição",
            "movement_type": "Tipo de movimentação",
            "value": "Valor",
            "date": "Data",
        }
        help_texts = {
            "description": "Use um nome claro para identificar rapidamente o lançamento.",
            "movement_type": "Escolha se o valor representa entrada ou saída.",
            "value": "Informe apenas números positivos; o tipo define o impacto no saldo.",
            "date": "Selecione a data em que a movimentação ocorreu.",
        }
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "placeholder": "Ex.: salário, aluguel, mercado, investimento",
                }
            ),
            "movement_type": forms.Select(),
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["movement_type"].choices = [
            (Movement.MovementType.CREDIT, "Entrada"),
            (Movement.MovementType.DEBIT, "Saída"),
        ]
        if not self.initial.get("date"):
            self.fields["date"].initial = timezone.localdate()
        if not self.is_bound:
            initial_value = self.initial.get("value") or getattr(
                self.instance, "value", None
            )
            if initial_value:
                self.initial["value"] = self.format_currency_value(initial_value)

    def clean_value(self):
        raw_value = self.cleaned_data["value"]
        raw_value = "".join(raw_value.replace("R$", "").split())

        if "," in raw_value:
            normalized_value = raw_value.replace(".", "").replace(",", ".")
        else:
            normalized_value = raw_value
            if normalized_value.count(".") > 1:
                normalized_value = normalized_value.replace(".", "")

        try:
            value = Decimal(normalized_value)
        except InvalidOperation as error:
            raise forms.ValidationError("Informe um valor numérico válido.") from error

        if value <= 0:
            raise forms.ValidationError("Informe um valor maior que zero.")
        return value

    @staticmethod
    def format_currency_value(value):
        decimal_value = Decimal(value).quantize(Decimal("0.01"))
        integer_part, decimal_part = f"{decimal_value:.2f}".split(".")
        integer_part_with_separator = f"{int(integer_part):,}".replace(",", ".")
        return f"R$ {integer_part_with_separator},{decimal_part}"
