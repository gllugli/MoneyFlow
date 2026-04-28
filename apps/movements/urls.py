from django.urls import path

from apps.movements.views import (
    MovementCreateView,
    MovementDeleteView,
    MovementListView,
    MovementUpdateView,
)


app_name = "movements"

urlpatterns = [
    path("", MovementListView.as_view(), name="movement_list"),
    path("nova/", MovementCreateView.as_view(), name="movement_create"),
    path("<int:pk>/editar/", MovementUpdateView.as_view(), name="movement_update"),
    path("<int:pk>/excluir/", MovementDeleteView.as_view(), name="movement_delete"),
]
