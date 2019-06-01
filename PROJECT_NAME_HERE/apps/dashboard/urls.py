from . import views as v
from apps.accounts.views import ActivateUser, EnableUser, RemoveUser, \
    SuspendUser
from django.contrib.auth.views import TemplateView
from django.urls import include, path

app_name = "dashboard"

urlpatterns = [
    path("users/browse/", v.BrowseUsersView, name="list-users"),
    path("profile/", v.UserEditView, name="profile"),
    path("settings/", v.ManageSiteView, name="site-management"),
    path("settings/users/manage/new/", v.UserCreationView, name="create-user"),
    path("settings/users/manage/edit/<int:userid>/", v.UserEditView, name="edit-user"),
    path("settings/users/manage/suspend/<int:userid>/", SuspendUser, name="suspend-user"),
    path("settings/users/manage/enable/<int:userid>/", EnableUser, name="enable-user"),
    path("settings/users/manage/remove/<int:userid>/", RemoveUser, name="remove-user"),
    path("settings/users/manage/activate/<int:userid>/", ActivateUser, name="activate-user"),
    path("", v.IndexView, name="home"),
]
