from typing import Any

from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.movements.models import Movement


class DashboardViewTests(TestCase):
    def test_dashboard_page_returns_success(self):
        response: Any = self.client.get(reverse("core:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/dashboard.html")

    def test_dashboard_renders_navbar_links(self):
        response: Any = self.client.get(reverse("core:dashboard"))

        self.assertContains(response, "MoneyFlow")
        self.assertContains(response, "Painel")
        self.assertContains(response, "Movimentações")
        self.assertContains(response, "Nova movimentação")
        self.assertContains(response, reverse("core:dashboard"))
        self.assertContains(response, reverse("movements:movement_list"))
        self.assertContains(response, reverse("movements:movement_create"))

    def test_dashboard_displays_financial_metrics(self):
        Movement._default_manager.create(
            description="Salário",
            movement_type=Movement.MovementType.CREDIT,
            value=Decimal("5000.00"),
            date=date(2026, 4, 20),
        )
        Movement._default_manager.create(
            description="Aluguel",
            movement_type=Movement.MovementType.DEBIT,
            value=Decimal("1800.00"),
            date=date(2026, 4, 21),
        )

        response: Any = self.client.get(reverse("core:dashboard"))

        self.assertContains(response, "Saldo atual")
        self.assertContains(response, "R$ 3.200,00")
        self.assertContains(response, "R$ 5.000,00")
        self.assertContains(response, "R$ 1.800,00")
        self.assertContains(response, "Salário")
        self.assertContains(response, "Aluguel")

    def test_dashboard_renders_executive_sections(self):
        response: Any = self.client.get(reverse("core:dashboard"))

        self.assertContains(response, "Painel executivo")
        self.assertContains(response, "Entradas x saidas nos ultimos 6 meses")
        self.assertContains(response, "Pulso do resultado")
        self.assertContains(response, "Mix financeiro do mes")
        self.assertContains(response, "Maiores impactos do mes")

    def test_dashboard_calculates_monthly_metrics_and_datasets(self):
        today = timezone.localdate()
        current_month_date = today.replace(day=10)
        if today.month == 1:
            previous_month_date = date(today.year - 1, 12, 12)
        else:
            previous_month_date = date(today.year, today.month - 1, 12)

        Movement._default_manager.create(
            description="Salário",
            movement_type=Movement.MovementType.CREDIT,
            value=Decimal("5000.00"),
            date=current_month_date,
        )
        Movement._default_manager.create(
            description="Freelance",
            movement_type=Movement.MovementType.CREDIT,
            value=Decimal("1200.00"),
            date=current_month_date.replace(day=18),
        )
        Movement._default_manager.create(
            description="Aluguel",
            movement_type=Movement.MovementType.DEBIT,
            value=Decimal("1800.00"),
            date=current_month_date.replace(day=20),
        )
        Movement._default_manager.create(
            description="Cartao",
            movement_type=Movement.MovementType.DEBIT,
            value=Decimal("900.00"),
            date=previous_month_date,
        )

        response: Any = self.client.get(reverse("core:dashboard"))

        self.assertEqual(response.context["current_month_credit"], Decimal("6200.00"))
        self.assertEqual(response.context["current_month_debit"], Decimal("1800.00"))
        self.assertEqual(response.context["current_month_net"], Decimal("4400.00"))
        self.assertEqual(response.context["largest_credit"], Decimal("5000.00"))
        self.assertEqual(response.context["largest_debit"], Decimal("1800.00"))
        self.assertEqual(len(response.context["six_months"]), 6)
        self.assertContains(response, "R$ 4.400,00")
        self.assertContains(response, "Freelance")
        self.assertContains(response, "Aluguel")
