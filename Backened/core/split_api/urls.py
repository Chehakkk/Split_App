from django.urls import path
from .views import (
    UserCreateView,
    UserProfileDetailView,

    GroupListCreateView,
    GroupDetailView,
    GroupMemberListCreateView,
    GroupMemberDetailView,

    ExpenseListCreateView,
    ExpenseDetailView,
    ExpenseSplitListCreateView,
    ExpenseSplitDetailView,

    PaymentListCreateView,
    CategoryListCreateView,
    NotificationListView,
    ActivityLogListView,
)

urlpatterns = [
    # 👤 User endpoints
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserProfileDetailView.as_view(), name='user-profile'),

    # 👥 Group endpoints
    path('groups/', GroupListCreateView.as_view(), name='group-list-create'),
    path('groups/<uuid:pk>/', GroupDetailView.as_view(), name='group-detail'),

    # 👤 Group members
    path('group-members/', GroupMemberListCreateView.as_view(), name='groupmember-list-create'),
    path('group-members/<uuid:pk>/', GroupMemberDetailView.as_view(), name='groupmember-detail'),

    # 💸 Expenses
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<uuid:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),

    # 🔢 Expense splits
    path('splits/', ExpenseSplitListCreateView.as_view(), name='split-list-create'),
    path('splits/<int:pk>/', ExpenseSplitDetailView.as_view(), name='split-detail'),

    # 🧾 Payments
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),

    # 🗂️ Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),

    # 🔔 Notifications
    path('notifications/', NotificationListView.as_view(), name='notification-list'),

    # 📋 Activity Logs
    path('activity-logs/', ActivityLogListView.as_view(), name='activity-log-list'),
]

