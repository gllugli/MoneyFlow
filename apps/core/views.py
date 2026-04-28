# pyright: reportAttributeAccessIssue=false

from collections import defaultdict
from decimal import Decimal

from django.db.models import Avg, Count, DecimalField, Max, Q, Sum, Value
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone
from django.views.generic import TemplateView

from apps.movements.models import Movement


MONTH_LABELS = (
    "jan",
    "fev",
    "mar",
    "abr",
    "mai",
    "jun",
    "jul",
    "ago",
    "set",
    "out",
    "nov",
    "dez",
)


def month_start(value):
    return value.replace(day=1)


def add_months(value, months):
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    return value.replace(year=year, month=month, day=1)


def month_label(value):
    return f"{MONTH_LABELS[value.month - 1]}/{str(value.year)[2:]}"


def calculate_change(current, previous):
    if previous == 0:
        if current == 0:
            return 0
        return 100
    return int(((current - previous) / previous) * 100)


def calculate_share(value, total):
    if total <= 0:
        return 0
    return int((value / total) * 100)


def build_net_points(months):
    if not months:
        return ""

    values = [item["net"] for item in months]
    min_value = min(values)
    max_value = max(values)

    if min_value == max_value:
        max_value += Decimal("1.00")
        min_value -= Decimal("1.00")

    width = 300
    height = 140
    x_step = width / max(len(months) - 1, 1)
    points = []

    for index, item in enumerate(months):
        normalized = (item["net"] - min_value) / (max_value - min_value)
        x_position = index * x_step
        y_position = height - float(normalized) * height
        points.append(f"{x_position:.1f},{y_position:.1f}")

    return " ".join(points)


