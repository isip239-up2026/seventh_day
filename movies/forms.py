from django import forms
from movies import models

class ReviewForm(forms.Form):
    author_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'})
    )
    rating = forms.ChoiceField(
        choices=models.Review.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )