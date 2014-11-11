from django.shortcuts import render
from django.template import RequestContext, loader
from core.forms import *
from django.http import HttpResponseRedirect

# Create your views here.

from core.models import Node, UserProfile



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

def new(request):
    """ """
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/index/')
    else:
        form = NodeForm()

    return render(request, 'ticket/new.html', {'form': form})
