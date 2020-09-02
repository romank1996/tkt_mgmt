"""tkt_mgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from register import views as v
from adm import views as adm_v
from engineer import views as eng_v
from usr import views as usr_v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('app/', include('app.urls')),
    path('register/', v.register, name='register'),
    path('adm/', adm_v.index, name='adm'),
    path('engineer/', eng_v.index, name='engineer'),
    path('usr/', usr_v.index, name='usr'),
    path('', include('django.contrib.auth.urls')),
]