class DashboardView(TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        current_month_start = month_start(today)
        next_month_start = add_months(current_month_start, 1)
        previous_month_start = add_months(current_month_start, -1)
        six_month_start = add_months(current_month_start, -5)
        money_field = DecimalField(max_digits=12, decimal_places=2)
        movement_manager = Movement._default_manager
        latest_movement = movement_manager.first()

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
        balance = totals["total_credit"] - totals["total_debit"]

        current_month_queryset = movement_manager.filter(
            date__gte=current_month_start,
            date__lt=next_month_start,
        )
        previous_month_queryset = movement_manager.filter(
            date__gte=previous_month_start,
            date__lt=current_month_start,
        )

        current_month_totals = current_month_queryset.aggregate(
            month_credit=Coalesce(
                Sum("value", filter=Q(movement_type=Movement.MovementType.CREDIT)),
                Value(Decimal("0.00")),
                output_field=money_field,
            ),
            month_debit=Coalesce(
                Sum("value", filter=Q(movement_type=Movement.MovementType.DEBIT)),
                Value(Decimal("0.00")),
                output_field=money_field,
            ),
            month_count=Count("id"),
            active_days=Count("date", distinct=True),
            average_value=Coalesce(
                Avg("value"),
                Value(Decimal("0.00")),
                output_field=money_field,
            ),
            largest_credit=Coalesce(
                Max("value", filter=Q(movement_type=Movement.MovementType.CREDIT)),
                Value(Decimal("0.00")),
                output_field=money_field,
            ),
            largest_debit=Coalesce(
                Max("value", filter=Q(movement_type=Movement.MovementType.DEBIT)),
                Value(Decimal("0.00")),
                output_field=money_field,
            ),
        )
        current_month_net = (
            current_month_totals["month_credit"] - current_month_totals["month_debit"]
        )

        previous_month_totals = previous_month_queryset.aggregate(
            month_credit=Coalesce(
                Sum("value", filter=Q(movement_type=Movement.MovementType.CREDIT)),
                Value(Decimal("0.00")),
                output_field=money_field,
            ),
            month_debit=Coalesce(
                Sum("value", filter=Q(movement_type=Movement.MovementType.DEBIT)),
                Value(Decimal("0.00")),
                output_field=money_field,
            ),
        )
        previous_month_net = (
            previous_month_totals["month_credit"] - previous_month_totals["month_debit"]
        )

        monthly_rows = (
            movement_manager.filter(date__gte=six_month_start)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(
                credit=Coalesce(
                    Sum("value", filter=Q(movement_type=Movement.MovementType.CREDIT)),
                    Value(Decimal("0.00")),
                    output_field=money_field,
                ),
                debit=Coalesce(
                    Sum("value", filter=Q(movement_type=Movement.MovementType.DEBIT)),
                    Value(Decimal("0.00")),
                    output_field=money_field,
                ),
            )
            .order_by("month")
        )

        monthly_map = {
            row["month"].date() if hasattr(row["month"], "date") else row["month"]: row
            for row in monthly_rows
        }

        six_months = []
        chart_max_value = Decimal("1.00")
        running_balance = Decimal("0.00")
        for index in range(6):
            month_value = add_months(six_month_start, index)
            month_data = monthly_map.get(month_value, {})
            income = month_data.get("credit", Decimal("0.00"))
            expense = month_data.get("debit", Decimal("0.00"))
            net = income - expense
            running_balance += net
            chart_max_value = max(chart_max_value, income, expense, abs(net))
            six_months.append(
                {
                    "label": month_label(month_value),
                    "income": income,
                    "expense": expense,
                    "net": net,
                    "running_balance": running_balance,
                }
            )

        for item in six_months:
            item["income_height"] = max(
                int((item["income"] / chart_max_value) * 100),
                6 if item["income"] > 0 else 0,
            )
            item["expense_height"] = max(
                int((item["expense"] / chart_max_value) * 100),
                6 if item["expense"] > 0 else 0,
            )

        current_month_volume = (
            current_month_totals["month_credit"] + current_month_totals["month_debit"]
        )
        income_share = calculate_share(
            current_month_totals["month_credit"], current_month_volume
        )
        expense_share = calculate_share(
            current_month_totals["month_debit"], current_month_volume
        )

        top_expenses = list(
            current_month_queryset.filter(movement_type=Movement.MovementType.DEBIT)
            .values("description")
            .annotate(total=Sum("value"))
            .order_by("-total", "description")[:3]
        )
        top_income = list(
            current_month_queryset.filter(movement_type=Movement.MovementType.CREDIT)
            .values("description")
            .annotate(total=Sum("value"))
            .order_by("-total", "description")[:3]
        )

        weekday_totals = defaultdict(lambda: Decimal("0.00"))
        weekday_labels = ("Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom")
        for row in current_month_queryset.values("date").annotate(total=Sum("value")):
            weekday_totals[row["date"].weekday()] += row["total"]

        weekday_activity = []
        weekday_max = max(weekday_totals.values(), default=Decimal("0.00"))
        for index, label in enumerate(weekday_labels):
            total = weekday_totals[index]
            if weekday_max > 0:
                height = max(
                    int((total / weekday_max) * 100),
                    12 if total > 0 else 0,
                )
            else:
                height = 0
            weekday_activity.append(
                {
                    "label": label,
                    "total": total,
                    "height": height,
                }
            )

        days_since_last_movement = None
        if latest_movement:
            days_since_last_movement = (today - latest_movement.date).days

        context.update(
            total_credit=totals["total_credit"],
            total_debit=totals["total_debit"],
            movement_count=totals["movement_count"],
            balance=balance,
            recent_movements=movement_manager.all()[:6],
            latest_movement=latest_movement,
            current_month_label=month_label(current_month_start),
            previous_month_label=month_label(previous_month_start),
            current_month_credit=current_month_totals["month_credit"],
            current_month_debit=current_month_totals["month_debit"],
            current_month_net=current_month_net,
            current_month_count=current_month_totals["month_count"],
            current_month_active_days=current_month_totals["active_days"],
            average_movement_value=current_month_totals["average_value"],
            largest_credit=current_month_totals["largest_credit"],
            largest_debit=current_month_totals["largest_debit"],
            previous_month_net=previous_month_net,
            net_change_percentage=calculate_change(
                current_month_net, previous_month_net
            ),
            income_change_percentage=calculate_change(
                current_month_totals["month_credit"],
                previous_month_totals["month_credit"],
            ),
            expense_change_percentage=calculate_change(
                current_month_totals["month_debit"],
                previous_month_totals["month_debit"],
            ),
            income_share=income_share,
            expense_share=expense_share,
            six_months=six_months,
            net_points=build_net_points(six_months),
            top_expenses=top_expenses,
            top_income=top_income,
            weekday_activity=weekday_activity,
            days_since_last_movement=days_since_last_movement,
        )
        return context
