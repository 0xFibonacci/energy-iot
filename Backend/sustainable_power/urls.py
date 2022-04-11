from django.conf.urls import url
from django.urls import include
from sustainable_power import views

urlpatterns = [
    url(r'^api/users$', views.user_list),
    url(r'^api/users/(?P<pk>[0-9]+)$', views.user_detail),
    url(r'^api/devices$', views.device_list),
    url(r'^api/devices/(?P<pk>[0-9]+)$', views.device_detail),
    url(r'^api/prices$', views.price_list),
    url(r'^api/emissions$', views.emission_list),
    url(r'^api/prognosed-emissions$', views.prognosed_emission_list),
    url(r'^api/bluetooth-devices$', views.bluetooth_devices),

    # Authentication
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
