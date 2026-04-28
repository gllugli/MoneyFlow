# pyright: reportAttributeAccessIssue=false

from typing import Any

from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.movements.models import Movement


class MovementListViewTests(TestCase):
    def test_movement_list_page_returns_success(self):
        response: Any = self.client.get(reverse("movements:movement_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movements/movement_list.html")

    def test_movement_list_renders_created_movements(self):
        movement = Movement(
            description="Salário",
            movement_type=Movement.MovementType.CREDIT,
            value=Decimal("3500.00"),
            date=date(2026, 4, 10),
        )
        movement.save()

        response: Any = self.client.get(reverse("movements:movement_list"))

        self.assertContains(response, "Salário")
        self.assertContains(response, "Entrada")
        self.assertContains(response, "+ R$ 3500,00")
        self.assertContains(response, "10/04/2026")
        self.assertContains(response, "Ações")
        self.assertContains(
            response, reverse("movements:movement_update", args=[movement.pk])
        )
        self.assertContains(
            response, reverse("movements:movement_delete", args=[movement.pk])
        )
        self.assertContains(
            response,
            'action="{}"'.format(
                reverse("movements:movement_delete", args=[movement.pk])
            ),
        )

    def test_movement_list_orders_newest_date_first(self):
        older_movement = Movement(
            description="Mercado",
            movement_type=Movement.MovementType.DEBIT,
            value=Decimal("120.00"),
            date=date(2026, 4, 3),
        )
        older_movement.save()

        newer_movement = Movement(
            description="Freelance",
            movement_type=Movement.MovementType.CREDIT,
            value=Decimal("800.00"),
            date=date(2026, 4, 12),
        )
        newer_movement.save()

        response: Any = self.client.get(reverse("movements:movement_list"))

        self.assertEqual(
            list(response.context["movements"]), [newer_movement, older_movement]
        )

    def test_movement_list_shows_empty_state(self):
        response: Any = self.client.get(reverse("movements:movement_list"))

        self.assertContains(response, "Descrição")
        self.assertContains(response, "Tipo")
        self.assertContains(response, "Valor")
        self.assertContains(response, "Data")
        self.assertContains(
            response,
            "Nenhuma movimentação cadastrada ainda. Use o botão acima para registrar a primeira.",
        )

    def test_movement_list_renders_navbar_links(self):
        response: Any = self.client.get(reverse("movements:movement_list"))

        self.assertContains(response, "MoneyFlow")
        self.assertContains(response, "Painel")
        self.assertContains(response, "Movimentações")
        self.assertContains(response, "Nova movimentação")
        self.assertContains(response, reverse("core:dashboard"))

    def test_movement_list_displays_summary_totals(self):
        Movement.objects.create(
            description="Salário",
            movement_type=Movement.MovementType.CREDIT,
            value=Decimal("4200.00"),
            date=date(2026, 4, 9),
        )
        Movement.objects.create(
            description="Conta de luz",
            movement_type=Movement.MovementType.DEBIT,
            value=Decimal("250.00"),
            date=date(2026, 4, 10),
        )

        response: Any = self.client.get(reverse("movements:movement_list"))

        self.assertContains(response, "Total de entradas")
        self.assertContains(response, "Total de saídas")
        self.assertContains(response, "R$ 4200,00")
        self.assertContains(response, "R$ 250,00")

    def test_movement_list_displays_balance_footer(self):
        Movement.objects.create(
            description="Salário",
            movement_type=Movement.MovementType.CREDIT,
            value=Decimal("4200.00"),
            date=date(2026, 4, 9),
        )
        Movement.objects.create(
            description="Conta de luz",
            movement_type=Movement.MovementType.DEBIT,
            value=Decimal("250.00"),
            date=date(2026, 4, 10),
        )

        response: Any = self.client.get(reverse("movements:movement_list"))

        self.assertContains(response, "Saldo final")
        self.assertContains(response, "Entradas menos saídas")
        self.assertContains(response, "R$ 3950,00")
        self.assertContains(response, "Excluir movimentação?")
        self.assertContains(response, "Confirmar")
        self.assertContains(response, "Cancelar")


class MovementCreateViewTests(TestCase):
    def test_movement_create_page_returns_success(self):
        response: Any = self.client.get(reverse("movements:movement_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movements/movement_form.html")
        self.assertContains(response, "Registrar movimentação")

    def test_movement_create_uses_masked_currency_widget_for_value(self):
        response: Any = self.client.get(reverse("movements:movement_create"))

        self.assertContains(response, 'data-currency-input="true"')
        self.assertContains(response, 'inputmode="numeric"')
        self.assertContains(response, 'placeholder="R$ 0,00"')

    def test_movement_create_persists_new_movement(self):
        response: Any = self.client.post(
            reverse("movements:movement_create"),
            {
                "description": "Investimento mensal",
                "movement_type": Movement.MovementType.CREDIT,
                "value": "1500.00",
                "date": "2026-04-27",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("movements:movement_list"))
        self.assertEqual(Movement.objects.count(), 1)
        self.assertContains(response, "Movimentação registrada com sucesso.")
        self.assertContains(response, "Investimento mensal")

    def test_movement_create_accepts_masked_currency_value(self):
        response: Any = self.client.post(
            reverse("movements:movement_create"),
            {
                "description": "Pagamento de cliente",
                "movement_type": Movement.MovementType.CREDIT,
                "value": "R$ 1.234,56",
                "date": "2026-04-27",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("movements:movement_list"))
        self.assertEqual(Movement.objects.count(), 1)
        self.assertEqual(Movement.objects.get().value, Decimal("1234.56"))


class MovementUpdateViewTests(TestCase):
    def test_movement_update_page_returns_success_with_edit_texts(self):
        movement = Movement.objects.create(
            description="Assinatura",
            movement_type=Movement.MovementType.DEBIT,
            value=Decimal("59.90"),
            date=date(2026, 4, 12),
        )

        response: Any = self.client.get(
            reverse("movements:movement_update", args=[movement.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movements/movement_form.html")
        self.assertContains(response, "Editar movimentação")
        self.assertContains(response, "Salvar alterações")
        self.assertContains(response, "R$ 59,90")

    def test_movement_update_persists_changes(self):
        movement = Movement.objects.create(
            description="Internet",
            movement_type=Movement.MovementType.DEBIT,
            value=Decimal("120.00"),
            date=date(2026, 4, 1),
        )

        response: Any = self.client.post(
            reverse("movements:movement_update", args=[movement.pk]),
            {
                "description": "Internet residencial",
                "movement_type": Movement.MovementType.DEBIT,
                "value": "R$ 139,90",
                "date": "2026-04-02",
            },
            follow=True,
        )

        movement.refresh_from_db()

        self.assertRedirects(response, reverse("movements:movement_list"))
        self.assertEqual(movement.description, "Internet residencial")
        self.assertEqual(movement.value, Decimal("139.90"))
        self.assertEqual(movement.date, date(2026, 4, 2))
        self.assertContains(response, "Movimentação atualizada com sucesso.")


class MovementDeleteViewTests(TestCase):
    def test_movement_delete_removes_record_after_confirmation(self):
        movement = Movement.objects.create(
            description="Academia",
            movement_type=Movement.MovementType.DEBIT,
            value=Decimal("89.90"),
            date=date(2026, 4, 8),
        )

        response: Any = self.client.post(
            reverse("movements:movement_delete", args=[movement.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse("movements:movement_list"))
        self.assertFalse(Movement.objects.filter(pk=movement.pk).exists())
        self.assertContains(response, "Movimentação excluída com sucesso.")

    def test_movement_delete_does_not_allow_get_requests(self):
        movement = Movement.objects.create(
            description="Curso",
            movement_type=Movement.MovementType.DEBIT,
            value=Decimal("300.00"),
            date=date(2026, 4, 14),
        )

        response: Any = self.client.get(
            reverse("movements:movement_delete", args=[movement.pk])
        )

        self.assertEqual(response.status_code, 405)
