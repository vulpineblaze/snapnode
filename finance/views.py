from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.

from core.models import Node, UserProfile
from django.core.mail import send_mail
from finance.forms import *
from finance.pdf import *

import itertools
import time

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

def invoices(request):
    node_list = []
    latest_node_list = Node.objects.order_by('-date_updated')
    # template = loader.get_template('core/index.html')

    for node in latest_node_list:
        for child in node.node_set.all():
            if(child.name == "flags"):
                if "|INVOICE|" in child.desc:
                    node_list.append(node.pk)

    queryset = Node.objects.filter(pk__in=node_list) 
    latest_node_list = queryset   

    month = int(time.strftime("%m"))
    if month == 1:
        month = 12
    elif month > 1:
        month -= 1
    day = int(time.strftime("%d"))
    year = int(time.strftime("%Y"))
    date = (month, day, year, 0, 0, 0, 0, 0, 0)
    date = time.mktime(date)
    due = time.strftime("%m/%d/%Y", time.gmtime(date))

    context = {'latest_node_list': latest_node_list, 'due': due}
    return render(request, 'finance/invoices.html', context)

def invoices_detail(request, node_id):
    """  Page for viewing all aspects of an invoice. """
    iterator=itertools.count() ###

    node = get_object_or_404(Node, pk=node_id)
    parent = node.parent
    return render(request, 'finance/detail.html', {'node': node, 'parent': parent, 'iterator':iterator})

def edit_invoices(request, node_id):
    """  Page for editing an invoice. """

    form_action = "/finance/invoices/edit/" + str(node_id)

    invoice_node = get_object_or_404(Node, pk=node_id)
    cost_other_node = Node.objects.get(parent=invoice_node, name='cost_other')
    status_node = Node.objects.get(parent=invoice_node, name='status')
    print_date_node = Node.objects.get(parent=invoice_node, name='print_date')

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():

            invoice_node.desc = form.cleaned_data['desc']

            invoice_node.save()         
            
            cost_other_node.desc = form.cleaned_data['cost_other']

            cost_other_node.save()

            status_node.desc = form.cleaned_data['status']
            status_node.save()

            if status_node.desc == 'Printed':
                if print_date_node.desc == ' ':
                    print_date_node.desc = time.strftime("%m/%d/%Y")

                    print_date_node.save()

                    new_invoice_node = Node.objects.create()
                    in_flag_node = Node.objects.create()
                    date_node = Node.objects.create()
                    new_cost_other_node = Node.objects.create()
                    new_status_node = Node.objects.create()
                    new_print_date_node = Node.objects.create()

                    new_invoice_node.parent = invoice_node.parent
                    new_invoice_node.name = "invoice"
                    new_invoice_node.desc = " "

                    new_invoice_node.save()

                    in_flag_node.parent = new_invoice_node
                    in_flag_node.name = "flags"
                    in_flag_node.desc = "|INVOICE|"

                    in_flag_node.save()

                    date_node.parent = new_invoice_node
                    date_node.name = "date"
                    date_node.desc = time.strftime("%m/%d/%Y")

                    date_node.save()            
                    
                    new_cost_other_node.parent = new_invoice_node
                    new_cost_other_node.name = "cost_other"
                    new_cost_other_node.desc = ""

                    new_cost_other_node.save()

                    new_status_node.parent = new_invoice_node
                    new_status_node.name = "status"
                    new_status_node.desc = "Open"

                    new_status_node.save()

                    new_print_date_node.parent = new_invoice_node
                    new_print_date_node.name = "print_date"
                    new_print_date_node.desc = " "

                    new_print_date_node.save()

            return HttpResponseRedirect('/finance/invoices/detail/'+str(invoice_node.id))
    else:
        form = InvoiceForm( initial = { 'invoice':invoice_node.desc,
                                            'cost_other':cost_other_node.desc,
                                            'status':status_node.desc
                                } )
    return render(request, 'finance/detail.html', {'form': form,'action':'edit'})

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
        form = NewBankDepositForm(request.POST)
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
        form = NewBankDepositForm()

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

