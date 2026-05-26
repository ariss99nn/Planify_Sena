from django.urls import path
from analitica.views.dashboard_view import DashboardView

analitica_urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]