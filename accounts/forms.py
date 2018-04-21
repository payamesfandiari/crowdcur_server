import logging

from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from crispy_forms.helper import FormHelper

from crispy_forms.layout import Submit, Layout, Div, Fieldset, MultiField, HTML

from .models import User


logger = logging.getLogger(__name__)


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2', 'age', 'education']

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-2'
    helper.field_class = 'col-md-10'
    helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary btn-lg'))
    # def __init__(self, *args, **kwargs):
    #     super(UserRegisterForm,self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-md-2'
    #     self.helper.field_class = 'col-md-10'
    #     self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary btn-lg'))
    #     self.helper.layout = Layout(
    #         Fieldset("Account Information",
    #                  Field('username', placeholder='A Unique Username',
    #                        css_class="some-class"),
    #                  Field('password'),
    #                  Field('email'),
    #                  ),
    #         Fieldset("About you", 'age', 'education',css_class="row"),
    #     )

    @transaction.atomic
    def save(self, **kwargs):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.education = self.cleaned_data.get('education')
        user.age = self.cleaned_data.get('age')
        user.save()
        return user