from django import forms
from .models import User, Organ, Service, Area, Job, Product, Brand

# 로그인 폼
class SigninForm(forms.Form):
    email = forms.EmailField(label='이메일', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '이메일을 입력해주세요',
            'required': 'True',
        }
    ))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '비밀번호를 입력해주세요',
            'required': 'True',
        }
    ))

# 일반회원 회원가입
class UserForm(forms.ModelForm):
    email = forms.EmailField(label='이메일')
    password1 = forms.CharField(label='비밀번호')
    password2 = forms.CharField(label='비밀번호 확인')
    codeNum = forms.DateField(label="생년월일")    
    class Meta:
        model = User
        fields = ['name', 'phoneNum',
                  'job', 'license', 'area', 'another', 'image']

# 기관회원 회원가입
class OrganUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'phoneNum', 'area']

# 기관만의 추가 폼
class OrganForm(forms.ModelForm):
    class Meta:
        model = Organ
        fields = ['crew', 'head', 'url']


# 기관에서 봉사활동 등록폼
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'Essential', 'point',
                  'level', 'number', 'emergency', 'image']
