from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

# 일반 유저
class User(AbstractBaseUser, PermissionsMixin):
    # 기본 내용
    email = models.EmailField('이메일', unique=True)
    name = models.CharField('이름', max_length=30, blank=True)
    is_staff = models.BooleanField('스태프 권한', default=False)
    is_active = models.BooleanField('사용중', default=True)
    date_joined = models.DateTimeField('가입일', default=timezone.now)
    # 커스터마이징
    codeNum = models.IntegerField(blank=True, null=True, verbose_name="주민번호")                # 주민 번호
    phoneNum = models.IntegerField(blank=True, null=True, verbose_name="전화번호")               # 핸드폰 번호
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='user_job', blank=True, null=True, verbose_name="직업")# 직업
    license = models.CharField(max_length=20, blank=True, null=True, verbose_name="자격증")    # 자격증
    level = models.IntegerField(default=1)  # 레벨
    point = models.IntegerField(default=0)  # 가지고 있는포인트
    area = models.ForeignKey('Area', on_delete=models.CASCADE, related_name='user_area', blank=True, null=True, verbose_name="지역")  # 지역
    another = models.CharField(max_length=100, blank=True, null=True, verbose_name="기타 특이사항")   # 비고
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="사진")  # 이미지
    is_organ = models.BooleanField(default=False, verbose_name="기관 여부") # 일반 회원인지, 기관 회원인지 확인
    organ = models.OneToOneField('Organ', on_delete=models.CASCADE,related_name='user_organ', blank=True, null=True)  # 기관에 대한 정보

    objects = UserManager()
    USERNAME_FIELD = 'email'    # email을 사용자의 식별자로 설정
    REQUIRED_FIELDS = ['name']  # email을 사용자의 식별자로 설정

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        swappable = 'AUTH_USER_MODEL'

    def __str(self):
        return self.name

# 기관 유저에 대해 이어줄 테이블 
class Organ(models.Model):
    crew = models.CharField(max_length=20, verbose_name="소속")                # 소속
    head = models.CharField(max_length=20, verbose_name="책임자명")             # 책임자명
    url = models.CharField(max_length=500, default="", verbose_name="URL")     # 인터넷 주소
    def __str(self):
        return self.Cuser.username

# 봉사 활동 -> 일반 유저와 기관 유저와 연결
class Service(models.Model):
    name = models.CharField(max_length=40)          # 봉사활동명
    Essential = models.BooleanField(default=True)   # 필수 퀘스트인지의 여부
    Finish = models.BooleanField(default=False)     # 봉사활동의 등록 마감 여부
    point = models.IntegerField()                   # 봉사활동에 해당하는 포인트
    level = models.IntegerField()                   # 어느 레벨에서 열리는지의 레벨
    organ = models.ForeignKey('User', on_delete=models.CASCADE, related_name="service_organ")    # 기k관
    user = models.ManyToManyField('User', related_name='service_user')    # 이에 대한 퀘스트를 할 유저
    number = models.IntegerField(default=15)        # 봉사활동에 참여할 수 있는 최대의 유저 _ 일반 유저가 참여할 때 마다 1씩 차감
    emergency = models.BooleanField(blank=False)    # 긴급 봉사인지의 여부
    image = models.ImageField(upload_to='images/', blank=True)  # 이미지
    def __str__(self):
        return self.name

# 지역
class Area(models.Model):
    area = models.CharField(max_length=20)  # 지역
    def __str__(self):
        return self.area

# 직업
class Job(models.Model):
    job = models.CharField(max_length=20)   # 직업
    def __str__(self):
        return self.name

# 상품
class Product(models.Model):
    name = models.CharField(max_length=30)  # 상품명
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name="products") # 상품의 브랜드
    point = models.IntegerField()           # 해당 상품의 포인트
    image = models.ImageField(upload_to='images/', blank=True)
    def __str__(self):
        return self.name

# 브랜드
class Brand(models.Model):
    name = models.CharField(max_length=20)  # 브랜드명
    image = models.ImageField(upload_to='images/', blank=True)  # 브랜드 이미지
    def __str__(self):
        return self.name

# Create your models here.
