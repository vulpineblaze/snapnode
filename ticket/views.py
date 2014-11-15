from django.shortcuts import render
from django.template import RequestContext, loader

# Create your views here.

from core.models import Node, UserProfile



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

    
    generic_html_dump = ""

    generic_html_dump += "<P> In new_ticket </P>"
    generic_html_dump += "fake <a href=\"../detail\" >SUBMIT</a>"
    generic_html_dump += " to pretend we just made a ticket<BR>"

    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'core/generic.html', context)




def detail(request):
    """  Page for viewing all aspects of a ticket. """

    
    generic_html_dump = ""

    generic_html_dump += "<P> In detail </P>"
    generic_html_dump += "<a href=\"../edit\" >EDIT</a><BR>"
    generic_html_dump += "<a href=\"../new_event\" >NEW_EVENT</a><BR>"

    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'core/generic.html', context)


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