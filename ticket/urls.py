from django.conf.urls import patterns, url

from ticket import views ###

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),    

    # url(r'^home/$', views.home, name='home'),
    
    url(r'^index/$', views.index, name='index'),
    
    url(r'^new_ticket/$', views.new_ticket, name='new_ticket'),
    
    url(r'^detail/(?P<node_id>\d+)/$', views.detail, name='detail'),

    
    url(r'^edit/$', views.edit, name='edit'),
    
    url(r'^new_event/$', views.new_event, name='new_event'),
    
    # url(r'^index/$', views.index, name='index'),
    
    # url(r'^index/$', views.index, name='index'),
    
    # url(r'^index/$', views.index, name='index'),
    
    # url(r'^index/$', views.index, name='index'),

    # # # ex: /polls/5/
    # url(r'^(?P<node_id>\d+)/$', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<node_id>\d+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<node_id>\d+)/vote/$', views.vote, name='vote'),

    # url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^logout/$', views.user_logout, name='logout'),
    # url(r'^logout/$', views.user_logout, name='logout'),

)