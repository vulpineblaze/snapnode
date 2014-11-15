from django.conf.urls import patterns, url

from ops import views ###

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
<<<<<<< HEAD
    url(r'^new/$', views.new, name='new'),
=======
    url(r'^new/$', views.new_node, name='new_node'),
    url(r'^(?P<node_id>\d+)/new_sub_node/$', views.new_sub_node, name='new_sub_node'),
>>>>>>> d5e93c8afc58392903d19e578a9afcad6216bd7d
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