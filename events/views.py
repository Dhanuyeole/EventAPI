from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .models import User, Event, Ticket
from .serializers import UserSerializer, EventSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import generics, status



# Generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
        print(user.password)
        if user and user.check_password(password):  # ❌ This is wrong
            tokens = get_tokens_for_user(user)
            return Response({"message": "Login successful", "tokens": tokens})
        else:
            return Response({"error": "Invalid credentials"}, status=400)

    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=400)

# Protected Route (Example)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": f"Hello, {request.user.username}! You are authenticated."})

# User Registration View (Admin/User)
class UserRegistrationView(generics.CreateAPIView):
    """
    API to register a user (Admin/User).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Hash the password before saving.
        """
        serializer.save(password=make_password(serializer.validated_data['password']))


# Event Management Views (Admin Only)
class EventCreateView(generics.CreateAPIView):
    """
    API to create a new event (Admin Only).
    """
    # permission_classes = [IsAuthenticated]  # Requires user to be authenticated

    def post(self, request):
        # Ensure the user is logged in
        # if not request.user.is_authenticated:
        #     return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        role = request.data.get("role")  
        # Check if the user is an admin
        if  role != 'admin':
            return Response({"error": "Only admins can create events"}, status=status.HTTP_403_FORBIDDEN)

        # Proceed with event creation
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventListView(generics.ListAPIView):
    """
    API to fetch all events (Admin and User).
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]  # Both Admin and User can view events


#  Ticket Purchase View (User Only)
class TicketPurchaseView(APIView):
    """
    API to purchase tickets for an event (User Only).
    """
    def post(self, request, id):
        role = request.data.get('role')
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)

        if role != 'user':
            return Response({"error": "Only Users can purchase tickets."}, status=403)

        quantity = request.data.get("quantity", 0)

        # Check if enough tickets are available
        if event.tickets_sold + quantity > event.total_tickets:
            return Response({"error": "Not enough tickets available."}, status=400)
        # Create ticket entry
        Ticket.objects.create(user=None, event=event, quantity=quantity)

        # Update tickets sold count
        event.tickets_sold += quantity
        event.save()

        return Response({"message": "Tickets purchased successfully!"})
