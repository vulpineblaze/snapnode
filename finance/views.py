from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.

from core.models import Node, UserProfile
from django.core.mail import send_mail
from finance.forms import *

def bank_deposit_event_index(request):
    node_list = []
    latest_node_list = Node.objects.order_by('-date_updated')
    # template = loader.get_template('core/index.html')

    for node in latest_node_list:
        for child in node.node_set.all():
            if(child.name == "flags"):
                if "|BDE|" in child.desc:
                    node_list.append(node.pk)

    queryset = Node.objects.filter(pk__in=node_list) 
    latest_node_list = queryset   

    context = {'latest_node_list': latest_node_list}
    return render(request, 'finance/bank_deposit_event_index.html', context)


def index(request):
    generic_html_dump = ""
    
    generic_html_dump += "<a href=\"bank_deposit_event_index\" >Bank Deposit Event</a><BR>"
    generic_html_dump += "<a href=\"new_bank_deposit_event_index\" >Create Bank Deposit Event</a><BR>"

    generic_html_dump += "<a href=\"expenditure_event_index\" >Expenditure Event</a><BR>"
    generic_html_dump += "<a href=\"new_expenditure_event\" >Create Expenditure Event</a><BR>"

    generic_html_dump += "<a href=\"payment_received_index\" >Payments received</a><BR>"
    generic_html_dump += "<a href=\"new_payment_received\" >Create Payments received</a><BR>"


    context = {'generic_html_dump': generic_html_dump}
    return render(request, 'finance/index.html', context)

#def Bank_Deposit_Event_detail(request, node_id):
#    """  Page for viewing all aspects of a ticket. """
#    iterator=itertools.count() ###

#    node = get_object_or_404(Node, pk=node_id)
#    return render(request, 'finance/bank_deposit_event/detail.html', {'node': node, 'iterator':iterator})

def new_bank_deposit_event(request):
    form_action = "/finance/new_bank_deposit_event/"

    if request.method == 'POST':
        form = NewBankDepositEventForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }

            BDE_node = Node.objects.create()
            ID_node = Node.objects.create()
            date_node = Node.objects.create()#date of event made
            bank_node = Node.objects.create()
            depositor_node = Node.objects.create()
            amount_node = Node.objects.create()
            flags_node = Node.objects.create()
            # customer_node = Node.objects.create()

            # record.save()
            BDE_node.name = form.cleaned_data['ID']
#            BDE_node.desc = form.cleaned_data['desc']

            BDE_node.save()

	#ID number of event
            ID_node.parent = BDE_node
            ID_node.name = "ID"
            ID_node.desc = form.cleaned_data['ID']

            ID_node.save()

            flags_node.parent = BDE_node
            flags_node.name = "flags"
            flags_node.desc = "|BDE|"

            flags_node.save()

            date_node.parent = BDE_node
            date_node.name = "date"
            date_node.desc = form.cleaned_data['date']

            date_node.save()

            bank_node.parent = BDE_node
            bank_node.name = "bank name"
            bank_node.desc = form.cleaned_data['bank']

            bank_node.save()

            depositor_node.parent = BDE_node
            depositor_node.name = "depositor"
            depositor_node.desc = form.cleaned_data['depositor']

            depositor_node.save()

            amount_node.parent = BDE_node
            amount_node.name = "amount"
            amount_node.desc = form.cleaned_data['amount']

            amount_node.save()

           # BDE_glue = Glue.objects.create(parent=form.cleaned_data['BDE'],
           #                                     child=ticket_node,
           #                                     name="BDE information")

            # asset_set = form.cleaned_data['assets']

            # customer_glue.parent = form.cleaned_data['customer']
            # customer_glue.child = ticket_node

            #BDE_glue.save()

            form.save()
            return HttpResponseRedirect('/finance/bank_deposit_event_detail/'+str(BDE_node.id))
    else:
        form = NewBankDepositEventForm()

    return render(request, 'finance/bank_deposit_event_detail.html', {'form': form,'action':'new_bank_deposit_event'})

def bank_deposit_event_detail(request):
    """  Page for viewing all aspects of a ticket. """
    iterator=itertools.count() ###
    node = get_object_or_404(Node, pk=node_id)
    return render(request, 'finance/bank_deposit_event_detail.html', {'node': node, 'iterator':iterator})


def home(request):
    """  Starting page where User chooses what to do. """
    """    generic_html_dump = ""
    generic_html_dump += "<P> In home.html </P>"
    generic_html_dump += "<a href=\"documentation\" >documentation</a><BR>"
    generic_html_dump += "<a href=\"new_document\" >New document</a><BR>"
    generic_html_dump += "<a href=\"invoices\" >invoices</a><BR>"
    generic_html_dump += "<a href=\"index\" >UNDECIDED FEATURE</a><BR>"

    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'core/generic.html', context)
    """
    generic_html_dump = ""

    generic_html_dump += "<a href=\"bank_deposit_event_index\" >Bank Deposit Event</a><BR>"
    generic_html_dump += "<a href=\"new_bank_deposit_event\" >Create Bank Deposit Event</a><BR>"

    generic_html_dump += "<a href=\"expenditure_event_index\" >Expenditure Event</a><BR>"
    generic_html_dump += "<a href=\"new_expenditure_event\" >Create Expenditure Event</a><BR>"

    generic_html_dump += "<a href=\"payment_received_index\" >Payments received</a><BR>"
    generic_html_dump += "<a href=\"new_payment_received\" >Create Payments received</a><BR>"


    context = {'generic_html_dump': generic_html_dump}
    return render(request, 'core/generic.html', context)


def invoices(request):
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
