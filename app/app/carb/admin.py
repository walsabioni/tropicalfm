from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html_join

from constance import config

from .models import GoogleCalendarShow, ScheduledBroadcast, User
from .tasks import sync_google_calendar_api


class CarbUserAdmin(UserAdmin):
    save_on_top = True
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'email')}),
        ('Permissions', {'fields': ('harbor_auth', 'is_active', 'is_superuser', 'groups',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'harbor_auth', 'is_superuser')
    list_filter = ('is_superuser', 'is_active', 'groups')
    readonly_fields = ('last_login', 'date_joined')

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        return super().save_model(request, obj, form, change)


class GoogleCalendarShowAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'start', 'end', 'users_list')
    fields = ('title', 'start', 'end', 'users_list')
    list_filter = ('users', 'start')
    date_hierarchy = 'start'

    def get_urls(self):
        return [path('sync/', self.admin_site.admin_view(self.sync_view),
                name='carb_googlecalendarshow_sync')] + super().get_urls()

    def users_list(self, obj):
        return format_html_join(
            ', ', '<a href="{}">{}</a>',
            ((reverse('admin:carb_user_change', args=(u.id,)), u.username) for u in obj.users.all())
        ) or 'none'
    users_list.short_description = 'User(s)'

    def sync_view(self, request):
        if not self.has_view_permission(request):
            raise PermissionDenied

        sync_google_calendar_api()
        messages.add_message(request, messages.INFO,
                             "Google Calendar is currently being sync'd. Please refresh this page in a few moments.")
        return redirect('admin:carb_googlecalendarshow_changelist')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return config.GOOGLE_CALENDAR_ENABLED


class ScheduledBroadcastAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('asset_path', 'scheduled_time', 'play_status', 'task_id')
    readonly_fields = ('play_status', 'task_id')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Can only edit asset_path on creation
            return self.readonly_fields + ('asset_path',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.queue()


admin.site.unregister(Group)
admin.site.register(User, CarbUserAdmin)
admin.site.register(GoogleCalendarShow, GoogleCalendarShowAdmin)
admin.site.register(ScheduledBroadcast, ScheduledBroadcastAdmin)
