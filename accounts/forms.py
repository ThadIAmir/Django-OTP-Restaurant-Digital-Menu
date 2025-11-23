from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email'] # Add email if you want
        
        # Override the field labels
        labels = {
            'username': 'نام کاربری',
            'email': 'ایمیل (اختیاری)',
        }
        
        # Override the help texts (The small text under inputs)
        help_texts = {
            'username': 'از حروف انگلیسی، اعداد و کاراکترهای @/./+/-/_ استفاده کنید.',
        }

    # We override the __init__ to change the password label/help text
    # because Password is not a standard DB field in Meta
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Password 1
        self.fields['username'].widget.attrs['placeholder'] = 'مثال: ali_rezaei'
        
        # Password 1 Labels & Help
        self.fields['password1'].label = "رمز عبور"
        self.fields['password1'].help_text = (
            "رمز عبور باید حداقل ۸ کاراکتر باشد و خیلی ساده نباشد (مثل ۱۲۳۴۵۶)."
        )
        
        # Password 2 Labels
        self.fields['password2'].label = "تکرار رمز عبور"
        # self.fields['password2'].help_text = (
        #     "دوباره رمز عبور خود را وارد کنید."
        # )
        self.fields['password2'].help_text = None