def bank_deposit_edit(request, node_id):

    latest_node_list = Node.objects.order_by('-date_updated')
    node_list = []

    form_action = "/finance/bank_deposit/edit/" + str(node_id)

    BDE_node = get_object_or_404(Node, pk=node_id)
    bank_node = Node.objects.get(parent=BDE_node,name='bank name')
    depositor_node = Node.objects.get(parent=BDE_node,name='depositor')
    amount_node = Node.objects.get(parent=BDE_node,name='amount')

    if request.method == 'POST':
        form = NewBankDepositForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }

            # record.save()
            BDE_node.desc = form.cleaned_data['desc']
            BDE_node.save()

            bank_node.desc = form.cleaned_data['bank']
            bank_node.save()

            depositor_node.desc = form.cleaned_data['depositor']
            depositor_node.save()

            amount_node.desc = form.cleaned_data['amount']
            amount_node.save()


            # form.save()
            return HttpResponseRedirect('/finance/bank_deposit/detail/'+str(BDE_node.id))
    else:

        form = NewBankDepositForm( initial = { 'desc':BDE_node.desc,
                                            'depositor':depositor_node.desc,
                                            'amount':amount_node.desc,
                                            'bank':bank_node.desc,
                                } )

    return render(request, 'finance/bank_deposit_detail.html', {'form': form,'action':'edit'})

def expenditure_edit(request, node_id):

    latest_node_list = Node.objects.order_by('-date_updated')
    node_list = []

    form_action = "/finance/expenditure/edit/" + str(node_id)

    EXP_node = get_object_or_404(Node, pk=node_id)
    payto_node = Node.objects.get(parent=EXP_node,name='payto')
    amount_node = Node.objects.get(parent=EXP_node,name='amount')

    if request.method == 'POST':
        form = NewExpenditureForm(request.POST)
        if form.is_valid():
            EXP_node.desc = form.cleaned_data['desc']
            EXP_node.save()

            payto_node.desc = form.cleaned_data['payto']
            payto_node.save()

            amount_node.desc = form.cleaned_data['amount']
            amount_node.save()

            # form.save()
            return HttpResponseRedirect('/finance/expenditure/detail/'+str(EXP_node.id))
    else:

        form = NewExpenditureForm( initial = { 'desc':EXP_node.desc,
                                            'payto':payto_node.desc,
                                            'amount':amount_node.desc,
                                } )

    return render(request, 'finance/expenditure_detail.html', {'form': form,'action':'edit'})

def payment_received_edit(request, node_id):

    latest_node_list = Node.objects.order_by('-date_updated')
    node_list = []

    form_action = "/finance/new_payment_received/edit/" + str(node_id)

    PR_node = get_object_or_404(Node, pk=node_id)
    payfrom_node = Node.objects.get(parent=PR_node,name='payfrom')
    amount_node = Node.objects.get(parent=PR_node,name='amount')

    if request.method == 'POST':
        form = NewPaymentReceivedForm(request.POST)
        if form.is_valid():
            PR_node.desc = form.cleaned_data['desc']
            PR_node.save()

            payfrom_node.desc = form.cleaned_data['payfrom']
            payfrom_node.save()

            amount_node.desc = form.cleaned_data['amount']
            amount_node.save()

            # form.save()
            return HttpResponseRedirect('/finance/payment_received/detail/'+str(PR_node.id))
    else:
        form = NewPaymentReceivedForm( initial = { 'desc':PR_node.desc,
                                            'payfrom':payfrom_node.desc,
                                            'amount':amount_node.desc,
                                } )

    return render(request, 'finance/payment_received_detail.html', {'form': form,'action':'edit'})


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

def bd_pdf(request):
    """ Calls the reportlab code in pdf.py for generate a pdf. """

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

    return bank_depo_pdf(request, latest_node_list)

def exp_pdf(request):
    """ Calls the reportlab code in pdf.py for generate a pdf. """

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

    return expend_pdf(request, latest_node_list)

def pr_pdf(request):
    """ Calls the reportlab code in pdf.py for generate a pdf. """

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

    return pay_rec_pdf(request, latest_node_list)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
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
