from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('example', views.example, name='example'),  # Ejemplo de una vista llamada 'index'
    # Agrega más patrones de URL según sea necesario para tus vistas
]
