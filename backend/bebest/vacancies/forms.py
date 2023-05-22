from django import forms
from django.utils.translation import gettext_lazy as _
from .models import VacancyArea, VacancyStats


class VacancyStatsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'] = forms.ChoiceField(choices=[(loc, _(loc)) for loc in sorted(VacancyArea.distinct_locations())], widget=forms.Select(attrs={
            'class': 'block appearance-none w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500',
        }))

    # speciality = forms.ChoiceField(choices=VacancyStats.Speciality.choices)
    speciality = forms.ChoiceField(choices=VacancyStats.Speciality.choices, widget=forms.Select(attrs={
        'class': 'block appearance-none w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500',
    }))

    # location (see __init__)

    # NOTE: tags are not supported yet
    # tags = forms.MultipleChoiceField(choices=[('1', 'Python'), ('2', 'Django')], widget=forms.CheckboxSelectMultiple)
