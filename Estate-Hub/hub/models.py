from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='buyer')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'role']

    def __str__(self):
        return f"{self.username} ({self.role})"

class Listing(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    num_bedrooms = models.IntegerField()
    num_bathrooms = models.IntegerField()
    square_footage = models.IntegerField()
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='property_images/')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='listings')

    def __str__(self):
        return self.title

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['property', 'reviewer']  # One review per property per user

    def __str__(self):
        return f"{self.reviewer.username}'s review for {self.property.title}"

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')  # Ensures a user can only favorite a property once

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.property.title}"
