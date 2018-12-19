"""mySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from app1 import views as v

urlpatterns = [
    path('', v.home, name='landing'),
    path('home.html', v.home, name='home'),
    path('sports.html', v.sports, name='sports'),
    path('politics.html', v.politics, name='politics'),
    path('business.html', v.business, name='business'),
    path('profile.html', v.profile, name='profile'),
    #path('signin.html', v.signin, name='signin'),
    #path('make-account.html', v.makeAccount, name='makeAccount'),
    url(r'^accounts/',include('accounts.urls')), 
    url(r'^post/(?P<pk>[0-9]+)/like/$', v.post_like, name='post_like'),
    #url(r'^(?P<source>[a-z]+)/post/(?P<pk>[0-9]+)/like/$', v.post_like, name='post_like'),)
    url(r'^post/(?P<pk>[0-9]+)/dislike/$', v.post_dislike, name='post_dislike'),
    url(r'^admin/', admin.site.urls),
    url(r'^user_search/$', v.user_search, name='user_search')
]


