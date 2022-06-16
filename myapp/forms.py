from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class CheckRequirementsForm(forms.Form):
    SEX_CHOICES = [('m', 'male'), ('f', 'female')]

    CEFR = (
        ("A1", "Beginner"),
        ("A2", "Elementary"),
        ("B1", "Intermediate"),
        ("B2", "Upper-Intermediate"),
        ("C1", "Advanced"),
        ("C2", "Proficiency"),
    )

    name = forms.CharField(label='name', max_length=100, required=True)
    sex = forms.ChoiceField(label='sex', choices=SEX_CHOICES, initial='m', widget=forms.RadioSelect, required=True)
    age = forms.IntegerField(label='age', validators=[MinValueValidator(18), MaxValueValidator(80)], initial=18, required=True)
    english_level = forms.ChoiceField(label='english level', choices=CEFR)












