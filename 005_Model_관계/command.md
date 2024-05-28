# 목표
1. DB 설계
2. 1:1, 1:N, N:M 관계 구현

# 명령어
```python

mkdir db
cd db
python -m venv venv
.\venv\Scripts\activate
pip install django
pip install pillow
django-admin startproject tutorialdjango .
python manage.py migrate
python manage.py startapp blog

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
    'blog',
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

###################################
# blog > models.py

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(
        upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

###################################
# blog > admin.py

from django.contrib import admin
from .models import Post

admin.site.register(Post)

###################################

python manage.py makemigrations
python manage.py migrate

###################################

python manage.py createsuperuser

leehojun
leehojun@gmail.com
이호준1234!

###################################
# tutorialdjango > urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

###################################
# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
]

###################################
# blog > views.py

from django.shortcuts import render
from .models import Post


def blog_list(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "blog/blog_list.html", context)


###################################
# blog > templates > blog > blog_list.html

비어있는 파일로 만들어주세요!

###################################

python manage.py runserver

# admin page 들어가셔서 게시물 3개 생성

###################################
모델 실습 교안 링크 : https://www.notion.so/paullabworkspace/Model-RDB-ERD-1-N-N-M-1-1-f34426c3b50c49c1adcda1a652dfa2c1

ERD 도구: https://www.erdcloud.com/, https://dbdiagram.io/, https://mermaid.live/edit
활용: ChatGPT에게 ERD 그려달라 요청 또는 추후 views.py로 ERD 시각화 요청

# 1:N


from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    head_image = models.ImageField(upload_to="blog/images/%Y/%m/%d/", blank=True)
    file_upload = models.FileField(upload_to="blog/files/%Y/%m/%d/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # '1:N'인 경우 ForeignKey는 N쪽에 작성한다.

    def __str__(self):
        return self.title


###################################
python manage.py makemigrations
# => fix해라!? 이전에 입력했던 게시물들 어떻게 할꺼냐!?
# => 1. 지금 넣어라
# => 2. 종료시키고 null=True를 주어라!
# 1번 입력하고 >>> 1 입력!
# 1번 유저가 author로 들어가게 됨.
# '1:N'에서 '1'에 대응하는 id 값
python manage.py migrate

###################################

python manage.py runserver
/admin으로 접속 후 다른 유저 만들고 게시물 할당해서 user 삭제해보기

###################################
# 실습 X

# author = models.ForeignKey(User, on_delete=models.CASCADE)
# 위 코드에서 on_delete=models.SET_NULL을 넣으면 삭제가 아니라 빈칸이 됩니다.

###################################
# templates > blog > blog_list.html
{% for i in posts %}
    <h1>{{ i.title }}</h1>
    <p>{{ i.content }}</p>
    <p>{{ i.author }}</p>
    <hr>
{% endfor %}

###################################
# 1:N, N:M 추가!
# views.py
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(
        upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    # N:M 관계를 만들어줍니다. 어디서든 정의해도 상관 없습니다.
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    '''
    related_name은 Post에서 Comment를 부를 때 사용할 이름입니다. 
    만약 이름을 licat이라 바꾸면 템플릿 문법에서 아래와 같이 호출됩니다.
    {% for comment in post.licat.all %}
    ForeignKey는 1:N 관계를 만들어줍니다. 단, N에서 정의합니다.
    '''
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.message
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


###################################
# 실습 X

# 1:1관계는 아래와 같습니다. 1:1관계는 주로 확장에서 많이 사용됩니다. 예를 들어 Student의 확장으로 '교환학생' 모델을 만들어서 국적등을 관리할 수 있습니다. 데이터를 최적화하기 위해서도 사용합니다.

# models.OneToOneField(Student, on_delete=models.CASCADE)

###################################

python manage.py makemigrations
python manage.py migrate

###################################
# admin.py

from django.contrib import admin
from .models import Post, Comment, Tag

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)

###################################

python manage.py runserver

뎃글 생성
태그 생성
연결
지우기

등을 실습

###################################
# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
]

###################################

from django.shortcuts import render
from .models import Post

def blog_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/blog_list.html', {'posts':posts})

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, "blog/blog_detail.html", {"post": post})

###################################
# blog_detail.html

<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>
<p>{{ post.author }}</p>

###################################
# blog_list.html

{# 여기서 posts는 post의 objects.all() #}
{# 여기서 post는 post의 objects.get() #}

{% for post in posts %}
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
    <p>{{ post.author }}</p>
    <!-- 필드에 없어도 1:N으로 연결되었으면 1쪽에서도 접근 가능합니다. N쪽에서는 변수명이 있기 때문에 당연히 접근이 가능합니다. -->
    <!-- 그렇지만 아래처럼 접근하면 None입니다! 이유는 comments 전체를 로딩할 수가 없습니다. -->
    <p>{{ post.comments }}</p>
    <p>{{ post.tags }}</p>
    {% for comment in post.comments.all %}
        <p>{{ comment.message }}</p>
    {% endfor %}
    {% for tag in post.tags.all %}
        <p>{{ tag.name }}</p>
    {% endfor %}
    <hr>
{% endfor %}

###################################
# blog_detail.html

<h1>{{ post.title }}</h1>
<p>{{ post.author }}</p>
<p>{{ post.content }}</p>

{% for tag in post.tags.all %}
    <p>{{ tag.name }}</p>
{% endfor %}

{% for comment in post.comments.all %}
    <p>{{ comment.message }}</p>
{% endfor %}

###################################
# blog_detail.html 
# 조금만 꾸며보겠습니다. 따라하지 않으셔도 됩니다. 다시 원복됩니다.

<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>
<p>{{ post.author }}</p>

<style>
    section {
        border: solid 1px black;
        margin: 10px;
        padding: 10px;
    }
</style>

<section>
    <h2>태그</h2>
    {% for tag in post.tags.all %}
        <p style="color:blue">#{{ tag.name }}</p>
    {% endfor %}
</section>

<section>
    <h2>댓글</h2>
    {% for comment in post.comments.all %}
        <p>{{ comment.message }}</p>
    {% endfor %}
</section>


###################################
# blog_detail.html

<h1>{{ post.title }}</h1>
<p>{{ post.author }}</p>
<p>{{ post.content }}</p>

{% for tag in post.tags.all %}
    <a href="/blog/tag/{{ tag.name }}">#{{ tag.name }}</a>
{% endfor %}

{% for comment in post.comments.all %}
    <p>{{ comment.message }}</p>
{% endfor %}

###################################
# views.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("tag/<str:tag>/", views.blog_tag, name="blog_tag"),
]

###################################
# blog_detail.html

<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>
<p>{{ post.author }}</p>

{% for tag in post.tags.all %}
    <a href="/blog/tag/{{ tag.name }}">#{{ tag.name }}</a>
{% endfor %}

{% for comment in post.comments.all %}
    <p>{{ comment.message }}</p>
{% endfor %}

<form action="" method="post">
    {% csrf_token %}
    <input type="text" name="message">
    <input type="submit">
</form>


###################################
# views.py

from django.shortcuts import render
from .models import Post, Comment, Tag


def blog_list(request):
    posts = Post.objects.all()
    return render(request, "blog/blog_list.html", {"posts": posts})


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        author = request.user
        message = request.POST["message"]
        c = Comment.objects.create(author=author, message=message, post=post)
        c.save()
    return render(request, "blog/blog_detail.html", {"post": post})


def blog_tag(request, tag):
    posts = Post.objects.filter(tags__name__iexact=tag)
    return render(request, "blog/blog_list.html", {"posts": posts})
```