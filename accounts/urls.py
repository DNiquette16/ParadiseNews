from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns=[
 url(r'^make-account/$', views.make_account_view, name='make-account'),
 url(r'^signin/$', views.signin_view, name='signin'),
 url(r'^logout/$', views.logout_view, name='logout')
]