from django.contrib.auth.models import BaseUserManager

from core.managers import CommonBaseManager
class BaseUserManager(BaseUserManager,CommonBaseManager):
    def create_user(
        self,
        email,
        password,
        first_name=None,
        last_name=None,
        is_staff=False,
    ):

        user = self.model(
            email=self.normalize_email(email.lower()),
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None):
        user = self.create_user(
            email=email,
            is_staff=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user
