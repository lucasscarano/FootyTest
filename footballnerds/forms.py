from django.contrib.auth.forms import UserCreationForm

from django import forms

from footballnerds.models import User, Nationality


class RegistrationForm(UserCreationForm):

    username = forms.CharField(label='Username', max_length=30)
    nationality = forms.ModelChoiceField(queryset=Nationality.objects.none(), required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'nationality',)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].help_text = None
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['nationality'] = forms.ModelChoiceField(label='Nationality', queryset=Nationality.objects.all())
        self.fields['nationality'].widget.attrs['class'] = 'form-control'
