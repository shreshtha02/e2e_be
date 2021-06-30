from django.contrib import admin
from django.conf.urls import url, include
from . import views
from personal_app.views import MyView,ReactView


urlpatterns = [
    # url('login/', MyView.as_view(), name='login'),
    url('wel/', ReactView.as_view(), name="something"),
    url('mongo_auth/', include('mongo_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
]