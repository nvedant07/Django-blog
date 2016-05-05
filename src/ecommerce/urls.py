"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'shop.views.firstpage',name='firstpage'),
   url(r'^signin$', 'shop.views.signin',name='signin'),
   url(r'^signup$', 'shop.views.signup',name='signup'),
   url(r'^signupvalidation$', 'shop.views.signupvalidation',name='signupvalidation'),
   url(r'^home$', 'shop.views.home',name='home'),
   url(r'^logout$', 'shop.views.Logout',name='logout'),
    url(r'^forgot$', 'shop.views.forgotpassword',name='forgot'),
     url(r'^change$', 'shop.views.changepassword',name='change'),
     url(r'^delete$', 'shop.views.delaccount',name='delete'),
      url(r'^write$', 'shop.views.write',name='write'),
    url(r'^myblogs$', 'shop.views.myblogs',name='myblogs'),
    url(r'^read', 'shop.views.read',name='read'),
    url(r'^deleteblog', 'shop.views.deleteblog',name='deleteblog'),
     url(r'^editblog$', 'shop.views.editblog',name='editblog'),
]
