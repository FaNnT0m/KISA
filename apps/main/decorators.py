from django.conf import settings
from django.contrib.auth.decorators import user_passes_test


def group_required(*group_names):
    """
    Ocupa que el usuario ser parte de al menos uno
    de los grupos que se pasen como argumento
    """

    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)):
                return True

        return False

    return user_passes_test(in_groups)

def anonymous_required(function=None, redirect_url=None):
    """
    Ocupa que el usuario no este loggeado
    """
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)

    return actual_decorator