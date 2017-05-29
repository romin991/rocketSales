"""zapdos_api URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('bases.urls')),
    url(r'', include('employees.urls')),
    url(r'', include('leads.urls')),
    url(r'', include('companies.urls')),
    url(r'', include('customers.urls')),
    url(r'', include('deals.urls')),
    url(r'', include('notes.urls')),
    url(r'', include('tasks.urls')),
    url(r'', include('events.urls')),
    url(r'', include('entities.urls')),
    url(r'', include('devices.urls')),
    url(r'', include('reports.urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),
]
