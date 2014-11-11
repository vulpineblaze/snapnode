from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'snapnode.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')), ##

    url(r'^$', 'core.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ticket/', include('ticket.urls')),
    url(r'^ops/', include('ops.urls')),
    url(r'^finance/', include('finance.urls')),
    url(r'^core/', include('core.urls')),
)
