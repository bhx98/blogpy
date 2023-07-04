from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
class ContactForm(forms.ModelForm):
    subject = forms.CharField(max_length=150)
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    # phone = forms.CharField(max_length=15)
    message = RichTextField
    # insert_date = forms.DateTimeField(auto_created=True)


class LoginForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Name', 'style': 'width: 300px;'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'style': 'width: 300px;'}))

# Override the user creation form


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True, label='Email', error_messages={'exitst': 'This already exists!'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(
                self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']
