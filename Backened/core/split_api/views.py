from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from .filters import ExpenseFilter

# from .models import (
#     UserProfile, Group, GroupMember, Expense, ExpenseSplit,
#     Payment, Category, ActivityLog, Notification
# )

# from .serializers import (
#     UserSerializer, UserProfileSerializer, GroupSerializer, GroupMemberSerializer,
#     ExpenseSerializer, ExpenseSplitSerializer, PaymentSerializer,
#     CategorySerializer, NotificationSerializer, ActivityLogSerializer
# )

User = get_user_model()

# ---------------------------
# 👤 User Views
# ---------------------------
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # Public registration allowed


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("Access denied.")
        return obj

# ---------------------------
# 👥 Group Views
# ---------------------------
class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']

    def get_queryset(self):
        # For development, return all groups if user is not authenticated
        if self.request.user.is_authenticated:
            return Group.objects.filter(members=self.request.user)
        else:
            return Group.objects.all()

    def perform_create(self, serializer):
        # For development, create a default user if not authenticated
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            # Create or get a default user for development
            user, created = User.objects.get_or_create(
                username='default_user',
                defaults={'email': 'default@example.com'}
            )
        
        group = serializer.save(created_by=user)
        group.members.add(user)

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user not in obj.members.all():
            raise PermissionDenied("Not a group member.")
        return obj

# ---------------------------
# 👥 Group Member Views
# ---------------------------
class GroupMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # For development, return all group members if user is not authenticated
        if self.request.user.is_authenticated:
            return GroupMember.objects.filter(user=self.request.user)
        else:
            return GroupMember.objects.all()

    def perform_create(self, serializer):
        # For development, allow creation without authentication
        serializer.save()

class GroupMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]

# ---------------------------
# 💸 Expense Views
# ---------------------------
class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny]  # Changed to AllowAny for development
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter

    def get_queryset(self):
        # For development, return all expenses if user is not authenticated
        if self.request.user.is_authenticated:
            return Expense.objects.filter(group__members=self.request.user)
        else:
            return Expense.objects.all()

    def perform_create(self, serializer):
        # For development, create a default user if not authenticated
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            # Create or get a default user for development
            user, created = User.objects.get_or_create(
                username='default_user',
                defaults={'email': 'default@example.com'}
            )
        
        serializer.save(created_by=user)

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user not in obj.group.members.all():
            raise PermissionDenied("Not a group member.")
        return obj

# ---------------------------
# 💰 Expense Split Views
# ---------------------------
class ExpenseSplitListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSplitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExpenseSplit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        expense = serializer.validated_data['expense']
        if self.request.user not in expense.group.members.all():
            raise PermissionDenied("You are not a group member.")
        serializer.save()

class ExpenseSplitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseSplit.objects.all()
    serializer_class = ExpenseSplitSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj.user and self.request.user != obj.expense.created_by:
            raise PermissionDenied("Access denied.")
        return obj

# ---------------------------
# 💳 Payment Views
# ---------------------------
class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]  # Changed to AllowAny for development

    def get_queryset(self):
        # For development, return all payments if user is not authenticated
        if self.request.user.is_authenticated:
            return Payment.objects.filter(from_user=self.request.user) | Payment.objects.filter(to_user=self.request.user)
        else:
            return Payment.objects.all()

    def perform_create(self, serializer):
        # For development, allow creation without authentication
        serializer.save()

# ---------------------------
# 🗂️ Category Views
# ---------------------------
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # Changed to AllowAny for development

    def get_queryset(self):
        # For development, return all categories if user is not authenticated
        if self.request.user.is_authenticated:
            return Category.objects.filter(created_by=self.request.user)
        else:
            return Category.objects.all()

    def perform_create(self, serializer):
        # For development, create a default user if not authenticated
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            # Create or get a default user for development
            user, created = User.objects.get_or_create(
                username='default_user',
                defaults={'email': 'default@example.com'}
            )
        
        serializer.save(created_by=user)

# ---------------------------
# 🔔 Notification Views
# ---------------------------
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

# ---------------------------
# 📝 Activity Log Views
# ---------------------------
class ActivityLogListView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.request.query_params.get('group')
        if not group_id:
            raise ValidationError("Missing 'group' query parameter.")
        return ActivityLog.objects.filter(group_id=group_id).select_related('user')
