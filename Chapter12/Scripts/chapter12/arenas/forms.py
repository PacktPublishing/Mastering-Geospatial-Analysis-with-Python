from django import forms
from .models import Arenas

class ArenaForm(forms.Form):
        name = ""
        description = "Use the dropdown to select an arena."
        selections = forms.ChoiceField(choices=Arenas.objects.values_list('id','name1'),
                                       widget=forms.Select(),required=True)
