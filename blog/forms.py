from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
class LoginForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Name', 'style': 'width: 300px;'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'style': 'width: 300px;'}))

