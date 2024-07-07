from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Change this to avoid clash
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Change this to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self) -> str:
        return self.username

# Item model
class Item(models.Model):
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Like New', 'Like New'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor')
    ]

    CATEGORY_CHOICES = [
        ('Vehicle', 'Vehicle'),
        ('Electronics', 'Electronics'),
        ('Furniture', 'Furniture'),
        ('Clothing', 'Clothing'),
        ('Books', 'Books'),
        ('Home Appliances', 'Home Appliances'),
        ('Toys', 'Toys'),
        ('Sports Equipment', 'Sports Equipment'),
        ('Jewelry', 'Jewelry'),
        ('Collectibles', 'Collectibles'),
        ('Others', 'Others')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_description = models.TextField(blank=True, null=True)
    item_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    item_condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    item_value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

# Exchange model
class Exchange(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed')
    ]

    offered_item = models.ForeignKey(Item, related_name='offered_item', on_delete=models.CASCADE)
    requested_item = models.ForeignKey(Item, related_name='requested_item', on_delete=models.CASCADE)
    offered_by_user = models.ForeignKey(User, related_name='offered_by_user', on_delete=models.CASCADE)
    requested_by_user = models.ForeignKey(User, related_name='requested_by_user', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (str(self.offered_by_user) + " - " + str(self.offered_item))

# Transaction model
class Transaction(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by_user = models.ForeignKey(User, related_name='paid_by_user', on_delete=models.CASCADE)
    received_by_user = models.ForeignKey(User, related_name='received_by_user', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)

# Message model
class Message(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    sender_user = models.ForeignKey(User, related_name='sender_user', on_delete=models.CASCADE)
    receiver_user = models.ForeignKey(User, related_name='receiver_user', on_delete=models.CASCADE)
    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
