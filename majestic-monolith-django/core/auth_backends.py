from threading import local

from django.contrib.auth.backends import ModelBackend

_stash = local()


class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, **credentials):
        ret = self._authenticate_by_phonenumber(**credentials)
        return ret

    def _authenticate_by_phonenumber(self, **credentials):
        phonenumber = credentials.get("phonenumber")
        password = credentials.get("password")

        if phonenumber:
            # import module from different domain
            from user.selectors import user_selector

            for user in user_selector.filter_users_by_phonenumber(phonenumber):
                if self._check_password(user, password):
                    return user
        return None

    def _check_password(self, user, password):
        ret = user.check_password(password)
        if ret:
            ret = self.user_can_authenticate(user)
            if not ret:
                self._stash_user(user)
        return ret

    @classmethod
    def _stash_user(cls, user):
        """Now, be aware, the following is quite ugly, let me explain:

        Even if the user credentials match, the authentication can fail because
        Django's default ModelBackend calls user_can_authenticate(), which
        checks `is_active`. Now, earlier versions of allauth did not do this
        and simply returned the user as authenticated, even in case of
        `is_active=False`. For allauth scope, this does not pose a problem, as
        these users are properly redirected to an account inactive page.

        This does pose a problem when the allauth backend is used in a
        different context where allauth is not responsible for the login. Then,
        by not checking on `user_can_authenticate()` users will allow to become
        authenticated whereas according to Django logic this should not be
        allowed.

        In order to preserve the allauth behavior while respecting Django's
        logic, we stash a user for which the password check succeeded but
        `user_can_authenticate()` failed. In the allauth authentication logic,
        we can then unstash this user and proceed pointing the user to the
        account inactive page.
        """
        global _stash
        ret = getattr(_stash, "user", None)
        _stash.user = user
        return ret

    @classmethod
    def unstash_authenticated_user(cls):
        return cls._stash_user(None)


class PasswordlessAuthenticationBackend(AuthenticationBackend):
    def authenticate(self, request, phonenumber, verification_success: bool):
        if phonenumber and verification_success:
            from user.selectors import user_selector

            for user in user_selector.filter_users_by_phonenumber(phonenumber):
                if self.user_can_authenticate(user):
                    return user
        return None
