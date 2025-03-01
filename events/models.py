from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Custom User Model (Without Django's built-in User)
class User(models.Model):
    """
    Custom User model with basic authentication fields.
    This model does not use Django's built-in authentication system.
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    username = models.CharField(max_length=150, unique=True)  # Unique username
    password = models.CharField(max_length=128, blank=True)  # Store hashed passwords for security
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')  # User roles: Admin/User

    def save(self, *args, **kwargs):
        """
        Override the save method to hash the password before saving.
        This ensures passwords are securely stored.
        """
        if not self.password.startswith('pbkdf2_sha256$'):  # Check if password is already hashed
            self.password = make_password(self.password)  # Hash the password
        super().save(*args, **kwargs)  # Call the parent save method

    def check_password(self, raw_password):
        """Compare hashed password with user input"""
        return check_password(raw_password, self.password)  


    def __str__(self):
        """
        String representation of the User model.
        Returns the username for better readability in the admin panel or shell.
        """
        return self.username


# Event Model
class Event(models.Model):
    """
    Model representing an event where users can purchase tickets.
    """
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=255)  # Name of the event
    date = models.DateField()  # Date when the event takes place
    total_tickets = models.IntegerField()  # Total number of tickets available
    tickets_sold = models.IntegerField(default=0)  # Number of tickets sold, default is 0

    def __str__(self):
        """
        String representation of the Event model.
        Returns event name and date for better readability.
        """
        return f"{self.name} ({self.date})"


# Ticket Model
class Ticket(models.Model):
    """
    Model representing tickets purchased by users for events.
    """
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,  # Set user to NULL if deleted
        null=True,  # Allow NULL values
        blank=True  # Allow blank values
    ) 
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # ForeignKey to Event (event purchased for)
    quantity = models.IntegerField()  # Number of tickets purchased
    purchase_date = models.DateTimeField(auto_now_add=True)  # Auto-set timestamp when ticket is purchased

    def __str__(self):
        """
        String representation of the Ticket model.
        Displays username, event name, and number of tickets purchased.
        """
        return f"{self.user.username} - {self.event.name} ({self.quantity} tickets)"
