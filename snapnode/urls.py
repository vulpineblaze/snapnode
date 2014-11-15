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
<<<<<<< HEAD
    url(r'^core/', include('core.urls')),
=======
    url(r'^pagetest/', include('pagetest.urls')),
>>>>>>> d5e93c8afc58392903d19e578a9afcad6216bd7d
)
