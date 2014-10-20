from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.contrib.admin import widgets   
from django.forms import TextInput, Textarea

from django.contrib.auth.models import User

from core.models import *


                                           
class UserForm(forms.ModelForm):
    """ 
    Creates a Form for the User/UserProfile model 
    Also has required confirm fields with supporting clean/error methods
    """

    confirm_email = forms.EmailField(
        label="Confirm Email",
        required=True,
    )
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password",
        required=True,
    )
    
    class Meta:
        """ Overrides Meta property to user User model and defines and orders fields  """
        model = User
        fields = ('username','first_name' ,'last_name', 'email', 'confirm_email', 'password', 'confirm_password' )
        
    def __init__(self, *args, **kwargs):

        if kwargs.get('instance'):
            email = kwargs['instance'].email
            kwargs.setdefault('initial', {})['confirm_email'] = email
            password = kwargs['instance'].password
            kwargs.setdefault('initial', {})['confirm_password'] = password

        return super(UserForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        """ Overrides cleam method to support confirm fields """
        valid_text = ""
        if (self.cleaned_data.get('email') !=
            self.cleaned_data.get('confirm_email')):
            self._errors['email'] = "Email addresses must match."
            self._errors['confirm_email'] = "Email addresses must match."
            valid_text += " Email addresses must match. "
        if (self.cleaned_data.get('password') !=
            self.cleaned_data.get('confirm_password')):
            self._errors['password'] = "Passwords must match."
            self._errors['confirm_password'] = "Passwords must match."
            valid_text += " Passwords must match. "
        if valid_text != "":
            raise ValidationError(valid_text)
        return self.cleaned_data

class UserProfileForm(forms.ModelForm):
    """ Creates a Form for the UserProfile """
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
#formset = MySpecialFormset(instance=rma) #add request.POST and request.FILES if used on the POST cycle


        
        
