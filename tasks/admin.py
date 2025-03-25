from django.contrib import admin
from .models import User, Task


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin view for managing Users.
    """
    list_display = ('id', 'username', 'email', 'mobile', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'mobile')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-date_joined',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin view for managing Tasks.
    """
    list_display = ('id', 'name', 'status', 'task_type', 'created_at', 'completed_at')
    search_fields = ('name', 'description')
    list_filter = ('status', 'task_type', 'created_at')
    ordering = ('-created_at',)
    autocomplete_fields = ('assigned_user',)  # Enables autocomplete for large user lists
    date_hierarchy = 'created_at'  # Adds date navigation at the top

    fieldsets = (
        ('Task Details', {'fields': ('name', 'description', 'task_type', 'status')}),
        ('Assignment', {'fields': ('assigned_user',)}),
        ('Timestamps', {'fields': ('created_at', 'completed_at')}),
    )

    readonly_fields = ('created_at', 'completed_at')  # Prevents manual date modification


# Register models in Django Admin
admin.site.site_header = "Task Management Admin"
admin.site.site_title = "Task Admin"
admin.site.index_title = "Welcome to Task Management Panel"
