from django.contrib import admin
from django.conf.urls import url, include
from . import views
from personal_app.views import MyView,ReactView


urlpatterns = [
    # url('login/', MyView.as_view(), name='login'),
    url('login/', views.login, name="login"),
    url('signup/', views.signup, name="signup"),
    url('getCountdown/', views.get_countdown, name="get_countdown"),
    url('wel/', ReactView.as_view(), name="something"),
    # url('mongo_auth/', include('mongo_auth.urls')),
    # url('mongo_auth/', ReactView.as_view(), name="something"),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
]