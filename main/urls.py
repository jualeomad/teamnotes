from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_note/', views.create_note_view, name='create_note'),
]
