from django.shortcuts import render , get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect

# Create your views here.

from core.models import Node, UserProfile

from ops.forms import *

import itertools
import time



def index(request):
    node_list = []
    latest_node_list = Node.objects.order_by('-date_updated')
    # template = loader.get_template('core/index.html')

    for node in latest_node_list:
        for child in node.node_set.all():
            if(child.name == "flags"):
                if "|CUSTOMER|" in child.desc:
                    node_list.append(node.pk)

    queryset = Node.objects.filter(pk__in=node_list)
    latest_node_list = queryset

    context = {'latest_node_list': latest_node_list}
    return render(request, 'ops/index.html', context)

def home(request):
    """  Starting page where User chooses what to do. """

    generic_html_dump = ""

    generic_html_dump += "<P> In home.html </P>"
    generic_html_dump += "<a href=\"customer\" >BROWSE CUSTOMERS</a><BR>"
    generic_html_dump += "<a href=\"customer/new_customer\" >NEW CUSTOMER</a><BR>"

    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'ops/home.html', context)


def new_customer(request):
    """  Page for making new customers. """

    form_action = "/ops/customer/new_customer/"

    if request.method == 'POST':
        form = NewCustomerForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }

            customer_node = Node.objects.create()
            primName_node = Node.objects.create()
            primPhone_node = Node.objects.create()
            primEmail_node = Node.objects.create()
            primAddress_node = Node.objects.create()
            rate_node = Node.objects.create()
            flags_node = Node.objects.create()
            invoice_node = Node.objects.create()
            in_flag_node = Node.objects.create()
            date_node = Node.objects.create()
            print_date_node = Node.objects.create()
            cost_other_node = Node.objects.create()
            status_node = Node.objects.create()

            # record.save()
            customer_node.name = form.cleaned_data['name']

            customer_node.save()

            primName_node.parent = customer_node
            primName_node.name = "primName"
            primName_node.desc = form.cleaned_data['primName']

            primName_node.save()

            primPhone_node.parent = customer_node
            primPhone_node.name = "primPhone"
            primPhone_node.desc = form.cleaned_data['primPhone']

            primPhone_node.save()

            primEmail_node.parent = customer_node
            primEmail_node.name = "primEmail"
            primEmail_node.desc = form.cleaned_data['primEmail']

            primEmail_node.save()

            primAddress_node.parent = customer_node
            primAddress_node.name = "primAddress"
            primAddress_node.desc = form.cleaned_data['primAddress']

            primAddress_node.save()

            rate_node.parent = customer_node
            rate_node.name = "rate"
            rate_node.desc = form.cleaned_data['rate']

            rate_node.save()

            flags_node.parent = customer_node
            flags_node.name = "flags"
            flags_node.desc = "|CUSTOMER|"

            flags_node.save()

            invoice_node.parent = customer_node
            invoice_node.name = "invoice"
            invoice_node.desc = " "

            invoice_node.save()

            in_flag_node.parent = invoice_node
            in_flag_node.name = "flags"
            in_flag_node.desc = "|INVOICE|"

            in_flag_node.save()

            date_node.parent = invoice_node
            date_node.name = "date"
            date_node.desc = time.strftime("%m/%d/%Y")

            date_node.save()   

            print_date_node.parent = invoice_node
            print_date_node.name = "print_date"
            print_date_node.desc = " "

            date_node.save()            
            
            cost_other_node.parent = invoice_node
            cost_other_node.name = "cost_other"
            cost_other_node.desc = "0"

            cost_other_node.save()

            status_node.parent = invoice_node
            status_node.name = "status"
            status_node.desc = "Open"

            status_node.save()

            #customer_glue = Glue.objects.create(parent=form.cleaned_data['customer'],
            #                                    child=ticket_node,
            #                                    name="CUSTOMER has TICKET")

            # asset_set = form.cleaned_data['assets']

            # customer_glue.parent = form.cleaned_data['customer']
            # customer_glue.child = ticket_node

            #customer_glue.save()

            # form.save()
            return HttpResponseRedirect('/ops/customer/detail/'+str(customer_node.id))
    else:
        form = NewCustomerForm()

    return render(request, 'ops/detail.html', {'form': form,'action':'new_customer'})


def detail(request, node_id):
    """  Page for viewing all aspects of a customer. """
    iterator=itertools.count() ###

    node = get_object_or_404(Node, pk=node_id)
    return render(request, 'ops/detail.html', {'node': node, 'iterator':iterator})


def edit(request, node_id):
    """  Page for editing all aspects of a customer. """

    form_action = "/ops/customer/edit/" + str(node_id)

    customer_node = get_object_or_404(Node, pk=node_id)
    primName_node = Node.objects.get(parent=customer_node, name='primName')
    primPhone_node = Node.objects.get(parent=customer_node, name='primPhone')
    primEmail_node = Node.objects.get(parent=customer_node, name='primEmail')
    primAddress_node = Node.objects.get(parent=customer_node, name='primAddress')
    rate_node = Node.objects.get(parent=customer_node, name='rate')

    if request.method == 'POST':
        form = NewCustomerForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }
            # record.save()

            customer_node.name = form.cleaned_data['name']

            customer_node.save()

            primName_node.desc = form.cleaned_data['primName']

            primName_node.save()

            primPhone_node.desc = form.cleaned_data['primPhone']

            primPhone_node.save()

            primEmail_node.desc = form.cleaned_data['primEmail']

            primEmail_node.save()

            primAddress_node.desc = form.cleaned_data['primAddress']

            primAddress_node.save()

            rate_node.desc = form.cleaned_data['rate']

            rate_node.save()

            #customer_glue = Glue.objects.create(parent=form.cleaned_data['customer'],
            #                                    child=ticket_node,
            #                                    name="CUSTOMER has TICKET")

            # asset_set = form.cleaned_data['assets']

            # customer_glue.parent = form.cleaned_data['customer']
            # customer_glue.child = ticket_node

            #customer_glue.save()

            # form.save()
            return HttpResponseRedirect('/ops/customer/detail/'+str(customer_node.id))
    else:
        form = NewCustomerForm( initial = { 'name':customer_node.name,
                                            'primName':primName_node.desc,
                                            'primEmail':primEmail_node.desc,
                                            'primPhone':primPhone_node.desc,
                                            'primAddress':primAddress_node.desc,
                                            'rate':rate_node.desc
                                } )

    return render(request, 'ops/detail.html', {'form': form,'action':'edit'})

def new_asset(request, node_id):                         ###
    """  Log a new event under a ticket. """

    form_action = "/ops/customer/new_asset/" + str(node_id) +"/"
    if request.method == 'POST':
        form = NewAssetForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }

            asset_node = Node.objects.create()
            flags_node = Node.objects.create()

            # record.save()

            asset_node.parent = get_object_or_404(Node, pk=node_id)
            asset_node.name = form.cleaned_data['name']
            asset_node.desc = form.cleaned_data['desc']

            asset_node.save()

            flags_node.parent = asset_node
            flags_node.name = "flags"
            flags_node.desc = "|ASSETS|"

            flags_node.save()  


            #customer_glue = Glue.objects.create(parent=get_object_or_404(Node, pk=node_id),
            #                                    child=asset_node,
            #                                    name="CUSTOMER has ASSET")

            #customer_glue.save()

            # form.save()
            return HttpResponseRedirect('/ops/customer/detail/'+str(node_id)+"/" )
    else:
        form = NewAssetForm()

    context = {'form': form,
                'action':'new_asset',
                'form_action':form_action}

    return render(request, 'ops/new_asset.html', context)
