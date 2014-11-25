from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.

from core.models import Node, UserProfile
from django.core.mail import send_mail
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


def documentation(request):
    generic_html_dump = ""
    
    generic_html_dump += "<a href=\"Bank_Deposit_Event\" >Bank Deposit Event</a><BR>"
    generic_html_dump += "<a href=\"Expenditure_Event\" >Expenditure Event</a><BR>"
    #generic_html_dump += "<a href=\"Contact_list\" >Documents</a><BR>"
    generic_html_dump += "<a href=\"payment_received\" >Payments received</a><BR>"
    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'core/generic.html', context)


"""
def new_document(request): #create new documents
	form_action = "/finance/documentation/new_document

"""
def home(request):
    """  Starting page where User chooses what to do. """

    generic_html_dump = ""

    generic_html_dump += "<P> In home.html </P>"
    generic_html_dump += "<a href=\"documentation\" >documentation</a><BR>"
    generic_html_dump += "<a href=\"new_document\" >New document</a><BR>"
    generic_html_dump += "<a href=\"invoices\" >invoices</a><BR>"
    generic_html_dump += "<a href=\"index\" >UNDECIDED FEATURE</a><BR>"

    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'core/generic.html', context)


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
