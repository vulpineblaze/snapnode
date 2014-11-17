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

    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            # record = form.save(commit = False)
            # change the stuffs here
            # node_data = {parent:None, name:"", desc:"" }


            ticket_node = Node.objects.create()
            priority_node = Node.objects.create()
            flags_node = Node.objects.create()
            customer_node = Node.objects.create()
            customer_glue = Glue.objects.create()

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

            customer_node.name = form.cleaned_data['customer']
            customer_node.parent = ticket_node

            customer_node.save()

            customer_glue.child = ticket_node
            customer_glue.parent = customer_node

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


def edit(request):
    """  Page for editing all aspects of a ticket. """


    generic_html_dump = ""

    generic_html_dump += "<P> In edit </P>"
    generic_html_dump += "fake <a href=\"../detail\" >SUBMIT</a>"
    generic_html_dump += " to pretend we just updated a ticket<BR>"

    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'core/generic.html', context)



def new_event(request):                         ###
    """  Log a new event under a ticket. """


    generic_html_dump = ""

    generic_html_dump += "<P> In new_event </P>"
    generic_html_dump += "fake <a href=\"../detail\" >SUBMIT</a>"
    generic_html_dump += " to pretend we just added an event to a ticket<BR>"

    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'core/generic.html', context)
