from django.conf import settings
from rolepermissions.roles import get_user_roles

from .constants import permissions as p
from .utils import getOptions


def site_meta_processor(request):
    user_roles = False

    if request.user.is_authenticated:
        user_roles = [role.title for role in get_user_roles(request.user)]

    data = {
        'meta': {
            "debug": settings.DEBUG,
            "application_version": settings.APPLICATION_VERSION
        },
        'user_roles': user_roles,
        'constants': {
            'permissions': p
        },
        'is_user_switched': request.session.get("%s_is_switched" % settings.LOGIN_AS_SESSION_FLAG, 0)
    }
    options = getOptions()
    for option in options:
        data['meta'][option] = options[option]

    return data
