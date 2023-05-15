from django.contrib.auth.models import User


def auto_approve(user: User):
    return user and user.is_staff


def can_see_unvalidated(user: User):
    return user and user.is_staff