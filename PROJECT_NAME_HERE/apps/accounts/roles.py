from rolepermissions.roles import AbstractUserRole
from apps.core.constants import permissions as p


class Admin(AbstractUserRole):

    available_permissions = {
        p.READ_USERS: True,
        p.EDIT_USERS: True,
        p.DELETE_USERS: True,
        p.SUSPEND_USERS: True,
        p.EDIT_FORM: True,
        p.ASSIGN_FORM: True,
    }

    display_name = 'admin'
    title = "Admin"


class Subscriber(AbstractUserRole):

    available_permissions = {
        p.READ_FORM: True
    }

    display_name = 'subscriber'
    title = "Subscriber"

class DemoUser(AbstractUserRole):

    available_permissions = {
        p.READ_FORM: True
    }

    display_name = "demo_user"
    title = "Demo User"
