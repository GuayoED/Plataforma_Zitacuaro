from django.urls import path
from .views import ReporteView

urlpatterns = [
    path('dispo_final/', ReporteView.as_view(), name='reportes')
]