from django.contrib import admin
from .models import (
    User,
    UserProfile,
    Group,
    GroupMember,
    GroupChatMessage,
    Category,
    Expense,
    ExpenseSplit,
    Payment,
    Notification,
    ActivityLog,
)

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(GroupChatMessage)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(ExpenseSplit)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(ActivityLog)
