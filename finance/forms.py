from django import forms

class InvoiceForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()
