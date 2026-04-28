from django.urls import path

from apps.movements.views import MovementCreateView, MovementListView


app_name = "movements"

urlpatterns = [
    path("", MovementListView.as_view(), name="movement_list"),
    path("nova/", MovementCreateView.as_view(), name="movement_create"),
]
