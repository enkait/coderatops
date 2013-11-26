from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User, Group

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^backend/', include('backend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^puzzle/', include('puzzle.urls')),
    url(r'^challenge/', include('challenge.urls')),
    url(r'^fblogin/', include('fblogin.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
