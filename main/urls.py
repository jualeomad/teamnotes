from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_note/', views.create_note_view, name='create_note'),
    path('edit_note/<str:note_id>/', views.edit_note, name='edit_note'),
    path('delete_note/<str:note_id>/', views.delete_note, name='delete_note'),
]
