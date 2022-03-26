from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):  # this class inherits forms.modelform

    password = forms.CharField(widget=forms.PasswordInput(attrs = {
    'placeholder': 'Enter Password',
    'class' : 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs = {
    'placeholder': 'Confirm Password',
    'class' : 'form-control',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password'] # mandated fields

    # Checking if password and confirm password match

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get ('password')
        confirm_password = cleaned_data.get ('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match!!")

    def __init__(self, *args, **kwargs): # applying the 'form-control' CSS styling to all input fields
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # placeholder applied to the input fields (password placeholder defined above)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
