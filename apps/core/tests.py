from typing import Any

from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

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
        self.assertContains(response, "R$ 3200,00")
        self.assertContains(response, "R$ 5000,00")
        self.assertContains(response, "R$ 1800,00")
        self.assertContains(response, "Salário")
        self.assertContains(response, "Aluguel")
