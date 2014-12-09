from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.contrib.admin import widgets
from django.forms import TextInput, Textarea

from django.contrib.auth.models import User

from core.models import *


class SubNodeForm(forms.ModelForm):
    """ Creates a Form for the sub-nodes for assets """

    class Meta:
        model = Node
        fields = ('name', 'desc')



class GenericAssetForm(forms.ModelForm):
    """ Creates a Form for the generic top-level assets """
    sub_name = forms.CharField(label="Property Name")
    sub_desc = forms.CharField(widget=forms.Textarea
                                ,label="Property Desc")

    class Meta:
        model = Node
        fields = ('name', 'desc','sub_name','sub_desc')




class NodeForm(forms.ModelForm):
    """ Creates a Form for the base Node """
    class Meta:
        model = Node
        fields = ('parent', 'name', 'desc')






# from django import forms
# from django.forms.extras.widgets import SelectDateWidget

# BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
# FAVORITE_COLORS_CHOICES = (('blue', 'Blue'),
#                             ('green', 'Green'),
#                             ('black', 'Black'))

# class SimpleForm(forms.Form):
#     birth_year = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
#     favorite_colors = forms.MultipleChoiceField(required=False,
#         widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)

TICKET_PRIORITY_CHOICES = (('1','1 - High'),
                            ('2','2 - Medium'),
                            ('3','3 - Low'))
TICKET_STATUS_CHOICES = (('Not Started','Not Started'),
                         ('In Progress','In Progress'),
                         ('Pending','Pending'),
                         ('Completed','Completed'))


class NewCustomerForm(forms.ModelForm):
    """ Creates a Form for the generic top-level assets """
    # sub_name = forms.CharField(label="Property Name")
    # customer = forms.CharField(label="Customer Name")


    #primName = []
    #primPhone = []
    #primEmail = []
    #primAddress = []
    #rate = []
    latest_node_list = Node.objects.order_by('-date_updated')
    latest_glue_list = Glue.objects.order_by('-date_updated')

    # template = loader.get_template('core/index.html')

    primName = forms.CharField(label="Primary Name")

    primPhone = forms.CharField(label="Primary Phone")

    primEmail = forms.CharField(label="Primary Email")

    primAddress = forms.CharField(label="Primary Address")

    rate = forms.CharField(label="Hourly Rate")

    class Meta:
        model = Node
        fields = ('name', 'primName', 'primPhone', 'primEmail', 'primAddress', 'rate')


class NewEventForm(forms.ModelForm):
    """ Creates a Form for the generic top-level assets """
    # sub_name = forms.CharField(label="Property Name")
    hours = forms.DecimalField(label="Hours Worked"
                                    ,min_value=0.0
                                    ,max_value=12.0)


    class Meta:
        model = Node
        fields = ('name', 'desc','hours')





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
