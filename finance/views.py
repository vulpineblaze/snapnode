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
            	if "|BDE|" in child.desc:
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

def Bank_Deposit_Event_detail(request, node_id):
    """  Page for viewing all aspects of a ticket. """
    iterator=itertools.count() ###

    node = get_object_or_404(Node, pk=node_id)
    return render(request, 'finance/Bank_Deposit_Event/detail.html', {'node': node, 'iterator':iterator})


"""
def new_document(request): #create new documents
	form_action = "/finance/documentation/new_document

"""
def Bank_Deposit_Event(request):
    generic_html_dump = ""

    generic_html_dump += "<a href=\"new_Bank_Deposit_Event\" >Bank Deposit Event</a><BR>"
    generic_html_dump += "<a href=\"details\" >list of Bank Deposit Event</a><BR>"


def new_Bank_Deposit_Event(request):
   #   Page for making new Bank_Deposit_Event documents. 
	#BDE = Bank Deposit Event
    form_action = "/finance/Bank_Deposit_Event/new_Bank_Deposit_Event/"

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
            amount_deposited_node = Node.objects.create()
            # customer_node = Node.objects.create()

            # record.save()
            BDE_node.name = form.cleaned_data['name']
            BDE_node.desc = form.cleaned_data['desc']

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
            date_node.desc = from.cleaned_data['date']

            date_node.save()

            bank_node.parent = BDE_node
            bank_node.name = "bank name"
            bank_node.desc = form.cleaned_data['bank']

            bank_node.save()

            depositor_node.parent = BDE_node
            depositor_node.name = "depositor"
            depositor_node.desc = form.cleaned_data['bank']

            depositor_node.save()

            amount_deposited_node.parent = BDE_node
            amount_deposited__node.name = "amount"
            amount_deposited_node.desc = form.cleaned_data['bank']

            amount_deposited_node.save()



           # BDE_glue = Glue.objects.create(parent=form.cleaned_data['BDE'],
           #                                     child=ticket_node,
           #                                     name="BDE information")

            # asset_set = form.cleaned_data['assets']

            # customer_glue.parent = form.cleaned_data['customer']
            # customer_glue.child = ticket_node

            #BDE_glue.save()

            form.save()
            return HttpResponseRedirect('/finance/bank_deposit_event/detail/'+str(BDE_node.id))
    else:
        form = NewFormBankDepositEvent()

    return render(request, 'bank_deposit_event/detail.html', {'form': form,'action':'new_BDE'})



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
