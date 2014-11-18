from django.shortcuts import render , get_object_or_404, render_to_response
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect


# Create your views here.

from core.models import Node, UserProfile
from ticket.forms import *

import itertools


def index(request):
    """  Front page for hot/new tickets. """
    node_list = []
    latest_node_list = Node.objects.order_by('-date_updated')
    # template = loader.get_template('core/index.html')


    for node in latest_node_list:
        for child in node.node_set.all():
            if(child.name == "flags"):
              if "|TICKET|" in child.desc:
                  node_list.append(node.pk)



    queryset = Node.objects.filter(pk__in=node_list)
    latest_node_list = queryset

    context = {'latest_node_list': latest_node_list}
    return render(request, 'ticket/index.html', context)



def home(request):
    """  Starting page where User chooses what to do. """

    generic_html_dump = ""

    generic_html_dump += "<P> In home.html </P>"
    generic_html_dump += "<a href=\"index\" >INDEX</a><BR>"
    generic_html_dump += "<a href=\"new_ticket\" >NEW TICKET</a><BR>"
    generic_html_dump += "<a href=\"index\" >UNDECIDED FEATURE</a><BR>"
    generic_html_dump += "<a href=\"index\" >UNDECIDED FEATURE</a><BR>"

    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'core/generic.html', context)


def new_ticket(request):
    """  Page for making new tickets. """

    form_action = "/ticket/new_ticket/"

    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }


            ticket_node = Node.objects.create()
            priority_node = Node.objects.create()
            flags_node = Node.objects.create()
            status_node = Node.objects.create()
            # customer_node = Node.objects.create()

            # record.save()
            ticket_node.name = form.cleaned_data['name']
            ticket_node.desc = form.cleaned_data['desc']

            ticket_node.save()

            priority_node.parent = ticket_node
            priority_node.name = "priority"
            priority_node.desc = form.cleaned_data['priority']

            priority_node.save()

            flags_node.parent = ticket_node
            flags_node.name = "flags"
            flags_node.desc = "|TICKET|"

            flags_node.save()

            status_node.parent = ticket_node
            status_node.name = "status"
            status_node.desc = form.cleaned_data['status']

            status_node.save()


            customer_glue = Glue.objects.create(parent=form.cleaned_data['customer'],
                                                child=ticket_node,
                                                name="CUSTOMER has TICKET")

            # customer_glue.parent = form.cleaned_data['customer']
            # customer_glue.child = ticket_node

            customer_glue.save()

            # form.save()
            return HttpResponseRedirect('/ticket/detail/'+str(ticket_node.id))
    else:
        form = NewTicketForm()

    return render(request, 'ticket/new_ticket.html', {'form': form,'action':'new_ticket'})




def detail(request, node_id):
    """  Page for viewing all aspects of a ticket. """
    iterator=itertools.count() ###

    node = get_object_or_404(Node, pk=node_id)
    return render(request, 'ticket/detail.html', {'node': node, 'iterator':iterator})



def edit(request, node_id):
    """  Page for editing all aspects of a ticket. """

    form_action = "/ticket/edit/" + str(node_id)

    ticket_node = get_object_or_404(Node, pk=node_id)
    priority_node = Node.objects.filter(parent=ticket_node,name='priority')[0]
    status_node = Node.objects.filter(parent=ticket_node,name='status')[0]

    #this is wrong, but works cuz the working bits are wrong tooo
    customer_node = Node.objects.filter(parent=ticket_node,name='customer')[0]

    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }






            # record.save()
            ticket_node.name = form.cleaned_data['name']
            ticket_node.desc = form.cleaned_data['desc']

            ticket_node.save()

            priority_node.desc = form.cleaned_data['priority']

            priority_node.save()

            status_node.desc = form.cleaned_data['status']

            status_node.save()



            # form.save()
            return HttpResponseRedirect('/ticket/detail/'+str(ticket_node.id))
    else:
        node = get_object_or_404(Node, pk=node_id)

        form = NewTicketForm( initial = { 'name':ticket_node.name,
                                            'desc':ticket_node.desc,
                                            'customer':customer_node.name,
                                            'priority':priority_node.desc,
                                            'status':status_node.desc,
            } )

    return render(request, 'ticket/new_ticket.html', {'form': form,'action':'new_ticket'})





def new_event(request, node_id):                         ###
    """  Log a new event under a ticket. """

    form_action = "/ticket/new_event/" + str(node_id)
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }

            event_node = Node.objects.create()
            flags_node = Node.objects.create()
            hours_node = Node.objects.create()

            # record.save()
            event_node.parent = get_object_or_404(Node, pk=node_id)
            event_node.name = form.cleaned_data['name']
            event_node.desc = form.cleaned_data['desc']

            event_node.save()


            flags_node.parent = event_node
            flags_node.name = "flags"
            flags_node.desc = "|EVENT|"

            flags_node.save()


            hours_node.parent = event_node
            hours_node.name = "hours"
            hours_node.desc = form.cleaned_data['hours']

            hours_node.save()



            # form.save()
            return HttpResponseRedirect('/ticket/detail/'+str(node_id))
    else:
        form = NewEventForm()

    context = {'form': form,
                'action':'new_event',
                'form_action':form_action}

    return render(request, 'ticket/new_event.html', context)
