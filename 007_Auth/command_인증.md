# 목표
1. 인증(로그인, 로그아웃) 구현
2. 인증된 유저만 읽을 수 이는 페이지 구현
3. 인증이 되고 자신의 글인 경우에만 수정 및 삭제할 수 있는 페이지 구현
4. 비밀번호 저장, 해쉬 알고리즘에 대한 이해

# 명령어
```python


################################
# 기획

다음 url이 실제 작동하도록 해주세요.
1.1 ''                          : 메인페이지
1.2 'accounts/signup/'          : 회원가입
1.3 'accounts/login/'           : 로그인
1.4 'accounts/logout/'          : 로그아웃 - 로그인 사용자
1.5 'accounts/profile/'         : 프로필 - 로그인 사용자
2.1 'blog/'                     : 블로그 글 목록
2.2 'blog/<int:pk>/'            : 블로그 상세 글 읽기
2.3 'blog/create/'              : 블로그 글 작성 - 로그인 사용자
2.4 'blog/update/<int:pk>/'     : 블로그 글 업데이트(수정하기) - 로그인 사용자 & 내 글인 경우
2.5 'blog/delete/<int:pk>/'     : 블로그 글 삭제 - 로그인 사용자 & 내 글인 경우


################################

mkdir accounts
cd accounts
python -m venv venv
.\venv\Scripts\activate
pip install django
pip install pillow
pip freeze > requirements.txt
django-admin startproject tutorialdjango .
python manage.py migrate
python manage.py startapp main
python manage.py startapp blog
python manage.py startapp accounts


###################################
# settings.py

ALLOWED_HOSTS = ['*'] # 28번째 줄에 접속할 수 있는 사람을 모든 사람으로 변경

# settings.py 에서 33번째 라인 수정
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'blog',
    'accounts',
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

###################################
# mysite > media 폴더 생성
# mysite > static 폴더 생성

mkdir static
mkdir media
mkdir templates

################################

python manage.py createsuperuser

leehojun
leehojun@gmail.com
이호준1234!

################################
# blog > models.py
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
################################

python manage.py makemigrations
python manage.py migrate

################################
# blog > admin.py

from django.contrib import admin
from .models import Post

admin.site.register(Post)

################################

python manage.py runserver

게시물 3개 업로드하고 시작

################################
# tutorialdjango > urls.py
# main은 만들었지만 사용하진 않습니다.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
]

################################
# 저는 아래 순서로 코딩합니다.
# 1. urls.py
# 2. views.py
# 3. models.py 
# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("create/", views.blog_create, name="blog_create"),
    path("update/<int:pk>/", views.blog_update, name="blog_update"),
    path("delete/<int:pk>/", views.blog_delete, name="blog_delete"),
]

################################
# blog > views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Post
from .forms import PostForm


def blog_list(request):
    if request.GET.get("q"):
        posts = Post.objects.filter(
            Q(title__contains=request.GET.get("q"))
            | Q(contents__contains=request.GET.get("q"))
        ).distinct()
    else:
        posts = Post.objects.all()
    context = {"object_list": posts}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {"object": post}
    print(request.user.is_authenticated)
    print(request.user)
    print(post.author)
    return render(request, "blog/blog_detail.html", context)


def blog_create(request):
    if request.method == "GET":
        form = PostForm()
        context = {"form": form}
        return render(request, "blog/blog_create.html", context)
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("blog_list")
        else:
            context = {
                "form": form,
                "error": "입력이 잘못되었습니다. 알맞은 형식으로 다시 입력해주세요!",
            }
            return render(request, "blog/blog_create.html", context)


def blog_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {"form": form, "pk": pk}
        return render(request, "blog/blog_update.html", context)


def blog_delete(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    print(post)
    if request.method == "POST":
        post.delete()
    return redirect("blog_list")

################################
# forms.py
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = ["title", "contents"]
        fields = "__all__"

################################
# accounts > urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.user_signup, name="user_signup"),
    path("login/", views.user_login, name="user_login"), # login, logout 등에 함수명은 사용하지 마세요.
    path("logout/", views.user_logout, name="user_logout"),
    path("profile/", views.user_profile, name="user_profile"),
]

################################
# accounts > views.py
from django.shortcuts import render


def user_signup(request):
    pass


def user_login(request):
    pass


def user_logout(request):
    pass


def user_profile(request):
    pass

################################
# accounts > views.py 내용입니다.
# 실무에서는 대부분 CBV를 사용합니다. 
# 후반부에 CBV 코드를 놓을테니 얼마나 짧아지는지 나중에 확인해주세요.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def user_signup(request):
    if request.method == "POST":
        # 회원가입 처리 로직
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST.get("email", "")  # 이메일은 선택적으로 처리
        if not (username and password):
            return HttpResponse("이름과 패스워드는 필수입니다.")

        # 동일한 사용자 이름이나 이메일을 가진 사용자가 이미 있는지 검사
        if User.objects.filter(username=username).exists():
            return HttpResponse("유저이름이 이미 있습니다.")
        if email and User.objects.filter(email=email).exists():
            return HttpResponse("이메일이 이미 있습니다.")

        # 새 사용자 생성
        user = User.objects.create_user(username, email, password)
        user.save()

        # 그냥 create하면 비밀번호가 암호화되지 않습니다.
        # 암호화 하지 않고 저장을 해버리면 로그인이 안됩니다.(작동을 안합니다.)
        # 아래 주석 처리된 코드는 위의 코드와 동일한 기능을 합니다.
        # user = User(username=username, email=email)
        # user.set_password(password)  # 이렇게 하면 비밀번호가 암호화됩니다.
        # user.save()

        # 자동 로그인 처리
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("user_profile")
    else:
        # GET 요청 시 회원가입 폼 페이지 렌더링
        return render(request, "accounts/signup.html")


def user_login(request):
    """
    이 함수 이름은 login으로 하지 않기를 권장합니다.
    login은 이미 장고에서 제공하는 함수명이기 때문입니다.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print("hello")
        print(user)
        if user is not None:
            login(request, user)
            # 로그인 성공 시 프로필 페이지로 리다이렉트
            return redirect("user_profile")
        else:
            # 로그인 실패 시, 로그인 폼과 에러 메시지를 다시 렌더링
            return render(
                request,
                "accounts/login.html",
                {"error": "아이디나 패스워드가 맞지 않습니다."},
            )
    else:
        # GET 요청 시 로그인 폼 페이지 렌더링
        return render(request, "accounts/login.html")


def user_logout(request):
    # 사용자 로그아웃
    logout(request)
    # 로그아웃 후 리다이렉트할 페이지, 예를 들어 로그인 페이지
    return redirect("user_login")


@login_required
def user_profile(request):
    # login_required 데코레이터는 사용자가 로그인하지 않은 상태에서 이 페이지에 접근하려고 하면,
    # 설정된 로그인 URL로 리다이렉트합니다.
    return render(request, "accounts/profile.html", {"user": request.user})


################################
# hash알고리즘
md5(이거는 깨졌습니다. 사용하시면 안됩니다.)
sha256
sha512

원본
leehojun

sha256(64개의 문자열)
859E57E3
E4197F11
C95F97DF
171B77F7
E03FA280
6D86A5DE
1C65CCC5
04C42831

원본
leehojun2

sha256(64개의 문자열, 지난 텍스트와 연관성이 없습니다.)
94D748F3C756496422CE4F0FBC29F2D483F4E75BA9CE6FE48BDB071C5FE369C0


원본
아주 큰 소설, 이미지, 영상

sha256(그래도 64개의 문자열을 줍니다.)
94D748F3C756496422CE4F0FBC29F2D483F4E75BA9CE6FE48BDB071C5FE369C0


원본 -> sha256 값은 되지만
sha256 -> 원본으로는 불가합니다.

그렇기 때문에 DB에 password를 sha256을 저장하면 해커가 해킹해도 user의 패스워드를 알지 못합니다!

---

md5(32자) => 레인보우어택으로 깨졌습니다.

1q2w3e4r! => 1E9E9F6FEF3369CDC763284D80AE5FEB
admin => 21232F297A57A5A743894A0E4A801FC3

해커가 해킹을 했는데 21232F297A57A5A743894A0E4A801FC3 를 발견했습니다! 이 패스워드는 무엇일까요? 족보를 저장해두었는데 저기에서 찾는 것입니다! 이걸 레인보우 어택이라 합니다.

---
salt(암호화 소금)

admin + 'hojun' => md5
1q2w3e4r! + 'hojun' => md5


adminhojun => B73105D4A2A8B8AE6F7A19C268437A46

이제는 '소금' 값을 알지 못하면 B73105D4A2A8B8AE6F7A19C268437A46 이 무엇인지 알지 못합니다.

---
소금을 연속으로 돌리는 방법
B73105D4A2A8B8AE6F7A19C268437A46 + 'hojun'

=> 5E7F66BFBDA59C8B3D6C3F03638A2E56

많이 할 수록 보안성은 올라가겠네요? => 성능이 떨어집니다.

################################

templates > blog > blog_list.html
templates > blog > blog_detail.html
templates > blog > blog_create.html
templates > blog > blog_update.html
templates > accounts > profile.html
templates > accounts > login.html
templates > accounts > signup.html

################################
# blog_list.html

<ul>
    {% for blog in object_list %}
    <li><a href="/blog/{{blog.id}}">{{blog.title}}</a></li>
    {% endfor %}
</ul>

################################
# blog_detail.html

<p>{{object.title}}</p>
<p>{{object.contents}}</p>

<!-- 로그인을 했고, 내가 이 글에 글쓴이라고 한다면 삭제와 업데이트 버튼 노출 -->
{% if user.is_authenticated and user == object.author %}
    <a href="{% url 'blog_update' object.pk %}">수정</a>
    <form action="{% url 'blog_delete' object.pk %}" method="post">
        {% csrf_token %}
        <input type="submit" value="삭제">
    </form>
{% endif %}

################################
# blog_update.html

<form action="" method="post">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <input type="submit">
</form>

################################
# blog_create.html

<form action="" method="post">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <input type="submit">
</form>

################################
# profile.html

<h1>개인 프로필 페이지</h1>
<p>{{ user }}</p>
<p>{{ user.username }}</p>
<p>{{ user.email }}</p>
<p>{{ user.first_name }}</p>
<p>{{ user.last_name }}</p>
<p>{{ user.is_staff }}</p>
<p>{{ user.is_active }}</p>
<p>{{ user.is_superuser }}</p>
<p>{{ user.last_login }}</p>
<p>{{ user.date_joined }}</p>

<form action="{% url 'user_logout' %}" method="post">
  {% csrf_token %}
  <input type="submit" value="로그아웃">
</form>

################################
# login.html

<form method="post">
    {% csrf_token %}
    <label for="username_id">아이디</label>
    <input id="username_id" type="text" name="username">

    <label for="password_id">비밀번호</label>
    <input id="password_id" type="password" name="password">

    <button type="submit">로그인</button>
</form>

################################
# signup.html
# {% csrf_token %}는 form에 안쪽에 있어야 합니다.

<form action="" method="post">
    {% csrf_token %}
    <label for="username_id">아이디</label>
    <input id="username_id" type="text" name="username">

    <label for="email_id">이메일</label>
    <input id="email_id" type="text" name="email">
    

    <label for="password_id">비밀번호</label>
    <input id="password_id" type="password" name="password">
    
    <button type="submit">회원가입</button>
</form>

################################

python manage.py runserver

# 실습하기 전 admin페이지와 http://127.0.0.1:8000/ 페이지 2개를 띄어주세요.
# blog는 들어갈 필요 없습니다. 생성되는 것을 구현하지 않았으니까요. user클릭해서 user만 확인해주세요.

http://127.0.0.1:8000/accounts/login/
http://127.0.0.1:8000/accounts/profile/
http://127.0.0.1:8000/accounts/signup/
http://127.0.0.1:8000/accounts/logout/

################################

로그인이 필요한 서비스는 앞으로 @login_require를 사용하시면 됩니다.

################################
# 실습X
# 클래스 기반 뷰
# views.py

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.shortcuts import render
from django.http import HttpResponse


signup = CreateView.as_view(
    form_class=UserCreationForm,
    template_name="accounts/signup.html",
    success_url=settings.LOGIN_URL,
)


login = LoginView.as_view(
    template_name="accounts/login.html",
)


logout = LogoutView.as_view(
    next_page=settings.LOGOUT_URL,
)


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
```