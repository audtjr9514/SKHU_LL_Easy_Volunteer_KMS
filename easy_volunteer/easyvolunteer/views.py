from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from .models import User, Organ, Service, Area, Job, Product, Brand
from .forms import SigninForm, UserForm, OrganUserForm, OrganForm, ServiceForm

# 맨 첫화면 _ 메인 페이지
def main(request):
    return render(request, 'main.html')

# 소개 페이지
def introduce(request):
    return render(request, 'introduce.html')

# 회원가입에서 기관/일반회원을 고를수 있는 선택 페이지
def select(request):
    return render(request, 'select.html')

# 기관 회원가입 페이지
def organ_signup(request):
    if request.method == "POST":
        organ_user_form = OrganUserForm(request.POST)
        organ_form = OrganForm(request.POST)
        if organ_user_form.is_valid() and organ_form.is_valid()and organ_user_form.cleaned_data["password"] == organ_user_form.cleaned_data["check_password"]:
            organ_user = User.objects.create_user(
                name = organ_user_form.cleaned_data['name'], 
                email = organ_user_form.cleaned_data['email'], 
                password = organ_user_form.cleaned_data['password'], 
                phoneNum= organ_user_form.cleaned_data['phoneNum'], 
                area = organ_user_form.cleaned_data['area']                
            )
            organ = Organ.objects.create(
                crew=organ_form.cleaned_data["crew"],
                head=organ_form.cleaned_data['head'],
                url=organ_form.cleaned_data['url']
            )
            organ_user.is_organ = True
            organ_user.organ = organ
            organ_user.save()
            login(request, organ_user)
            return redirect('main')    
    else:
        organ_user_form = OrganUserForm()
        organ_form = OrganForm()
        return render(request, 'organ_signup.html', {'organ_user_form': organ_user_form, 'organ_form': organ_form})


# 일반 회원가입 페이지
def user_signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid() and form.cleaned_data["password"] == form.cleaned_data["check_password"]:
            new_user = User.objects.create_user(
            name=form.cleaned_data["name"], 
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            codeNum=form.cleaned_data["codeNum"],
            phoneNum=form.cleaned_data["phoneNum"],
            job=form.cleaned_data["job"],
            license=form.cleaned_data["license"],
            area=form.cleaned_data["area"],
            another=form.cleaned_data["another"],
            image=form.cleaned_data["image"])
            login(request, new_user)
            return redirect('main')
        else:
            form = UserForm()
            return render(request, 'main', {'form': form})
    else:
        form = UserForm()
        return render(request, 'user_signup.html', {'form': form})

# 로그인 페이지
def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email = email, password = password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'signin.html', {'errormessage': "로그인 정보가 틀렸습니다."})
    else:
        form = SigninForm()
        return render(request, 'signin.html', {'form': form})


# 일반 회원 마이페이지
def mypage(request): 
    users = User.objects.all()
    service = Service.objects.all()
    organs = Organ.objects.all()
    return render(request, 'mypage.html', {'users': users, 'service': service, 'organs': organs})

# 개인 정보 수정
def user_update(request, user=None):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save
    return render(request, 'user_update.html')

# 기관용 마이페이지
def organ_mypage(request):
    return render(request, 'organ_mypage.html')

# 기관에서 봉사 등록 페이지
def register(request, service=None):
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save(commit=False)
            service.organ = request.user
            service.save()
            return render(request, 'main.html')
    else:
        form = ServiceForm()
        return render(request, 'register.html', {'form': form})

# 봉사활동을 선택할 수 있는 페이지
def quest(request):
    users = User.objects.all()
    service = Service.objects.all()
    organs = Organ.objects.all()
    return render(request, 'quest.html', {'users': users, 'service': service, 'organs': organs})

#봉사활동 선택 후 업데이트
def quest_update(request, service_id, user_id):
    service = get_object_or_404(Service, id=service_id)
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        if service.number > 0:
            if user.level >= service.level:
                user = User.objects.get(pk=user_id)
                service.user.add(user)
                service.number = service.number - 1
                service.save()
                return render(request, 'thanks2.html', {'username': user.name, 'service_name': service.name})
            else:
                return render(request, 'thanks2.html', {'errormessage': "level이 낮습니다."})
        else:
            return render(request, 'thanks2.html', {'errormessage': "인원이 마감되었습니다."})
    else:
        return render(request, 'thanks2.html', {'errormessage': "비정상적인 접근입니다."})
# 회원이 포인트를 사용할 수 있는 페이지


def point(request):
    brands = Brand.objects.all()
    products = Product.objects.all()
    return render(request, 'point.html', {'brands': brands, 'products': products})

# 회원이 포인트 사용 후 페이지
def point_update(request, product_id, user_id):
    product = get_object_or_404(Product, id=product_id)
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        if user.point >= product.point:
            user.point = user.point - product.point
            user.save()
            return render(request, 'thanks.html', {'username': user.name, 'product_name': product.name, 'user_point': user.point})
        else:
            return render(request, 'thanks.html', {'errormessage': "포인트가 부족합니다."})
    else:
        return render(request, 'thanks.html', {'errormessage': "비정상적인 접근법입니다."})
