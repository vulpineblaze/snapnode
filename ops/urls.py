from django.conf.urls import patterns, url

from ops import views ###

urlpatterns = patterns('',

    #url(r'^$', views.index, name='index'),
    url(r'^customer/$', views.index, name='index'),

    url(r'^$', views.home, name='home'),
    url(r'^customer/new_customer/$', views.new_customer, name='new_customer'),
    url(r'^customer/detail/(?P<node_id>\d+)/$', views.detail, name='detail'),
    url(r'^customer/edit/(?P<node_id>\d+)/$', views.edit, name='edit'),
    url(r'^customer/new_asset/(?P<node_id>\d+)/$', views.new_asset, name='new_asset'),

    # # ex: /polls/5/
    # url(r'^(?P<node_id>\d+)/$', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<node_id>\d+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<node_id>\d+)/vote/$', views.vote, name='vote'),

    # url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^logout/$', views.user_logout, name='logout'),

)
