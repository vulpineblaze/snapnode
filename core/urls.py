from django.conf.urls import patterns, url

from core import views ###

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    # ex: /polls/5/
    url(r'^(?P<node_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<node_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<node_id>\d+)/vote/$', views.vote, name='vote'),

    url(r'^$', views.index, name='index'), # ADD NEW PATTERN!

    url(r'^new_node/$', views.new_node, name='new_node'), # 
    url(r'^new_asset/$', views.new_asset, name='new_asset'), # new_asset
    url(r'^(?P<node_id>\d+)/new_sub_node/$', views.new_sub_node, name='new_sub_node'), # new_sub_node


    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

)