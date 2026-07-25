from django.urls import path
from .views import RegistrationListCreateView, RegistrationDetailView

urlpatterns = [
    path('', RegistrationListCreateView.as_view(), name='registration-list-create'),
    path('<int:pk>/', RegistrationDetailView.as_view(), name='registration-detail'),
]