from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.admin_filters import UserIsActiveFilter

from .events import UserEventsEmitter
from .models import CustomUser, UserProfileDriver, UserProfileStaff
from .services import UserDeleteService, UserDTO
from .slack_notification import SlackNotificationUser


class ProfileDriverModelForm(forms.ModelForm):
    class Meta:
        model = UserProfileDriver
        fields = "__all__"


class UserProfileDriverInline(admin.StackedInline):
    model = UserProfileDriver
    form = ProfileDriverModelForm


class ProfileStaffModelForm(forms.ModelForm):
    class Meta:
        model = UserProfileStaff
        fields = "__all__"


class UserProfileStaffInline(admin.StackedInline):
    model = UserProfileStaff
    form = ProfileStaffModelForm


class CustomUserAdmin(UserAdmin):
    actions = ["unregister", "ban_permanently"]
    search_fields = ("username", "phonenumber", "=uuid")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email", "phonenumber", "type")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )
    list_display = (
        "username",
        "uuid",
        "email",
        "phonenumber",
        "is_active",
        "banned",
        "date_joined",
        "is_staff",
        "type",
    )
    list_filter = ["banned", UserIsActiveFilter, "type"]

    inlines = [UserProfileDriverInline, UserProfileStaffInline]

    def save_model(self, request, obj, form, change):
        super(CustomUserAdmin, self).save_model(request, obj, form, change)
        from user.utils_user import delete_user_profile_cache

        delete_user_profile_cache(obj.uuid)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="Unregister User")
    def unregister(self, request, queryset):
        for user in queryset:
            user_dto = UserDTO(user=user)
            UserDeleteService(user_dto).unregister()

            # event emitter
            user_data = {"uuid": user.uuid.hex}
            UserEventsEmitter().user_deactivated(user_data)

            # slack notification
            SlackNotificationUser().deacivated(user)

    @admin.action(description="Ban user")
    def ban_permanently(self, request, queryset):
        for user in queryset:
            user_dto = UserDTO(user=user)
            UserDeleteService(user_dto).ban()

            # event emitter
            user_data = {"uuid": user.uuid.hex}
            UserEventsEmitter().user_banned(user_data)

            SlackNotificationUser().banned(user)


admin.site.register(CustomUser, CustomUserAdmin)
