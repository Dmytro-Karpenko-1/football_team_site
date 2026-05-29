from django import forms
from .models import JoinApplication


class JoinTeamForm(forms.ModelForm):
    """Short trial training request form."""
    class Meta:
        model = JoinApplication
        fields = ['child_name', 'parent_phone', 'birth_year']
        widgets = {
            'child_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': "Ім'я дитини",
                'autocomplete': 'given-name',
            }),
            'parent_phone': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '+380',
                'type': 'tel',
                'autocomplete': 'tel',
            }),
            'birth_year': forms.Select(attrs={'class': 'form-select form-select-lg'}),
        }
        labels = {
            'child_name': "Ім'я дитини",
            'parent_phone': 'Телефон батьків',
            'birth_year': 'Рік народження дитини',
        }
