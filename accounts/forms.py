import logging

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from crispy_forms.helper import FormHelper

from crispy_forms.layout import HTML

from .models import User

logger = logging.getLogger(__name__)


class UserRegisterForm(UserCreationForm):
    pref = forms.CharField(max_length=999,widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'education','nationality']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'worker_register_form'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        self.helper.layout.append(
            HTML(
                """
            <div class="row">
                        <div class="col-sm-1"></div>
                        <div class="col-sm-5 pref-list">
                            <h3>Keywords : </h3>
                            <ol class="list-group list-group-sortable-connected">
                            {% for key in keywords %}
                                <li class="list-group-item list-group-item-info choice">{{ key }}</li>                                
                            {% endfor %}
                            </ol>
                        </div>

                        <div class="col-sm-5 pref-list">
                            <h3>Your Preferences : </h3>
                            <ol class="list-group list-group-sortable-connected" id="crowdcur_worker_feedback">

                            </ol>
                        </div>
                        <div class="col-sm-1"></div>
                    </div>
            """))
        self.helper.layout.append(HTML(
            """
            <div class="row submit-div">
                <div class="col-xs-4 col-md-4"></div>
                <div class="col-xs-4 col-md-4">                    
                    <input type="submit" value="Submit"
                           class="btn btn-primary btn-block btn-lg" tabindex="7">
                </div>
                <div class="col-xs-4 col-md-4"></div>

            </div>
            """
        ))

    def clean_pref(self):
        pref = self.cleaned_data['pref'].split(',')
        if len(pref) < 5:
            forms.ValidationError('Not Enough Keywords have been selected.',code="not_enough_keywords")
        else:
            return pref[0:5]


    @transaction.atomic
    def save(self, **kwargs):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.education = self.cleaned_data.get('education')
        user.age = self.cleaned_data.get('age')
        user.preference = self.cleaned_data.get('pref')
        user.save()
        return user
