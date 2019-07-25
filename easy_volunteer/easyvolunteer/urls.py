from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),                               # 메인 페이지
    path('introduce', views.introduce, name='introduce'),            # 소개 페이지
    path('select', views.select, name='select'),                     # 기관/회원 회원가입 선택 페이지
    path('organ_signup', views.organ_signup, name='organ_signup'),   # 기관 회원 가입 페이지
    path('user_signup', views.user_signup, name='user_signup'),      # 일반 회원 가입 페이지
    path('signin', views.signin, name='signin'),                     # 로그인 페이지
    path('mypage', views.mypage, name='mypage'),                     # 일반 회원 로그인 페이지
    path('organ_mypage', views.organ_mypage, name='organ_mypage'),   # 기관 회원 로그인 페이지
    path('register', views.register, name='register'),               # 기관에서 봉사 등록 페이지
    path('quest', views.quest, name='quest'),                        # 일반 회원이 봉사 등록 페이지
    path('point', views.point, name='point'),                        # 일반 회원이 포인트 사용하는 페이지
    path('', include('django.contrib.auth.urls')),                   # 로그아웃
]
