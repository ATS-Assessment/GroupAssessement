from django import forms
from django.forms import ModelForm, inlineformset_factory, BaseFormSet
from django.utils import timezone

from groups.models import Group
from .models import Poll, Choice


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["title", "start_date", "end_date"]

    def clean(self):
        super(PollForm, self).clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if start_date < timezone.now().date():
            raise forms.ValidationError('Invalid input. Start date should not be in past.')

        if end_date < start_date:
            raise forms.ValidationError('Invalid Input. End date should be greater than start date.')


# class PollForm1(forms.ModelForm):
#     class Meta:
#         model = Poll
#         exclude = ["creator", "created_date", "group"]


class ChoiceForm(forms.ModelForm):
    # choice_one = forms.CharField(max_length=200)
    # choice_two = forms.CharField(max_length=200)
    # choice_three = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Choice
        exclude = ["poll", "vote"]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': "form-control rounded",
                                                  'style': 'border: 1px solid #ccc',
                                                  'margin-bottom': '10px'})
        }



PollInlineFormSet = inlineformset_factory(Poll, Choice, form=ChoiceForm, extra=0, can_delete=False)


# class ChoiceForm(forms.ModelForm):
#     # choice_one = forms.CharField(max_length=200)
#     # choice_two = forms.CharField(max_length=200)
#     # choice_three = forms.CharField(max_length=200, required=False)
#
#     class Meta:
#         model = Choice
#         fields = ["choice_text"]

