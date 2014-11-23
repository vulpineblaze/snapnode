from django.shortcuts import render , get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from core.forms import *
from django.http import HttpResponseRedirect

# Create your views here.

from core.models import Node, UserProfile

import itertools



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

    
    generic_html_dump = ""

    generic_html_dump += "<P> In new_customer </P>"
    generic_html_dump += "fake <a href=\"../detail\" >SUBMIT</a>"
    generic_html_dump += " to pretend we just made a customer<BR>"

    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'core/generic.html', context)


def detail(request, node_id):
    """  Page for viewing all aspects of a customer. """
    iterator=itertools.count() ###

    node = get_object_or_404(Node, pk=node_id)
    return render(request, 'ops/detail.html', {'node': node, 'iterator':iterator})


def edit(request):
    """  Page for editing all aspects of a customer. """

    
    generic_html_dump = ""

    generic_html_dump += "<P> In edit </P>"
    generic_html_dump += "fake <a href=\"../detail\" >SUBMIT</a>"
    generic_html_dump += " to pretend we just updated a customer<BR>"

    context = {'generic_html_dump': generic_html_dump}

    return render(request, 'core/generic.html', context)



