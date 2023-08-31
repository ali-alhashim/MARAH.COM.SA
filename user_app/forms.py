
from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class CustomUserChangeForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'w-100'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'w-100'}))
    class Meta:

        model = User
        fields = ["email", "full_name", "nikname","mobile","profile_photo","language","is_active","is_admin","is_staff","is_superuser","email_verified","mobile_verified"]
        labels = {
                    'email': 'Email Address',
                    'is_active': 'Active',
                  }
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CustomUserChangeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    


class RegistrationForm(forms.ModelForm):
        password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password', 'class':'text-password'}))
        confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm password', 'class':'text-password'}))
        email            = forms.EmailField(widget=forms.EmailInput(attrs={'class':'text-email'}))
        full_name             = forms.CharField(widget=forms.TextInput(attrs={'class':'text-subject'}))
        mobile           = forms.CharField(widget=forms.TextInput(attrs={'class':'text-mobile'}))
        nikname          = forms.CharField(widget=forms.TextInput(attrs={'class':'text-subject'}))
        class Meta:
            model = User
            fields = ['full_name', 'mobile', 'email','nikname', 'password']

        
        def clean(self):
            cleaned_data = super(RegistrationForm, self).clean()
            password     = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')

            if password != confirm_password:
                raise forms.ValidationError('password dose not match !!')
        