# 목표
1. 여러개의 앱, 여러개의 urls.py 파일 분기
2. 템플릿 폴더 별도로 만들어 서빙
3. 템플릿 상속을 이용하여 중복되는 구조를 하나의 파일에서 서빙 (base.html 파일 상속)
4. static 파일 서빙

# django
```python

# 앞 부분의 자세한 설명은 이전 강의를 참고해주세요.

mkdir mysite
cd mysite
python -m venv venv

.\venv\Scripts\activate # window
source ./venv/bin/activate # mac, linux

pip install django
django-admin startproject tutorialdjango .
python manage.py migrate

# python manage.py runserver

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

''
'about/'
'contact/'
'blog/'
'blog/<int:pk>/'

앱이름: main
URL             views 함수이름	 html 파일이름	    비고
''              index           index.html
'about/'        about
'contact/'      contact

앱이름: blog
URL             views 함수이름  html 파일이름     비고
'blog/'         blog_list      blog_list.html	
'blog/<int:pk>' blog_detail    blog_detail.html  게시물이 없을 경우에는 404로 연결

################################
# tutorialdjango > urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("blog/", include("blog.urls")),
]

################################
# main > urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]

# name은 URL의 고유 별칭입니다. 
# 템플릿에서 이 별칭을 이용해 이 URL에 접근할 수 있습니다.

################################
# main > views.py

from django.shortcuts import render


def index(request):
    return render(request, "main/index.html")


def about(request):
    return render(request, "main/about.html")


def contact(request):
    return render(request, "main/contact.html")


################################
# tutorialdjango > settings.py
# 기본 템플릿 폴더를 변경해서 앞으로는 mysite > templates라는 폴더에서 통합 관리합니다.

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

>>> from pathlib import Path
>>> file_path = './hello/world'
>>> p = Path(file_path)
>>> p / 'templates/'
>>> p / 'templates/' / 'hojun'

################################
# 아래 파일들 생성

templates > main > index.html
templates > main > about.html
templates > main > contact.html

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
# 아래 파일들 생성

templates > blog > blog_list.html
templates > blog > blog_detail.html

################################

python manage.py runserver

http://127.0.0.1:8000
http://127.0.0.1:8000/about/
http://127.0.0.1:8000/contact/
http://127.0.0.1:8000/blog/
http://127.0.0.1:8000/blog/10/

################################
# blog > views.py 수정

from django.shortcuts import render

blog_database = [
    {
        "id": 1,
        "title": "제목1",
        "content": "내용1",
        "created_at": "2021-02-22",
        "updated_at": "2021-02-22",
        "author": "홍길동",
        "category": "일상",
        "tag": ["태그1", "태그2"],
        "view_count": 0,
        "thumbnail": "https://picsum.photos/200/300",
        "like_count": 3,
        "like_user": [10, 20, 21],
    },
    {
        "id": 2,
        "title": "제목2",
        "content": "내용2",
        "created_at": "2021-02-23",
        "updated_at": "2021-02-23",
        "author": "김철수",
        "category": "일기",
        "tag": ["태그1", "태그3"],
        "view_count": 0,
        "thumbnail": "https://picsum.photos/200/300",
        "like_count": 10,
        "like_user": [10, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    },
    {
        "id": 3,
        "title": "제목3",
        "content": "내용3",
        "created_at": "2021-02-24",
        "updated_at": "2021-02-24",
        "author": "이영희",
        "category": "맛집",
        "tag": ["태그1", "태그3"],
        "view_count": 0,
        "thumbnail": "https://picsum.photos/200/300",
        "like_count": 20,
        "like_user": [10, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    },
    {
        "id": 4,
        "title": "제목4",
        "content": "내용4",
        "created_at": "2021-02-25",
        "updated_at": "2021-02-25",
        "author": "박민수",
        "category": "여행",
        "tag": ["태그1", "태그3"],
        "view_count": 0,
        "thumbnail": "https://picsum.photos/200/300",
        "like_count": 30,
        "like_user": [10, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    },
]


def blog_list(request):
    # blogs = Blog.objects.all() # 실제로는 이렇게 데이터베이스에서 가져옴
    context = {"object_list": blog_database}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    # blog = Blog.objects.get(pk=pk) # 실제로는 이렇게 데이터베이스에서 가져옴
    context = {"object": blog_database[pk - 1]}
    return render(request, "blog/blog_detail.html", context)


# render(request, html파일, context(딕셔너리 형태))
# => html파일을 일반 텍스트로 가져옵니다. 중괄호와 같은 문법이 나오면 context에 있는 값을 가져와서 넣어줍니다. 그리고 이것을 사용자에게 넘겨주는 역활을 합니다. 넘겨줄 때에는 HttpResponse를 사용합니다.
# => request는 사용자가 보내는 요청에 대한 정보가 담겨있습니다. 이 요청에 로그인 정보 등이 담겨있습니다. 나중에는 이것을 이용해서 template에서 로그인 정보를 출력하게 한다던지, 로그인 정보가 없으면 로그인 페이지로 이동하게 한다던지 등에 기능을 할 수 있습니다.
# 함수 각각을 직접 다 읽어보시는 것은 권하지는 않습니다. 가볍게 훑어보시는 정도는 괜찮습니다. https://github.com/django/django/blob/main/django/http/response.py 여기에 있는 HttpResponse를 보시면 됩니다. django의 공식 소스코드입니다.



################################
# templates > blog > blog_list.html

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
</head>
<body>
    <h1>bloglist</h1>
    <ul>
        {% for blog in object_list %}
        <li>
            {{ forloop.counter }}
            {# 주석입니다. 'url 'blog_detail' blog.id' 와 같은 형태는 urls.py에서 blog_detail이라는 name을 가진 url을 찾습니다. 그걸로만 연결을 해주는데 뒤에 값이 들어가야 할 경우, 파라미터가 있는 경우! 뒤에 띄어쓰기로 아규먼트를 넣어줄 수 있습니다. 결국에는 blog.id가 blog_detail에 pk로 들어가는 것입니다. #}
            <a href="{% url 'blog_detail' blog.id %}">{{ blog.title }}</a>
        </li>
        {% endfor %}
    </ul>
</body>
</html>

# <a href="{% url 'blog_detail' blog.id %}">{{ blog.title }}</a> 이렇게 사용하지 않고
# <a href="/blog/{{blog.id}}/">{{ blog.title }}</a> 이렇게 개발하는 경우도 종종 있습니다.
# 이렇게 코딩하는 것을 '하드코딩'이라고 합니다.
# 다만 이렇게 코딩하면 유지보수성이 떨어집니다! 그래서 실무에서는 이런 하드코딩 패턴을 피해야 합니다.
# '시간이 부족하여' 빠르게 코딩해야 할 일이 생기기도 하는데요. 나중에 유지보수를 생각하면 아무리 급해도 80점짜리 코드를 짜도록 노력하시는 편이 좋습니다.

# 어떤 경우에 하드코딩을 하여 유지보수가 힘든 일이 생길까요?
# 예를 들어 
# 1. /blog/이 url이 변경이 되거나
# 2. blog/notice/1처럼 깊이가 변하는 경우
# 하드 코딩을 하면 모두 찾아서 수정해야 합니다.

################################
# templates > blog > blog_detail.html

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>blogdetail</title>
</head>
<body>
    <h1>blogdetail</h1>
    <h2>{{ object.title }}</h2>
    <p>{{ object.content }}</p>
    <p>{{ object.created_at }}</p>
    <p>{{ object.updated_at }}</p>
    <a href="{% url 'blog_list' %}">목록</a>
</body>
</html>

################################
# 템플릿 상속
# 예를 들어 메뉴는 모든 페이지에 다 있어야 하는데 똑같은 코드를 다 작성해야 하나요?
# 다 작성했는데 메뉴가 하나 추가되었어요. 수백개의 메뉴 바를 다 수정해야 하나요?
# 반복되고 주요한 것들은 상속을 이용해서 1개의 파일로만 관리합니다.

# header, footer, aside => 주로 1개의 파일로만 관리가 됩니다.

# 이를 해결하기 위해 앞서 배웠던 템플릿 태그 중 템플릿 상속 태그가 존재합니다.

* 부모코드(상속해주는 코드)

...부모 위 코드...
{% block 자식이름 %}
{% endblock %}
...부모 아래 코드...

* 자식코드(상속받는 코드)
{% extends '부모html파일명' %}
{% block 자식이름 %}
... 실제 사용할 자식 코드 ...
{% endblock %}

################################
# templates > base > base.html
# 부모코드!
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>weniv blog</title>
</head>
<body>
    <header>
        <h1>weniv blog</h1>
        <nav>
            <ul>
                <li>메뉴1</li>
                <li>메뉴2</li>
                <li>메뉴3</li>
            </ul>
        </nav>
    </header>

    <main>
        {% block contents %}
        <p>test 이어서 써집니다1</p>
        <p>test 이어서 써집니다2</p>
        {% endblock %}
    </main>

    <footer>
        <p>저작권은 weniv에게 있습니다.</p>
    </footer>
</body>
</html>
################################
# templates > blog > blog_list.html
# 자식코드!
{% extends 'base/base.html '%}

{% block contents %}
<h1>bloglist</h1>
<ul>
    {% for blog in blog_list %}
    <li>
        {{ forloop.counter }}
        <a href="{% url 'blog_detail' blog.id %}">{{ blog.title }}</a>
    </li>
    {% endfor %}
</ul>
{% endblock %}
################################
# templates > blog > blog_detail.html
# 자식코드!
{% extends 'base/base.html '%}

{% block contents %}
<h1>blogdetail</h1>
<h2>{{ blog.title }}</h2>
<p>{{ blog.content }}</p>
<p>{{ blog.created_at }}</p>
<p>{{ blog.updated_at }}</p>
<a href="{% url 'blog_list' %}">목록</a>
{% endblock %}

################################
# 템플릿 상속 나아가기
# templates > base > base.html
# 부모코드!
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>weniv blog</title>
</head>
<body>
    <header>
        <h1>weniv blog</h1>
        <nav>
            <ul>
                <li>메뉴1</li>
                <li>메뉴2</li>
                <li>메뉴3</li>
            </ul>
        </nav>
    </header>

    <main>
        {% block contents %}
        <p>test 이어서 써집니다1</p>
        <p>test 이어서 써집니다2</p>
        {% endblock %}
    </main>

    {% block binky %}
    {% endblock %}

    <footer>
        <p>저작권은 weniv에게 있습니다.</p>
    </footer>

    {% block mura %}
    {% endblock %}
</body>
</html>

################################
# templates > blog > blog_liste.html
# 자식코드!
{% extends 'base/base.html '%}

{% block contents %}
<h1>bloglist</h1>
<ul>
    {% for blog in blog_list %}
    <li>
        {{ forloop.counter }}
        <a href="{% url 'blog_detail' blog.id %}">{{ blog.title }}</a>
    </li>
    {% endfor %}
</ul>
{% endblock %}

{% block binky %}
<h2>binky test</h2>
{% endblock %}


{% block mura %}
<script>
    console.log('mura test');
</script>
{% endblock %}


################################
# settings.py
# static파일은 정적으로 서빙해야 하는 파일들이 있는 곳입니다.
# 예를 들어 css, js 등을 의미합니다.
# 사용자가 올린 이미지처럼 변화가 있는 파일은 동적 파일입니다.

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

################################
# static 폴더를 최상위에 만들고 각각 폴더를 만들어주세요.
mysite > static > css > custom.css
mysite > static > js > custom.js

################################
# 이 폴더에서 로드해야 하는 모든 html에 아래와 같이 수정, 변경해야 합니다.
# 만약 여러분이 이 작업을 매우~ 많이 해야 한다면 .py파일로 gen.py파일을 만들어주세요.
# (메크로를 만드시는 편이 공수가 덜 드신다 생각이 되시면요.)

{% load static %} # 최 상위 1번
{% static 'STATIC_URL 이후의 경로' %} # 정적 파일을 로드하고 있는 모든 경로
# 실제로 /static/css/styles.css 이런식으로 하드코딩해도 작동하긴 합니다.
# 유지보수가 어려워질 뿐이죠.

# 상대경로로 되어 있는 모든 것, 예를 들어 아래 있는 것들은 static이라고 고쳐주셔야 합니다.

script의 src
img의 src
background-image: url()
link의 href

* 상대경로: ./ 이렇게 시작하거나, 파일명이나 폴더명부터 시작을 하는 경로명(현재 파일 기준)
* 절대경로: C:\... 이렇게 시작하거나, https:// 이렇게 시작하는 경로명

################################

# 상속작업 +
    * 주의사항: load static은 태그 자체가 상속이 되진 않습니다. 그래서 파일마다 아래와 같은 구조로 넣어주셔야 합니다.(자식 파일에 최상위에 기입합니다.)
    {% extends 'base.html' %}
    {% block contents %}
    {% load static %}
    ... 내용 ....
    {% endblock %}

################################
# templates > base.html
# 다음 소스코드에서 상대경로를 탬플릿 태그를 통해 변경해주세요.
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>weniv blog</title>
    <link rel="stylesheet" href="css/custom.css">
</head>
<body>
    <header>
        <h1>weniv blog</h1>
        <nav>
            <ul>
                <li>메뉴1</li>
                <li>메뉴2</li>
                <li>메뉴3</li>
            </ul>
        </nav>
    </header>

    <main>
        {% block contents %}
        <p>test 이어서 써집니다1</p>
        <p>test 이어서 써집니다2</p>
        {% endblock %}
    </main>

    {% block binky %}
    {% endblock %}

    <footer>
        <p>저작권은 weniv에게 있습니다.</p>
    </footer>

    {% block mura %}
    {% endblock %}
    <script src="js/custom.js"></script>
</body>
</html>


###########################
{% load static %}
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>weniv blog</title>
    <link rel="stylesheet" href="{% static 'css/custom.css' %}">
</head>
<body>
    <header>
        <h1>weniv blog</h1>
        <nav>
            <ul>
                <li>메뉴1</li>
                <li>메뉴2</li>
                <li>메뉴3</li>
                <li>메뉴4</li>
            </ul>
        </nav>
    </header>

    <main>
        {% block contents %}
        {% endblock %}
    </main>

    {% block binky %}
    {% endblock %}

    <footer>
        <p>저작권은 weniv에게 있습니다.</p>
    </footer>

    {% block mura %}
    {% endblock %}

    <script src="{% static 'js/custom.js' %}"></script>
</body>
</html>
```