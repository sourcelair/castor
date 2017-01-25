"""castor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from rest_framework import routers

from docker_events.views import DockerEventViewSet
from docker_servers.views import DockerServerViewSet
from web.views import home
from web.views import signin
from web.views import webhooks
from web.views import webhook
from webhooks.views import DeliveryViewSet
from webhooks.views import WebHookDeliveryViewSet
from webhooks.views import WebHookViewSet


router = routers.DefaultRouter()
router.register(r'docker-events', DockerEventViewSet)
router.register(r'docker-servers', DockerServerViewSet)
router.register(r'webhooks', WebHookViewSet)
router.register(r'deliveries', DeliveryViewSet)
router.register(
    r'webhooks/(?P<webhook_id>\d+)/deliveries',
    WebHookDeliveryViewSet,
    base_name='webhook-delivery'
)

urlpatterns = [
    url(r'^auth/', include('social_django.urls', namespace='auth')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^$', home),
    url(r'^signin/$', signin, name='signin'),
    url(r'^signout/$', logout_then_login, name='signout'),
    url(r'^webhooks/?$', webhooks, name='webhooks'),
    url(r'^webhooks/(?P<webhook_id>\d+)/?$', webhook, name='webhook'),
]
