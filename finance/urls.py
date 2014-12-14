from django.conf.urls import patterns, url

from finance import views ###

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),

    url(r'^index/$', views.index, name='index'),
    url(r'^invoices/$', views.invoices),
    url(r'^contact/$', views.contact),
    url(r'^contact/thanks$', views.thanks),
    url(r'^bank_deposit/$', views.bank_deposit),
    url(r'^bank_deposit/detail/(?P<node_id>\d+)/$', views.bank_deposit_detail),
    url(r'^new_bank_deposit/$', views.new_bank_deposit),
    url(r'^bank_deposit/edit/(?P<node_id>\d+)/$', views.bank_deposit_edit),
    url(r'^expenditure/$', views.expenditure),
    url(r'^expenditure/detail/(?P<node_id>\d+)/$', views.expenditure_detail),
    url(r'^expenditure/edit/(?P<node_id>\d+)/$', views.expenditure_edit),
    url(r'^new_expenditure/$', views.new_expenditure),
    url(r'^payment_received/$', views.payment_received),
    url(r'^payment_received/detail/(?P<node_id>\d+)/$', views.payment_received_detail),
    url(r'^new_payment_received/$', views.new_payment_received),
    url(r'^payment_received/edit/(?P<node_id>\d+)/$', views.payment_received_edit),

    url(r'^bank_deposit/pdf/$', views.pdf_maker, name='pdf'),
#    url(r'^bank_deposit_event_detail/$', views.bank_deposit_event_detail),
#    url(r'^bank_deposit_event_edit$', views.bank_deposit_event_edit),

)
