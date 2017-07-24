from django.contrib.auth import views as auth_views
from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'^signup$', views.signup_view, name='accounts_signup'),
    url(r'^login$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='auth_login'),
    url(r'^logout$', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='auth_logout'),
    url(r'^profile$', views.profile_view, name='accounts_profile')
]
