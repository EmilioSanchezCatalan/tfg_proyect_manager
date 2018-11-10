from django import forms
from core.models import Masters

class FilterPublicTfmForm(forms.Form):
    name_project = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))
    formation_project = forms.ModelChoiceField(
        queryset=Masters.objects.all(),
        empty_label="Master",
        required=False, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

class FilterTeacherTfmForm(forms.Form):
    search_text = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Título'}
    ))