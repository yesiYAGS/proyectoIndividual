from django import forms
from .models import Usuario
import bcrypt

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    confirmed_pw = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput,
        }
        
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirmed_pw")
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_pw does not match"
            )
        # first_name = cleaned_data.get("first_name")
        # last_name = cleaned_data.get("last_name")
        # email = cleaned_data.get("email")
        # forms.Form.add_error( field, message )
        # if len(first_name) < 3:
        #      self._errors['first_name'] = self.error_class([
        #         'First Name Minimum 5 characters required'])
        # if len(last_name) < 3:
        #      self._errors['last_name'] = self.error_class([
        #         'Last Name Minimum 5 characters required'])
        # if len(email) < 0:
        #      self._errors['email'] = self.error_class([
        #         'Email Minimum 5 characters required'])



    def save(self, commit=True):
        # your logic or Save your object for example:
        pw = self.cleaned_data["password"]
        pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
        user = Usuario.objects.create(first_name=self.cleaned_data["first_name"], last_name=self.cleaned_data["last_name"], email=self.cleaned_data["email"], password=pw_hash)
        return user