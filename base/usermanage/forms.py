from django import forms
from .models import Profile


email_messages = {
    'required' : 'این فیلد اجباری است' ,
    'invalid' : 'ایمیل صحیح نمی باشد'
}



class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length = 30 ,
        widget = forms.TextInput( attrs={
            'class' : 'form-control' ,
            'placeholder' : 'username' ,
        })
    )
    password = forms.CharField(
        max_length = 40 ,
        widget = forms.PasswordInput( attrs={
            'class' : 'form-control' ,
            'placeholder' : 'password' ,
        })
    )


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        max_length = 30 ,
        widget = forms.TextInput( attrs={
            'class' : 'form-control' ,
            'placeholder' : 'username' ,
        })
    )
    email = forms.EmailField(
        max_length = 50 ,
        error_messages = email_messages ,        
        widget = forms.EmailInput( attrs={
            'class' : 'form-control' ,
            'placeholder' : 'Email' ,
        })
    )
    password = forms.CharField(
        max_length = 40 ,
        widget = forms.PasswordInput( attrs={
            'class' : 'form-control' ,
            'placeholder' : 'password' ,
        })
    )

class EditProfileForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta :
        model = Profile
        fields = ('bio','age')



class PhoneLoginForm(forms.Form):
    phone = forms.IntegerField()

    def clean_phone(self):
        phone = Profile.objects.filter(phone = self.cleaned_data['phone'])
        if not phone.exists():
            raise forms.ValidationError('This phone number does not exists')
        # phone is Recorde Field can not send 
        return self.cleaned_data['phone']


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()





