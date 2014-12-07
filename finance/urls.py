from django.conf.urls import patterns, url

from finance import views ###

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),

    url(r'^index/$', views.index, name='index'),
    # # ex: /polls/5/
    # url(r'^(?P<node_id>\d+)/$', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<node_id>\d+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<node_id>\d+)/vote/$', views.vote, name='vote'),

    # url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^invoices/$', views.invoices),
    url(r'^contact/$', views.contact),
    url(r'^bank_deposit/$', views.bank_deposit),
    url(r'^contact/thanks$', views.thanks),
    url(r'^bank_deposit/detail/(?P<node_id>\d+)/$', views.bank_deposit_detail),
    url(r'^new_bank_deposit/$', views.new_bank_deposit),
#    url(r'^bank_deposit_event_detail/$', views.bank_deposit_event_detail),
#    url(r'^bank_deposit_event_edit$', views.bank_deposit_event_edit),

)
