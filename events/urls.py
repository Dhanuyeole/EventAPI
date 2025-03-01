from django.urls import path
from .views import UserRegistrationView, EventCreateView, EventListView, TicketPurchaseView
from .views import login_view, protected_view
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', protected_view, name='protected'),  # Example protected rout
    path('register/', UserRegistrationView.as_view(), name='register'),  # User Registration
    path('events/', EventListView.as_view(), name='event-list'),  # Fetch all events
    path('events/create/', EventCreateView.as_view(), name='event-create'),  # Create Event (Admin)
    path('events/<int:id>/purchase/', TicketPurchaseView.as_view(), name='ticket-purchase'),  # Purchase Tickets
]
