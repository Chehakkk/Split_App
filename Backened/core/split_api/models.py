from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    profile_img = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.user.username

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, through='GroupMember', related_name='group_memberships')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.group.name} - {self.user.username}"


class GroupChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.message[:30]}"

CATEGORY_CHOICES=(
    ('food','Food'),
    ('transport','Transport'),
    ('entertainment','Entertainment'),
    ('other','Other'),
)
class Category(models.Model):
    # name = models.CharField(max_length=200)
    name=models.CharField(choices=CATEGORY_CHOICES,max_length=200,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_categories')

    def __str__(self):
        return self.name


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_created')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} (${self.amount})"

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='splits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('expense', 'user')

    def __str__(self):
        return f"{self.user.username} owes ${self.amount} for {self.expense.description}"

class Payment(models.Model):
    from_user = models.ForeignKey(User, related_name='payments_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='payments_received', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.ForeignKey(ExpenseSplit, on_delete=models.SET_NULL, null=True, blank=True)
    expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    settled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} paid {self.to_user.username} ${self.amount.amount if self.amount else 0}"



# class Payment(models.Model):
#     from_user = models.ForeignKey(User, related_name='payments_sent', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(User, related_name='payments_received', on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     amount = models.ManyToManyField(ExpenseSplit, blank=True)
#     expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, null=True, blank=True)
#     note = models.TextField(blank=True, null=True)
#     settled_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         total = sum(a.amount for a in self.amount.all())
#         return f"{self.from_user.username} paid {self.to_user.username} ${total}"


# --------------------------------------
# Notifications
# --------------------------------------
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    type = models.CharField(max_length=50, default='general')  # e.g., 'expense', 'invite'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


# --------------------------------------
# Activity Logs
# --------------------------------------
class ActivityLog(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='activity_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)  # e.g., "added an expense"
    data = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"


# Create your models here.
