from django.urls import path, include, reverse
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.site.login = login_required(admin.site.login)

urlpatterns = [
    path('accounts/', include('apps.accounts.urls', namespace="accounts")),
    path('dashboard/', include('apps.dashboard.urls', namespace="dashboard")),
    path("Ww33AVMWvekVt8UhxosX/YzWWxjPVfeI5j8UsJZzP/HL9eMqygOmEK1rQugoqY/2AaA8qIG35cA0dq0PisC/", admin.site.urls),
    path("", include('apps.portal.urls', namespace="portal" )),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls))
    )

handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'
handler403 = 'apps.core.views.permission_denied'
handler400 = 'apps.core.views.bad_request'
