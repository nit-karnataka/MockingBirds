from django import forms

class SearchForm(forms.Form):
    keywords=forms.CharField(widget=forms.Textarea)
    email=forms.EmailField()
