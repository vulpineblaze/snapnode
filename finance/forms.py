from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.contrib.admin import widgets
from django.forms import TextInput, Textarea

class InvoiceForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()

class NewBankDepositEventForm(forms.ModelForm):
    #Creates a Form for the generic top-level assets
    # sub_name = forms.CharField(label="Property Name")
    # customer = forms.CharField(label="Customer Name")


    BDE_list = []
#    asset_list = []
    cust_asset_list = []
    latest_node_list = Node.objects.order_by('-date_updated')
    latest_glue_list = Glue.objects.order_by('-date_updated')

    # template = loader.get_template('core/index.html') 

    for node in latest_node_list:
        for child in node.node_set.all():
            if(child.name == "flags"):
              if "|BDE|" in child.desc:
                  cust_list.append(node.pk)
"""
    for node in latest_node_list:
        for child in node.node_set.all():
            if(child.name == "flags"):
              if "|ASSET|" in child.desc:
                  asset_list.append(node.pk)
"""

    cust_queryset = Node.objects.filter(pk__in=cust_list)

    customer = forms.ModelChoiceField(queryset=cust_queryset, 
                                        empty_label="(Choose One)",
                                        to_field_name="name")

    # test_var = dir(customer)
    # second_var = dir(customer.choices) ##
    # third_var = customer.choices.queryset
#    for glue in latest_glue_list:
#        if glue.parent is customer and glue.child.pk in asset_list:
#            cust_asset_list.append(glue.child.pk)

    

#    asset_queryset = Node.objects.filter(pk__in=cust_asset_list)

#    assets = forms.ModelMultipleChoiceField(queryset=asset_queryset, 
#                                        to_field_name="name",
#                                        required=False)

#    priority = forms.ChoiceField(label="Priority"
#                                ,choices=TICKET_PRIORITY_CHOICES)
#    status = forms.ChoiceField(label="Status"
#                              ,choices=TICKET_STATUS_CHOICES)

    class Meta:
        model = Node
        fields = ('ID', 'date','bank','depositor', 'amount')



