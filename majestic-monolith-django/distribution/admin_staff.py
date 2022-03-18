from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import (
    ValidationError,
)
from django.contrib.auth.views import AuthenticationForm

CustomUser = get_user_model()


class StaffAdminAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        if not user.is_superuser and not user.type == "SELLER":
            raise ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )


class StaffAdminSite(admin.AdminSite):
    site_header = 'Staff'
    index_title = 'Staff Site'
    site_url = None
    enable_nav_sidebar = False
    login_form = StaffAdminAuthenticationForm

    def has_permission(self, request):
        if request.user.is_authenticated:
            return (request.user.is_active and request.user.type == CustomUser.Types.STAFF) \
                   or request.user.is_superuser
        else:
            return False

    def get_app_list(self, request):
        ordering = {
            "shipping": 1,
            "distribution": 2,
        }
        app_dict = self._build_app_dict(request)
        # a.sort(key=lambda x: b.index(x[0]))
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list


staff_admin_site = StaffAdminSite(name='staff')
'''
Add url 

path('staff_admin/', staff_admin_site.site.urls)

'''