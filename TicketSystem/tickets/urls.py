from django.urls import path

from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.main, name='main'),
    path('list/', views.ticket_list, name='list'),
    path('detail/<int:pk>/add', views.add_file_to_ticket, name='add_file'),
    path('detail/<int:id>/', views.ticket_detail, name='detail'),
    path('delete/<int:id>/', views.delete_view, name='delete'),
    path('create/', views.create_ticket, name='create'),
]
