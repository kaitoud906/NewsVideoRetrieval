from django import forms

class FilterForm(forms.Form):
    FILTER_CHOICES = (
        # ('none', 'None'),
        ('single', 'Single Query'),
        ('multiple', 'Multiple Query')
    )

    filter_by = forms.ChoiceField(choices = FILTER_CHOICES)