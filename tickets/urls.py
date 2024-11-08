
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket_list'),
    path('test-template/', views.test_template, name='test_template'),

    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/create/', views.TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/<int:pk>/edit/', views.TicketUpdateView.as_view(), name='ticket_update'),
    path('ticket/<int:ticket_id>/comment/', views.comment_create, name='comment_create'),
]
