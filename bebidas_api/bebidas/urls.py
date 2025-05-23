from django.urls import path
from .views import BebidaListCreate, BebidaDetail, CrearPostreDesdeBebida

urlpatterns = [
    path('bebidas/', BebidaListCreate.as_view()),
    path('bebidas/<int:pk>/', BebidaDetail.as_view()),
    path('bebidas/crear-postre/', CrearPostreDesdeBebida.as_view()),
]