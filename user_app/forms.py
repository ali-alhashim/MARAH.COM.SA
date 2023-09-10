
from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class CustomUserChangeForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'w-100'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'w-100'}))
    class Meta:

        model = User
        fields = [ "name", "mobile","profile_photo","language","is_active","is_admin","is_staff","is_superuser","mobile_verified"]
        labels = {
                    
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
      
        name             = forms.CharField(widget=forms.TextInput(attrs={'class':'text-subject'}))
        mobile           = forms.CharField(widget=forms.TextInput(attrs={'class':'text-mobile','value':'966'}))
        
        class Meta:
            model = User
            fields = ['name', 'mobile',  'password']

        
        def clean(self):
            cleaned_data = super(RegistrationForm, self).clean()
            password     = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')

            if password != confirm_password:
                raise forms.ValidationError('password dose not match !!')



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields =  ('name', 'mobile', 'is_active','is_admin','is_staff','is_superuser', 'groups', 'user_permissions',)
        widgets = {
            
            'name':forms.TextInput(attrs={'class':'form-control'}),
          
               'groups':forms.SelectMultiple(attrs={'class':'form-select'}),
                'user_permissions':forms.SelectMultiple(attrs={'class':'form-select'}),
             
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
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label= ("Password"))
     

    class Meta:
        model = User
        fields =  ('name','password', 'mobile','is_active','is_admin','is_staff','is_superuser',  'groups', 'user_permissions')
        widgets = {
           
            'name':forms.TextInput(attrs={'class':'form-control'}),
            
          
             'mobile':forms.TextInput(attrs={'class':'form-control'}),
         
          
              'groups':forms.SelectMultiple(attrs={'class':'form-select'}),
              'user_permissions':forms.SelectMultiple(attrs={'class':'form-select'}),
              
              
             
        }            

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class PasswordChangeForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('name','password')
        widgets = {
            'password':forms.TextInput(attrs={'class':'form-control', 'readonly':'True'}),
            'name':forms.TextInput(attrs={'class':'form-control', 'readonly':'True'}),
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
        user = super(PasswordChangeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
