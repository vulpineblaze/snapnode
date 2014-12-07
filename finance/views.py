from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.

from core.models import Node, UserProfile
from django.core.mail import send_mail
from finance.forms import *

import itertools

def index(request):
    generic_html_dump = ""
    
    generic_html_dump += "<a href=\"bank_deposit\" >Bank Deposit Event</a><BR>"
    generic_html_dump += "<a href=\"new_bank_deposit\" >Create Bank Deposit Event</a><BR>"

    generic_html_dump += "<a href=\"expenditure\" >Expenditure Event</a><BR>"
    generic_html_dump += "<a href=\"new_expenditure\" >Create Expenditure Event</a><BR>"

    generic_html_dump += "<a href=\"payment_received\" >Payments received</a><BR>"
    generic_html_dump += "<a href=\"new_payment_received\" >Create Payments received</a><BR>"


    context = {'generic_html_dump': generic_html_dump}
    return render(request, 'finance/index.html', context)

def home(request):
    """  Starting page where User chooses what to do. """
    generic_html_dump = ""

    generic_html_dump += "<a href=\"bank_deposit\" >Bank Deposit Event</a><BR>"
    generic_html_dump += "<a href=\"new_bank_deposit\" >Create Bank Deposit Event</a><BR>"

    generic_html_dump += "<a href=\"expenditure\" >Expenditure Event</a><BR>"
    generic_html_dump += "<a href=\"new_expenditure\" >Create Expenditure Event</a><BR>"

    generic_html_dump += "<a href=\"payment_received\" >Payments received</a><BR>"
    generic_html_dump += "<a href=\"new_payment_received\" >Create Payments received</a><BR>"


    context = {'generic_html_dump': generic_html_dump}
    return render(request, 'finance/home.html', context)

def bank_deposit(request):
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
    return render(request, 'finance/bank_deposit.html', context)

def expenditure(request):
    node_list = []
    latest_node_list = Node.objects.order_by('-date_updated')
    # template = loader.get_template('core/index.html')

    for node in latest_node_list:
        for child in node.node_set.all():
            if(child.name == "flags"):
                if "|EXP|" in child.desc:
                    node_list.append(node.pk)

    queryset = Node.objects.filter(pk__in=node_list) 
    latest_node_list = queryset   

    context = {'latest_node_list': latest_node_list}
    return render(request, 'finance/expenditure.html', context)

def payment_received(request):
    node_list = []
    latest_node_list = Node.objects.order_by('-date_updated')
    # template = loader.get_template('core/index.html')

    for node in latest_node_list:
        for child in node.node_set.all():
            if(child.name == "flags"):
                if "|PR|" in child.desc:
                    node_list.append(node.pk)

    queryset = Node.objects.filter(pk__in=node_list) 
    latest_node_list = queryset   

    context = {'latest_node_list': latest_node_list}
    return render(request, 'finance/payment_received.html', context)

def new_bank_deposit(request):
    form_action = "/finance/new_bank_deposit/"

    if request.method == 'POST':
        form = NewBankDepositEventForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }

            BDE_node = Node.objects.create()
            bank_node = Node.objects.create()
            depositor_node = Node.objects.create()
            amount_node = Node.objects.create()
            flags_node = Node.objects.create()
            # customer_node = Node.objects.create()

            # record.save()

            BDE_node.desc = form.cleaned_data['desc']

            BDE_node.save()

            flags_node.parent = BDE_node
            flags_node.name = "flags"
            flags_node.desc = "|BDE|"

            flags_node.save()

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
            return HttpResponseRedirect('/finance/bank_deposit/detail/'+str(BDE_node.id))
    else:
        form = NewBankDepositEventForm()

    return render(request, 'finance/bank_deposit_detail.html', {'form': form,'action':'new_bank_deposit'})

def new_expenditure(request):
    form_action = "/finance/new_expenditure/"

    if request.method == 'POST':
        form = NewExpenditureForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }

            EXP_node = Node.objects.create()
            payto_node = Node.objects.create()
            amount_node = Node.objects.create()
            flags_node = Node.objects.create()
            # customer_node = Node.objects.create()

            # record.save()
            EXP_node.desc = form.cleaned_data['desc']

            EXP_node.save()

            flags_node.parent = EXP_node
            flags_node.name = "flags"
            flags_node.desc = "|EXP|"

            flags_node.save()

            payto_node.parent = EXP_node
            payto_node.name = "payto"
            payto_node.desc = form.cleaned_data['payto']

            payto_node.save()

            amount_node.parent = EXP_node
            amount_node.name = "amount"
            amount_node.desc = form.cleaned_data['amount']

            amount_node.save()
            #BDE_glue.save()

            form.save()
            return HttpResponseRedirect('/finance/expenditure/detail/'+str(EXP_node.id))
    else:
        form = NewExpenditureForm()

    return render(request, 'finance/expenditure_detail.html', {'form': form,'action':'new_expenditure'})

def new_payment_received(request):
    form_action = "/finance/new_payment_received/"

    if request.method == 'POST':
        form = NewPaymentReceivedForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }

            PR_node = Node.objects.create()
            payfrom_node = Node.objects.create()
            amount_node = Node.objects.create()
            flags_node = Node.objects.create()
            # customer_node = Node.objects.create()

            # record.save()
            PR_node.desc = form.cleaned_data['desc']
#            BDE_node.desc = form.cleaned_data['desc']

            PR_node.save()

            flags_node.parent = PR_node
            flags_node.name = "flags"
            flags_node.desc = "|PR|"

            flags_node.save()

            payfrom_node.parent = PR_node
            payfrom_node.name = "payfrom"
            payfrom_node.desc = form.cleaned_data['payfrom']

            payfrom_node.save()

            amount_node.parent = PR_node
            amount_node.name = "amount"
            amount_node.desc = form.cleaned_data['amount']

            amount_node.save()
            #BDE_glue.save()

            form.save()
            return HttpResponseRedirect('/finance/payment_received/detail/'+str(PR_node.id))
    else:
        form = NewPaymentReceivedForm()

    return render(request, 'finance/payment_received_detail.html', {'form': form,'action':'new_payment_received'})

def bank_deposit_detail(request, node_id):
    """  Page for viewing all aspects of a bank deposit. """
    iterator=itertools.count() ###

    node = get_object_or_404(Node, pk=node_id)
    return render(request, 'finance/bank_deposit_detail.html', {'node': node, 'iterator':iterator})

def expenditure_detail(request, node_id):
    """  Page for viewing all aspects of a expenditure. """
    iterator=itertools.count() ###

    node = get_object_or_404(Node, pk=node_id)
    return render(request, 'finance/expenditure_detail.html', {'node': node, 'iterator':iterator})

def payment_received_detail(request, node_id):
    """  Page for viewing all aspects of a payment received. """
    iterator=itertools.count() ###

    node = get_object_or_404(Node, pk=node_id)
    return render(request, 'finance/payment_received_detail.html', {'node': node, 'iterator':iterator})


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
