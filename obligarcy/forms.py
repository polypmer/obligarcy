# -*- coding: utf-8 -*-
from functools import partial
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from .models import Submission, Contract, UserProfile, Deadline
from django.contrib.auth.models import User

# http://stackoverflow.com/questions/20700185/how-to-use-datepicker-in-django
# for the datepicker:
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs=
        {'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):
    picture = forms.FileInput(attrs=
        {'class': 'form-control'})

    class Meta:
        model = UserProfile
        fields = ['picture']


class SubForm(forms.Form):
    # here we use a dummy `queryset`, because ModelChoiceField
    # requires some queryset
    body = forms.CharField(widget=forms.Textarea(attrs=
        {'class': 'form-control','rows':'18'}))
    deadline = forms.ModelChoiceField(queryset=Deadline.objects.none())

    def __init__(self, contract_id):
        super(SubForm, self).__init__()
        self.fields['deadline'].queryset = Deadline.objects.filter(contract=contract_id) # Somehow this works


class ContractForm(forms.ModelForm):
# https://docs.djangoproject.com/en/dev/topics/forms/#looping-over-the-form-s-fields
    FREQ = (
        ('O', 'Once off'),
        ('D', 'Daily'),
        ('2D', 'Every other day'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    )

    preamble = forms.CharField(max_length=150,
        widget=forms.Textarea(attrs={'class': 'form-control',
'placeholder': 'We the undersigned agree to this contract ...',
         'rows': '3'}))
    conditions = forms.CharField(max_length=400,
        widget=forms.Textarea(attrs={'class': 'form-control',
'placeholder': 'I must submit a movie review no less than 200 words every ...',
         'rows': '7'}))
    penalties = forms.CharField(max_length=200,
        widget=forms.Textarea(attrs={'class': 'form-control',
'placeholder': 'I agree to the aforementioned conditions on pain of ...',
         'rows': '5'}))
    end_date = forms.DateField(widget=DateInput())
    start_date = forms.DateField(widget=DateInput())
    frequency = forms.CharField(max_length=20, widget=forms.Select(
        attrs={'class': 'form-control'}, choices=FREQ))
    #http://getbootstrap.com/css/#forms-control-readonly
    #<input class="form-control" type="text" placeholder="…" readonly>
    first_signee = forms.ModelChoiceField(queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}))
    second_signee = forms.ModelChoiceField(queryset=User.objects.all(),
        required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    third_signee = forms.ModelChoiceField(queryset=User.objects.all(),
         required=False, widget=forms.Select(attrs={'class':
              'form-control'}))
    fourth_signee = forms.ModelChoiceField(queryset=User.objects.all(),
         required=False, widget=forms.Select(attrs={'class':
              'form-control'}))

    class Meta:
        model = Contract
        fields = ['preamble','conditions','penalties', 'end_date', 'start_date', 'frequency']
