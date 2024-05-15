from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('example', views.example, name='example'),
    path('create_note/', views.create_note_view, name='create_note'),
]
