from django import forms
from .models import User, Organ, Service, Area, Job, Product, Brand

# 로그인 폼
class SigninForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

# 일반회원 회원가입
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'codeNum', 'phoneNum',
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
