from django import forms
import datetime
from .models import User, Organ, Service, Area, Job, Product, Brand

YEARS = range(datetime.date.today().year, 1950, -1)
MONTHS = {
    1: ('1월'), 2: ('2월'), 3: ('3월'), 4: ('4월'),
    5: ('5월'), 6: ('6월'), 7: ('7월'), 8: ('8월'),
    9: ('9월'), 10: ('10월'), 11: ('11월'), 12: ('12월')
}
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
        attrs={'class': 'form-control',
               'placeholder': '비밀번호를 입력해주세요',
               'required': 'True',
               }
    ))

# 일반회원 회원가입


class UserForm(forms.ModelForm):
    email = forms.EmailField(
        label='이메일', help_text="ex) email@gmail.com 형식으로 기재해주세요")
    password = forms.CharField(
        label="비밀번호", widget=forms.PasswordInput, required=True)
    check_password = forms.CharField(
        label="비밀번호 확인", widget=forms.PasswordInput, required=True)
    codeNum = forms.DateField(widget=forms.SelectDateWidget(
        months=MONTHS,
        years=YEARS,
        empty_label=("Choose Year", "Choose Month", "Choose Day")),
        label="생년월일", help_text="ex) 월, 일, 년도를 선택해주세요.")
    phoneNum = forms.CharField(
        label="전화번호", help_text='ex) 010-1234-5678 형식으로 기재해주세요.')

    class Meta:
        model = User
        fields = ['email', 'password', 'check_password', 'name', 'codeNum',
                  'phoneNum', 'job', 'license', 'area', 'another', 'image']


# 기관회원 회원가입
class OrganUserForm(forms.ModelForm):
    email = forms.EmailField(
        label='이메일', help_text="ex) email@gmail.com 형식으로 기재해주세요")
    name = forms.CharField(label='기관명')
    password = forms.CharField(
        label="비밀번호", widget=forms.PasswordInput, required=True)
    check_password = forms.CharField(
        label="비밀번호 확인", widget=forms.PasswordInput, required=True)
    phoneNum = forms.CharField(
        label="전화번호", help_text='ex) 010-1234-5678 형식으로 기재해주세요.')

    class Meta:
        model = User
        fields = ['name', 'email', 'password',
                  'check_password', 'phoneNum', 'area']

# 기관만의 추가 폼
class OrganForm(forms.ModelForm):
    class Meta:
        model = Organ
        fields = ['crew', 'head', 'url']


# 기관에서 봉사활동 등록폼
class ServiceForm(forms.ModelForm):
    name = forms.CharField(label="봉사활동명")
    Essential = forms.BooleanField(label="필수퀘스트 여부")
    point = forms.IntegerField(label="퀘스트 포인트")
    level = forms.IntegerField(label="퀘스트 레벨")
    number = forms.IntegerField(label="퀘스트 인원")
    emergency = forms.BooleanField(label="긴급퀘스트 여부")
    image = forms.ImageField(label="이미지 등록")
    class Meta:
        model = Service
        fields = ['name', 'Essential', 'point',
                  'level', 'number', 'emergency', 'image']
