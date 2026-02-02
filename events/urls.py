from django.urls import path
from .views import event_list
from .views import event_list, get_tickets,event_detail


urlpatterns = [
    path("", event_list, name="event_list"),
    path("", event_list, name="event_list"),
    path("tickets/<int:event_id>/", get_tickets, name="get_tickets"),
    path('', event_list, name='event_list'),
    path('event/<int:event_id>/', event_detail, name='event_detail'),
    path('tickets/<int:event_id>/', get_tickets, name='get_tickets'),

]
