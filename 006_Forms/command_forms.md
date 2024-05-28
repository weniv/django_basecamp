# 목표
1. forms.py 역할 이해하기
2. forms.py로 입력폼 만들기
3. forms.py로 모델 연결하여 입력폼 간소화하기

# 명령어
```python

mkdir mysite
cd mysite
python -m venv venv
.\venv\Scripts\activate
pip install django
pip install pillow
pip freeze > requirements.txt
django-admin startproject tutorialdjango .
python manage.py migrate
python manage.py startapp blog

# 추가된 명령어 pip freeze > requirements.txt에 대하여
# pip install -r requirements.txt # 추후 이 파일을 통해 설치합니다.
# 왜 이 파일이 필요한가요? 이 버전대로 설치하기 위해서 입니다.
# 여러분도, 저도 GitHub에 가상환경을 제외하고 올리니까요!

################################

# urls 기획
1. 다음 url이 실제 작동하도록 해주세요.
1.1 'blog/'                     : 블로그 글 목록
1.2 'blog/<int:pk>/'            : 블로그 상세 글 읽기
1.3 'blog/create/'              : 블로그 글 작성 - (인증을 배운 후에는 로그인한 사용자만 작성)

###################################
앱이름: blog                views 함수이름        html 파일이름  비고
'blog/'                     blog_list            blog_list.html	
'blog/<int:pk>/'            blog_detail          blog_detail.html
'blog/create/'              blog_create          blog_create.html

################################
# tutorialdjango > settings.py

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
]

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

################################
# mysite > static 폴더 생성
# mysite > media 폴더 생성

mkdir static
mkdir media

################################
# tutorialdjango > urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
]


################################
# blog > urls.py(생성 후 아래 내용 넣어주세요.)

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("create/", views.blog_create, name="blog_create"),
]

################################
# blog > views.py

from django.shortcuts import render


def blog_list(request):
    return render(request, "blog/blog_list.html")


def blog_detail(request, pk):
    return render(request, "blog/blog_detail.html")


def blog_create(request):
    return render(request, "blog/blog_create.html")

################################

blog > templates > blog > blog_list.html
blog > templates > blog > blog_detail.html
blog > templates > blog > blog_create.html

# window 노트북인 경우
# blog 폴더에서 아래 명령어로 파일 생성 가능합니다.
# echo '' >> blog_list.html
# 위 명령어는 간소화가 가능합니다.
# ''>blog_list.html;''>blog_detail.html;''>blog_create.html

# 맥북이나 리눅스 계열 노트북, git bash인 경우
# touch blog_list.html blog_detail.html blog_create.html


################################

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    main_image = models.ImageField(upload_to="blog/%Y/%m/%d/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

python manage.py createsuperuser

leehojun
leehojun@gmail.com
이호준1234!

################################
# tutorialdjango > urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

################################

python manage.py runserver 

# 게시물 3개 생성

################################
# blog > views.py 코드 추가

from django.shortcuts import render
from .models import Post


def blog_list(request):
    posts = Post.objects.all()
    context = {"object_list": posts}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {"object": post}
    return render(request, "blog/blog_detail.html", context)


def blog_create(request):
    return render(request, "blog/blog_create.html")


################################
# blog/blog_list.html

<h1>게시판</h1>
<form action="" method="get">
    <input type="search" name="q">
    <button type="submit">검색</button>
</form>
<ul>
    {% for post in db %}
    <li>
        <a href="{% url 'blog_detail' post.id %}">{{ post.title }}</a>
        <p>{{ post.contents }}</p>
    </li>
    {% endfor %}
</ul>
################################
# blog/blog_detail.html
<h1>게시판</h1>

<p>{{ object.title }}</p>
<p>{{ object.contents }}</p>
<p>{{ object.created_at }}</p>
<p>{{ object.updated_at }}</p>
<p>{{ object.id }}</p>
{% if object.main_image %}
<img src="{{ object.main_image.url }}" alt="">
{% endif %}
<a href="{% url 'blog_list' %}">뒤로가기</a>

################################
# blog > views.py

from django.shortcuts import render
from django.db.models import Q
from .models import Post
# from .forms import PostForm


def blog_list(request):
    if request.GET.get("q"):
        db = Post.objects.filter(
            Q(title__contains=request.GET.get("q"))
            | Q(contents__contains=request.GET.get("q"))
        ).distinct()
        # 기본으로 배우는 sqlite3에서는 대소문자 구분이 안됩니다.
        # Django와 자주 사용하는 postgresql에서는 대소문자 구분이 됩니다.
        # namefield__icontains는 대소문자를 구분하지 않고
        # namefield__contains는 대소문자를 구분합니다.
    else:
        db = Post.objects.all()
    context = {"object_list": db}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {"object": post}
    return render(request, "blog/blog_detail.html", context)


def blog_create(request):
    # form = PostForm()
    # context = {"form": form}
    '''
    이렇게 생성된 form은 자동으로 form을 만들어주는 기능을 가지고 있습니다.
    또한 유효성 검증 등의 다양한 기능도 가지고 있습니다.
    이렇게 안하면 하나씩 직접 form을 만들어야 합니다. 
    이해하긴 일일이 만드는 것이 더 좋기 때문에 먼저 form을 직접 만들고
    얼마나 쉽게 자동으로 만들어지는지 추후 확인하도록 하겠습니다.
    '''
    return render(request, "blog/blog_create.html")

################################

python manage.py runserver
blog/
blog/1/
실행확인

################################

# blog > templates > blog > blog_create.html
<form action="" method="post">
    {# 해킹 공격 방어를 위한 토큰입니다. #}
    {% csrf_token %}
    title: <input type="text" name="title"><br>
    contents: <input type="text" name="contents"><br>
    <button type="submit">저장</button>
</form>

################################

blog/create/

def blog_create(request):
    print(request.POST.get("title"))
    print(request.POST.get("contents"))
    return render(request, "blog/blog_create.html")

# views.py 수정해놓고 실행해보세요.

################################
# blog > views.py

from django.shortcuts import render
from django.db.models import Q
from .models import Post
from django.shortcuts import redirect

# from .forms import PostForm


def blog_list(request):
    if request.GET.get("q"):
        db = Post.objects.filter(
            Q(title__contains=request.GET.get("q"))
            | Q(contents__contains=request.GET.get("q"))
        ).distinct()
        # 기본으로 배우는 sqlite3에서는 대소문자 구분이 안됩니다.
        # Django와 자주 사용하는 postgresql에서는 대소문자 구분이 됩니다.
        # namefield__icontains는 대소문자를 구분하지 않고
        # namefield__contains는 대소문자를 구분합니다.
    else:
        db = Post.objects.all()
    context = {"object_list": db}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {"object": post}
    return render(request, "blog/blog_detail.html", context)


def blog_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        contents = request.POST.get("contents")
        q = Post.objects.create(title=title, contents=contents)
        q.save()
        return redirect("blog_list")
    return render(request, "blog/blog_create.html")




################################
# blog > forms.py
# 입력창에 들어갈 데이터 또는 입력창에서 입력된 데이터를 forms.py로 관리하는 것을 권합니다.
# 꼭 이름이 forms.py일 필요는 없습니다. forms.Form을 상속받고 있다면요.

from django import forms


class PostForm(forms.Form):  # PostForm은 여러분이 원하는 이름으로 바꿔도 됩니다. forms.Form은 기본 form입니다. 이는 추후 forms.ModelForm로 바뀌어야 합니다.
    title = forms.CharField()
    contents = forms.CharField()

################################
# blog > views.py

from .forms import PostForm # 최상단 주석 풀어주세요.


def blog_create(request):
    form = PostForm()
    context = {"form": form}
    return render(request, "blog/blog_create.html", context)

################################
# blog > templates > blog > blog_create.html

<form action="" method="post">
    {# 해킹 공격 방어를 위한 토큰입니다. #}
    {% csrf_token %}
    <ul>
        {{ form.as_ul }}
    </ul>
    <button type="submit">저장</button>
</form>

################################
# blog > templates > blog > blog_create.html

<form action="" method="post">
    {# 해킹 공격 방어를 위한 토큰입니다. #}
    {% csrf_token %}
    <table>
    {{ form.as_table }}
    </table>
    <button type="submit">저장</button>
</form>


################################
# blog > templates > blog > blog_create.html
# 정리된 파일입니다.

<form action="{% url 'blog_create' %}" method="post">
    {# 해킹 공격 방어를 위한 토큰입니다. #}
    {% csrf_token %}

    {% comment %}

        <!-- 주석입니다. 나중에 여러개를 해보세요. 제공하고 있는 형태가 많습니다. -->
        <!-- https://docs.djangoproject.com/en/5.0/ref/forms/api/ -->
        {{ form }}
        {{ form.as_p }}
        {{ form.as_div }}

        <!-- ul 태그를 위에 하나 만들어주어야 합니다. 자주 사용합니다. -->
        <ul>
            {{ form.as_ul }}
        </ul>

        <!-- ol 태그, 거의 사용하지 않습니다. -->
        <ol>
            {{ form.as_ol }}
        </ol>

        <!-- table 태그를 위에 하나 만들어주어야 합니다. -->
        <table>
            {{ form.as_table }}
        </table>

        <!-- 필드를 하나씩 나열합니다. -->
        {{ form.title }}
        {{ form.contents }}

    {% endcomment %}
    
    {{ form }}

    <button type="submit">저장</button>
</form>

################################
# blog > views.py

def blog_create(request):
    if request.method == "GET":
        print("GET으로 들어왔습니다!")
        form = PostForm()
        context = {"form": form}
        return render(request, "blog/blog_create.html", context)
    elif request.method == "POST":
        print("POST로 들어왔습니다!")
        print(request.POST)
        form = PostForm(request.POST)
        if form.is_valid():
            # form.is_valid()를 통과하면 form.cleaned_data를 통해 데이터를 가져올 수 있습니다. form.is_valid() 이걸 안하면 form.cleaned_data 사용할 수 없습니다. 호출도 불가합니다!
            print(form)
            print(form.data)
            print(form.cleaned_data["title"])
            print(type(form))
            print(dir(form))
            """
            'add_error', 'add_initial_prefix', 'add_prefix', 'as_div', 'as_p', 'as_table', 'as_ul', 'auto_id', 'base_fields', 'changed_data', 'clean', 'cleaned_data', 'data', 'declared_fields', 'default_renderer', 'empty_permitted', 'error_class', 'errors', 'field_order', 'fields', 'files', 'full_clean', 'get_context', 'get_initial_for_field', 'has_changed', 'has_error', 'hidden_fields', 'initial', 'is_bound', 'is_multipart', 'is_valid', 'label_suffix', 'media', 'non_field_errors', 'order_fields', 'prefix', 'render', 'renderer', 'template_name', 'template_name_div', 'template_name_label', 'template_name_p', 'template_name_table', 'template_name_ul', 'use_required_attribute', 'visible_fields'
            """
            return render(request, "blog/blog_create.html")
        else:
            context = {"form": form}
            return render(request, "blog/blog_create.html", context)

################################
# forms.py에서 우리가 작성한 models와 forms를 연결하는 작업

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField()
    contents = forms.CharField()

    class Meta:
        model = Post
        fields = ["title", "contents"]

################################
# blog > views.py 주석과 print 제거버전
# 위 생략
from django.shortcuts import redirect

# ... 생략 ...

def blog_create(request):
    if request.method == "GET":
        form = PostForm()
        context = {"form": form}
        return render(request, "blog/blog_create.html", context)
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            # detail로 가야한다!
            # return redirect('blog_detail', pk=post.pk)
            return redirect("blog_list")
        else:
            context = {"form": form}
            return render(request, "blog/blog_create.html", context)


################################
# forms.py에 조건을 하나 두고 테스트 해보도록 하겠습니다.
from django import forms
from .models import Post


class PostForm(forms.ModelForm):  # PostForm은 여러분이 원하는 이름으로 바꿔도 됩니다.
    title = forms.CharField(max_length=10)
    contents = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ["title", "contents"]

################################
# forms.py에 조건을 하나 두고 테스트 해보도록 하겠습니다.
# => blog > views.py error 추가

def blog_create(request):
    if request.method == "GET":
        form = PostForm()
        context = {"form": form}
        return render(request, "blog/blog_create.html", context)
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            # detail로 가야한다!
            # return redirect("blog_details", pk=post.pk)
            return redirect("blog_list")
        else:
            context = {
                "form": form,
                "error": "입력이 잘못되었습니다. 알맞은 형식으로 다시 입력해주세요!",
            }
            return render(request, "blog/blog_create.html", context)
################################
# error 메시지 출력
# blog > templates > blog > create.html

<p style="color:red;">{{ error }}</p>
<form action="{% url 'blog_create'%}" method="post">
    {% csrf_token %}
    {{ form }}
    <button type="submit">저장</button>
</form>
################################

개발자 도구 열어 maxlength를 임의적으로 수정합니다!
=> 경고 문구 뜨는 것까지 확인

################################
# blog > blog_details.html

<h1>게시판</h1>

<p>{{ object.title }}</p>
<p>{{ object.contents }}</p>
<p>{{ object.created_at }}</p>
<p>{{ object.updated_at }}</p>
<p>{{ object.id }}</p>
{% if object.main_image %}
<img src="{{ object.main_image.url }}" alt="">
{% endif %}
<a href="{% url 'blog_list' %}">뒤로가기</a>

<!-- 삭제하기 버튼 -->
{% comment %}
<form action="{% url 'blog_delete' object.id %}" method="post">
    {% csrf_token %}
    <button type="submit">삭제하기</button>
</form>
{% endcomment %}

################################
# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("create/", views.blog_create, name="blog_create"),
    path("<int:pk>/delete/", views.blog_delete, name="blog_delete"),
]

################################
# blog > views.py

def blog_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect("blog_list")

################################
# 이미지 필드 추가!
# forms.py에서 max_length와 main_image필드를 추가했습니다!

from django import forms
from .models import Post


class PostForm(forms.ModelForm):  # PostForm은 여러분이 원하는 이름으로 바꿔도 됩니다.
    title = forms.CharField(max_length=100)
    contents = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ["title", "contents", "main_image"]
        # fields = '__all__'

################################
# 이미지 필드 추가!
# views.py

def blog_create(request):
    if request.method == "GET":
        form = PostForm()
        context = {"form": form}
        return render(request, "blog/blog_create.html", context)
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES) # 수정
        if form.is_valid():
            post = form.save()
            # detail로 가야한다!
            # return redirect("blog_details", pk=post.pk)
            return redirect("blog_list")
        else:
            context = {
                "form": form,
                "error": "입력이 잘못되었습니다. 알맞은 형식으로 다시 입력해주세요!",
            }
            return render(request, "blog/blog_create.html", context)

################################
# 이미지 필드 추가!
# blog_create.html

<p style="color:red;">{{ error }}</p>
<form action="{% url 'blog_create'%}" method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form }}
    <button type="submit">저장</button>
</form>

################################
# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("create/", views.blog_create, name="blog_create"),
    path("<int:pk>/update/", views.blog_update, name="blog_update"),
    path("<int:pk>/delete/", views.blog_delete, name="blog_delete"),
]
################################
# views.py

from django.shortcuts import get_object_or_404


def blog_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {"form": form, "pk": pk}
        return render(request, "blog/blog_update.html", context)

def blog_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("blog_list")


################################
# blog_update.html
<p style="color:red;">{{ error }}</p>
<form action="" method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form }}
    <button type="submit">저장</button>
</form>

################################
# blog_detail.html
<h1>게시판</h1>

<p>{{ object.title }}</p>
<p>{{ object.contents }}</p>
<p>{{ object.created_at }}</p>
<p>{{ object.updated_at }}</p>
<p>{{ object.id }}</p>
{% if object.main_image %}
<img src="{{ object.main_image.url }}" alt="">
{% endif %}

<!-- 삭제하기 버튼 -->
<form action="{% url 'blog_delete' object.id %}" method="post">
    {% csrf_token %}
    <button type="submit">삭제하기</button>
</form>
<a href="{% url 'blog_update' object.id %}">수정</a>

<a href="{% url 'blog_list' %}">뒤로가기</a>
```