from django.shortcuts import render
from django.template import RequestContext, loader

# Create your views here.

from core.models import Node, UserProfile
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from finance.forms import *

def index(request):
    node_list = []
    latest_node_list = Node.objects.order_by('-date_updated')
    # template = loader.get_template('core/index.html')

    for node in latest_node_list:
        for child in node.node_set.all():
            if(child.name == "flags"):
            	if "|LINE ITEM|" in child.desc:
                	node_list.append(node.pk)

    queryset = Node.objects.filter(pk__in=node_list) 
    latest_node_list = queryset   

    context = {'latest_node_list': latest_node_list}
    return render(request, 'finance/index.html', context)

def invoices(request):
    """ """
    context = {}
    return render(request, 'finance/invoices.html', context)

def contact(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd['email'],
                ['throwemailhere0@gmail.com'],
            )
            return HttpResponseRedirect('../contact/thanks')
    else:
        form = InvoiceForm()
    return render(request, 'finance/contact.html', {'form': form})

def thanks(request):
    return HttpResponse("thanks\n")
