from django import forms

from .models import Choice

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

    def clean_choice(self):
        choice_text = self.cleaned_data.get('choice_text')
        return choice_text
