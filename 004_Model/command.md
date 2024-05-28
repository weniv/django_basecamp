# 목표
1. 모델을 만들어 데이터를 DB에 저장하고 템플릿에 템플릿 태그로 출력
    * DB의 관계 1:1, 1:N, N:M은 추후 강의합니다.
2. 이미지를 비롯한 다양한 데이터를 업로드 해보고 불러오기
3. 웹 서비스에서 데이터 검색 기능 구현

# django
```python

mkdir db
cd db
python -m venv venv
.\venv\Scripts\activate
pip install django
pip install pillow
django-admin startproject tutorialdjango .
python manage.py migrate
python manage.py startapp main
python manage.py startapp blog

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
    "main",
    "blog",
]

################################

# URL 구조 작성(기획 단계), 연습할 때에도 이걸 만들어놓고 연습하시기를 권고합니다.

'blog/'
'blog/<int:pk>/'

################################
# tutorialdjango > urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include("main.urls")),
    path("blog/", include("blog.urls")),
]


################################
# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
]

################################
# blog > views.py

from django.shortcuts import render


def blog_list(request):
    return render(request, "blog/blog_list.html")


def blog_detail(request, pk):
    return render(request, "blog/blog_detail.html")


################################
# 기본 templates 변경

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


################################
# 아래 파일들 생성

templates > blog > blog_list.html
templates > blog > blog_test.html
templates > blog > blog_detail.html

################################
# blog > models.py
# https://docs.djangoproject.com/en/5.0/ref/models/fields/
# 어떤 항목을 게시판에 게시할지 기획 => 기획된 항목들이 어떤 타입인지 ref 문서에서 확인

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 처음 생성될 때에만
    updated_at = models.DateTimeField(auto_now=True) # 수정될 때마다

################################

python manage.py makemigrations # 파이썬 코드로 DB를 만질 수 있는 코드를 생성(0001_initial.py, 명세서라고 이해하시면 좋습니다.)
python manage.py migrate # 위에 생성된 코드로 실제 DB를 만지는 명령

################################
# blog > admin.py

from django.contrib import admin
from .models import Post

admin.site.register(Post)  # admin page 커스터마이징은 뒤에서 배웁니다.

################################

python manage.py createsuperuser
leehojun
leehojun@gmail.com
dlghwns1234!
dlghwns1234!

################################

python manage.py runserver

################################

/admin으로 로그인 후 게시물 3개 작성

################################
# blog > admin.py

from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at", "updated_at"]


admin.site.register(Post, PostAdmin)

################################

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 처음 생성될 때에만
    updated_at = models.DateTimeField(auto_now=True)  # 수정될 때마다

    def __str__(self):
        # https://docs.python.org/ko/3/library/datetime.html#strftime-and-strptime-format-codes
        create_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        update_time = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"제목: {self.title}, 생성시간: {create_time}, 수정시간: {update_time}"


################################
# blog > views.py 수정

from django.shortcuts import render
from .models import Post


def blog_list(request):
    blogs = Post.objects.all()
    context = {
        "object_list": blogs,
    }
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    blogs = Post.objects.get(pk=pk)
    context = {
        "object": blogs,
    }
    return render(request, "blog/blog_detail.html", context)


################################
# templates > blog > blog_list.html

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>게시판</h1>
    <ul>
        {% for post in object_list %}
            <li>
                <a href="{% url 'blog_detail' post.pk %}">{{ post.title }}</a>
            </li>
        {% endfor %}
    </ul>
    <p>{% url 'blog_list' %}</p>
    <p>{% url 'blog_detail' 1 %}</p>
</body>
</html>

################################
# templates > blog > blog_detail.html

<!DOCTYPE html>
<html lang="ko">
<head>
    <title>blog_detail</title>
</head>
<body>
    <h1>blog_detail</h1>
    <h2>{{ object.title }}</h2>
    <p>{{ object.content }}</p>
    <p>{{ object.created_at }}</p>
    <p>{{ object.updated_at }}</p>
    <a href="{% url 'blog_list' %}">목록</a>
</body>
</html>


################################
ORM(Object Relational Mapping), Django Shell, QuerySet : https://paullabworkspace.notion.site/ORM-Django-Shell-QuerySet-4c1ad20735ce44c483d6ff9071bd092c?pvs=4
공식문서 : https://docs.djangoproject.com/en/5.0/ref/models/querysets/#django.db.models.query.QuerySet
jupyter notebook 사용 : https://youtu.be/Di5CYnoHYRk

python manage.py shell

eq - equal ( = )
ne - not equal ( <> )
lt - little ( < )
le - little or equal ( <= )
gt - greater ( > )
ge - greater or equal ( >= )



>>> from blog.models import Post
>>> Post.objects.all()
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>, <Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수 :39:14, 수정시간: 2024-02-23 02:39:14>, <Post: 제목: 3, 생성시간: 2024-02-23 02:39:17, 수정시간: 2024-02-23 02:39:17>]>
>>> data = Post.objects.all()
>>> type(data)
<class 'django.db.models.query.QuerySet'>
>>> dir(data)
['__aiter__', '__and__', '__bool__', '__class__', '__class_getitem__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eoc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__t_s_', '__iinit_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__or__', '__reduce__', '__reduce, 'tattr__'_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '__xor__', '_add_hann', '_chaints', '_annotate', '_batched_insert', '_chain', '_check_bulk_create_options', '_check_operator_queryset', '_check_ordering_firstet_ator_que_last_queryset_aggregation', '_clone', '_combinator_query', '_db', '_defer_next_filter', '_deferred_filter', '_earliest', '_extra', lude', 'ct_model_params', '_fetch_all', '_fields', '_filter_or_exclude', '_filter_or_exclude_inplace', '_for_write', '_has_filters', '_hi_itcts', '_nts', '_insert', '_iterable_class', '_iterator', '_known_related_objects', '_merge_known_related_objects', '_merge_sanity_check',_noh_relate '_next_is_sticky', '_not_support_combined_queries', '_prefetch_done', '_prefetch_related_lookups', '_prefetch_related_objects', e',pdate', 
'_prepare_for_bulk_create', '_query', '_raw_delete', '_result_cache', '_sticky_filter', '_update', '_validate_values_are_expressie',ete', 'aons', '_values', 'aaggregate', 'abulk_create', 'abulk_update', 'acontains', 'acount', 'acreate', 'adelete', 'aearliest', 'aexists', as', 'al', 'aexplain', 'afirst', 'aget', 'aget_or_create', 'aggregate', 'ain_bulk', 'aiterator', 'alast', 'alatest', 'alias', 'all', 'ann'aucreate',otate', 'as_manager', 'aupdate', 'aupdate_or_create', 'bulk_create', 'bulk_update', 'complex_filter', 'contains', 'count', 'creater'er', 'fie', 'dates', 'datetimes', 'db', 'defer', 'delete', 'difference', 'distinct', 'earliest', 'exclude', 'exists', 'explain', 'extra',te'', 'pref 'filter', 'first', 'get', 'get_or_create', 'in_bulk', 'intersection', 'iterator', 'last', 'latest', 'model', 'none', 'only', 'oruer_create'der_by', 'ordered', 'prefetch_related', 'query', 'raw', 'resolve_expression', 'reverse', 'select_for_update', 'select_related', ', 'union', 'update', 'update_or_create', 'using', 'values', 'values_list']

# Read
>>> Post.objects.all().order_by('-pk')
<QuerySet [<Post: 제목: 3, 생성시간: 2024-02-23 02:39:17, 수정시간: 2024-02-23 02:39:17>, <Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수정시간: 2024-02-23 02:39:14>, <Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>]>
>>> Post.objects.count()
3
>>> q = Post.objects.get(id=1)
>>> q
# q의 __str__ 입니다. 우리가 만들어준 코드입니다.
<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>
>>> q.title
'1'
>>> q['title']
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: 'Post' object is not subscriptable
>>> q.id
1
>>> q.pk
1
>>> q.content
'11'
>>> q.created_at
datetime.datetime(2024, 2, 23, 2, 39, 11, 936704, tzinfo=datetime.timezone.utc)
>>> Post.objects.filter(title='1')
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>]>
>>> Post.objects.filter(title='2')
<QuerySet [<Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수정시간: 2024-02-23 02:39:14>]>
>>> Post.objects.filter(id=1)
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>]>
>>> Post.objects.filter(title__contains='1')
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>]>
>>> Post.objects.filter(content__contains='1')
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>]>
>>> Post.objects.filter(content__contains='1').filter(title__contains='1')
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>]>
>>> Post.objects.filter(id__lt=3)
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>, <Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수정시간: 2024-02-23 02:39:14>]>
>>> Post.objects.filter(id__lt=2)
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>]>
>>> Post.objects.filter(id__gt=2)
<QuerySet [<Post: 제목: 3, 생성시간: 2024-02-23 02:39:17, 수정시간: 2024-02-23 02:39:17>]>
>>> Post.objects.filter(id__lt=3)[0]
<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>
>>> Post.objects.filter(id__lt=3)
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>, <Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수정시간: 2024-02-23 02:39:14>]>
>>> Post.objects.filter(id__lt=3)[:2]
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>, <Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수정시간: 2024-02-23 02:39:14>]>


# Create
>>> q = Post.objects.create(title='c4', content='c44')
>>> q.title
'c4'
>>> q.created_at
datetime.datetime(2024, 2, 23, 5, 9, 23, 820194, tzinfo=datetime.timezone.utc)
>>> dir(q)
[... 생략 ...'delete', 'from_db', 'full_clean', 'get_constraints', 'get_deferred_fields', 'get_next_by_created_at', 'get_next_by_updated_at', 'get_previous_by_created_at', 'get_previous_by_updated_at', 'id', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'title', 'unique_error_message', 'updated_at', 'validate_constraints', 'validate_unique']
>>> q.save()
>>> Post.objects.all()
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>, <Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수정시간
: 2024-02-23 02:39:14>, <Post: 제목: 3, 생성시간: 2024-02-23 02:39:17, 수정시간: 2024-02-23 02:39:17>, <Post: 제목: c4, 생성시간: 2024-02-23 05:05:58, 수정시간: 2024-02-23 05:05:58>, <Post: 제목: c4, 생성시간: 2024-02-23 05:09:23, 수정시간: 2024-02-23 05:11:36>]>
>>> q = Post.objects.create(title='c1', content='c11')        
>>> Post.objects.all()
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>, <Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수정시간
: 2024-02-23 02:39:14>, <Post: 제목: 3, 생성시간: 2024-02-23 02:39:17, 수정시간: 2024-02-23 02:39:17>, <Post: 제목: c4, 생성시간: 2024-02-23 05:05:58, 수정시간: 2024-02-23 05:05:58>, <Post: 제목: c4, 생성시간: 2024-02-23 05:09:23, 수정시간: 2024-02-23 05:11:36>, <Post: 제목: c1, 생성시간: 
2024-02-23 05:13:00, 수정시간: 2024-02-23 05:13:00>]>
>>> q.save()
>>> q = Post.objects.filter(title__contains='1')
>>> q
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>, <Post: 제목: c1, 생성시간: 2024-02-23 05:13:00, 수정시
간: 2024-02-23 05:13:31>]>
>>> q = Post.objects.filter(content__contains='1')
>>> q
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>, <Post: 제목: c1, 생성시간: 2024-02-23 05:13:00, 수정시
간: 2024-02-23 05:13:31>]>


# Delete
>>> q = Post.objects.get(pk=3) 
>>> q.delete()
(1, {'blog.Post': 1})
>>> q
<Post: 제목: 3, 생성시간: 2024-02-23 02:39:17, 수정시간: 2024-02-23 02:39:17>
>>> Post.objects.all()
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>, <Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수정시간
: 2024-02-23 02:39:14>, <Post: 제목: c4, 생성시간: 2024-02-23 05:05:58, 수정시간: 2024-02-23 05:05:58>, <Post: 제목: c4, 생성시간: 2024-02-23 05:09:23, 수정시간: 2024-02-23 05:11:36>, <Post: 제목: c1, 생성시간: 2024-02-23 05:13:00, 수정시간: 2024-02-23 05:13:31>]>


# Update
>>> q = Post.objects.all()[0]
>>> q.title
'1'
>>> q.title = 'hello world1'
>>> q
<Post: 제목: hello world1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>
>>> Post.objects.all()
<QuerySet [<Post: 제목: 1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 02:39:11>, <Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수정시간
: 2024-02-23 02:39:14>, <Post: 제목: c4, 생성시간: 2024-02-23 05:05:58, 수정시간: 2024-02-23 05:05:58>, <Post: 제목: c4, 생성시간: 2024-02-23 05:09:23, 수정시간: 2024-02-23 05:11:36>, <Post: 제목: c1, 생성시간: 2024-02-23 05:13:00, 수정시간: 2024-02-23 05:13:31>]>
>>> q.save()
>>> Post.objects.all()
<QuerySet [<Post: 제목: hello world1, 생성시간: 2024-02-23 02:39:11, 수정시간: 2024-02-23 05:18:58>, <Post: 제목: 2, 생성시간: 2024-02-23 02:39:14, 수정시간: 2024-02-23 02:39:14>, <Post: 제목: c4, 생성시간: 2024-02-23 05:05:58, 수정시간: 2024-02-23 05:05:58>, <Post: 제목: c4, 생성시간: 2024-02-23 05:09:23, 수정시간: 2024-02-23 05:11:36>, <Post: 제목: c1, 생성시간: 2024-02-23 05:13:00, 수정시간: 2024-02-23 05:13:31>]>


################################
# 게시물 생성
# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("create/<str:title>/", views.blog_create, name="blog_create"),
    path("test/", views.blog_test, name="test"),
]

################################
# 게시물 생성
# blog > views.py

from django.shortcuts import render, redirect
from .models import Post


def blog_list(request):
    blogs = Post.objects.all()
    context = {"db": blogs}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    blog = Post.objects.get(pk=pk)
    context = {"db": blog}
    return render(request, "blog/blog_detail.html", context)


def blog_create(request, title):
    contents = f"hello world {title}"
    q = Post.objects.create(title=title, contents=contents)
    q.save()
    return redirect("blog_list")


def blog_test(request):
    return render(request, "blog/blog_test.html")

################################

http://127.0.0.1:8000/blog/create/orm/
http://127.0.0.1:8000/blog/create/jeju/
http://127.0.0.1:8000/blog/create/hello/

################################
# 게시물 삭제
# blog > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("create/<str:title>/", views.blog_create, name="blog_create"),
    path("delete/<int:pk>/", views.blog_delete, name="blog_delete"),
]

################################
# blog > views.py

from django.shortcuts import render, redirect
from .models import Post


def blog_list(request):
    blogs = Post.objects.all()
    context = {"db": blogs}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    blog = Post.objects.get(pk=pk)
    context = {"db": blog}
    return render(request, "blog/blog_detail.html", context)


def blog_create(request, title):
    contents = f"hello world {title}"
    q = Post.objects.create(title=title, contents=contents)
    q.save()
    return redirect("blog_list")


def blog_delete(request, pk):
    q = Post.objects.get(pk=pk)
    q.delete()
    return redirect("blog_list")


################################

http://127.0.0.1:8000/blog/delete/1/
http://127.0.0.1:8000/blog/delete/2/

################################

* 간편하게 DB 정리 방법
1. 프로그램 사용
https://sqlitebrowser.org/dl/
다운로드 받아 실행한 후 '데이터베이스 구조' 말고 '데이터 보기' 탭 클릭하여 데이터 삭제하고 '변경사항 저장하기'한 다음 django에서 확인
2. 덮어쓰기
기존에 DB를 별도에 폴더에 넣어두었다가 덮어쓰기
3. GitHub commit 돌아가기 기능을 사용

################################

# django models fields
# https://docs.djangoproject.com/en/4.2/ref/models/fields/
# pillow는 이미지 관련 라이브러리입니다.
# 매우 많은 프레임웤이나 라이브러리가 이 라이브러리를 사용합니다.
# 이미지를 자르거나, 확대하거나, 축소하거나, 저장하거나 등이 사용됩니다.

pip install pillow

################################
# blog > models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    main_image = models.ImageField(upload_to='blog/', blank=True, null=True) 
    # upload_to='blog/' : blog 폴더 안에 저장
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# * blank=True는 '이 필드는 필수가 아니다'라는 내용입니다.
# * null=True는 '이 필드는 새로 생성되어도 DB 비어있어도 된다.'
# 1번게시물 - 이미지 없음
# 2번게시물 - 이미지 없음
# 3번게시물 => main_image 필드 추가, 그러면 1번게시물? 2번게시물?은 어떻게 하죠?
# -> django가 입력을 하라고 얘기를 합니다. 입력을 거기서 해줍니다.
# -> null=True를 주셔서 이전 게시물이 비어있어도 된다라고 명시해줍니다.

################################

python manage.py makemigrations # 파이썬 코드로 DB를 만질 수 있는 코드를 생성(0001_initial.py, 명세서라고 이해하시면 좋습니다.)
python manage.py migrate # 위에 생성된 코드로 실제 DB를 만지는 명령

################################
# 초기에 이렇게 세팅을 많이 합니다.

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

################################

메인프로젝트폴더 > media
메인프로젝트폴더 > static

################################

이미지까지 업로드 한 게시물 3개 작성

# => 이미지를 클릭해보면 이미지가 안나옵니다?
# 파일이 저장되었는지 확인
# => a.jpg만 3개 올렸는데 아래처럼 저장되었습니다.
# => media/a.jpg
# => media/a_난수.jpg
# => media/a_난수.jpg

################################
# tutorialdjango > urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include("main.urls")),
    path("blog/", include("blog.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



################################
# blog_detail.html

<!DOCTYPE html>
<html lang="ko">
<head>
    <title>blog_detail</title>
</head>
<body>
    <h1>blog_detail</h1>
    <h2>{{ object.title }}</h2>
    <p>{{ object.content }}</p>
    <p>{{ object.created_at }}</p>
    <p>{{ object.updated_at }}</p>
    {% if object.main_image %}
        <img src="{{ object.main_image.url }}" alt="">
    {% endif %}
    <a href="{% url 'blog_list' %}">목록</a>
</body>
</html>

################################
# blog_list.html

<h1>게시판</h1>
<form action="" method="get">
    <input name="q" type="search">
    <button type="submit">검색</button>
</form>
<ul>
    {% for blog_detail in db %}
    <li>
        <a href="{% url 'blog_detail' blog_detail.id %}">{{ blog_detail.title }}</a>
        <p>{{blog_detail.contents}}</p>
    </li>
    {% endfor %}
</ul>

################################
from django.shortcuts import render
from .models import Post
from django.shortcuts import redirect
from django.db.models import Q


def blog_list(request):
    print(request.GET)
    if request.GET.get("q"):
        q = request.GET.get("q")
        blogs = Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        ).distinct()
    else:
        blogs = Post.objects.all()
    # blogs = Post.objects.filter(title__contains="j")
    context = {
        "object_list": blogs,
    }
    return render(request, "blog/blog_list.html", context)
    
################################