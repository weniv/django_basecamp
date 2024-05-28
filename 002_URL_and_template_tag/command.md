# django
```python
# 폴더 기준으로 VSC 열기
#     * 이 작업은 리눅스 명령어 나중에 배울때 까지 똑같은 방식으로 진행하겠습니다.(내가 리눅스 명령어를 좀 안다! 하시는 분은 동일하게 안하셔도 됩니다.)
#     * File > Open Folder 누르시고 Django 작업할 폴더를 열어주세요.

# 터미널을 열어 작업
#     * 터미널(Ctrl + `), 단축키 대신 VSC에서 Terminal > new Terminal
# 이 명령어는 powershell 에서 치고 있습니다.
# 터미널 오른쪽 상단 +버튼 옆 아래 꺾쇠 버튼 눌러스 powershell을 열어주세요.

python --version
# 파이썬 버전 확인
mkdir mysite
# mysite라는 폴더 생성 => 마우스 클릭하셔서 생성하는 것과 차이 없습니다. 보통 mysite라는 이름 대신 프로젝트 이름을 넣습니다.
cd mysite
# 폴더 이동
python -m venv venv
# 가상 환경 설정(이어 설명합니다.) 하는 명령어 입니다.

# 가상환경 설정
#     * 가상환경은 선택이 아니라 필수 입니다.
#     * 가상환경을 왜 잡을까요? 관리, 이관, 업데이트 등에 중요한 거점이 됩니다.
#     * pip list를 쳐보세요. 많은 python 라이브러리가 보이죠? 여기서 소숫점 3번째 짜리까지 안맞으면 작동 안되는 경우도 허다합니다. => 가상 환경은 통째로 다 이동합니다.
#     * `python -m venv venv`뒤가 가상환경 이름입니다.

# 가상환경속으로 들어가기
.\venv\Scripts\activate # window
.\venv\Script\activate.bat # window
source ./venv/bin/activate # mac, linux

# window에서 오류가 뜰 경우
+ CategoryInfo          : 보안 오류: (:) [], PSSecurityException
+ FullyQualifiedErrorId : UnauthorizedAccess
# 아래 명령어를 입력해주세요. 
# 혹시 이 명령어가 제대로 작동하지 않으면 관리자 권한으로 powershell을 여시고 아래 명령어를 입력해주세요. (혹시 입력해야 하는 창이 있으면 '모두 예'인 'A'를 입력해주세요.)
# VSC를 관리자권한으로 여셔서 작업하셔도 동일한 효과가 납니다.
Set-ExecutionPolicy Unrestricted

# 앞에 (venv) ~~~ 이런 상태에서만 작업을 하셔야 합니다. 이 곳이 가상환경입니다. 쉽게 말해 컴퓨터 안에 컴퓨터입니다!
# pip list 쳐보면 설치된 것이 없는 깨끗한 백지상태입니다.

pip install django
# django를 최신 버전으로 설치합니다. 구버전 설치 하고 싶으시면 pip install django==4.0

django-admin startproject tutorialdjango .
# 띄고 점 꼭 하셔야 합니다!!!! 설치된 django로 초기세팅 하겠다라는 명령어 입니다. 암기하는 명령어 입니다. tutorialdjango는 이름입니다. 여러분 마음대로 지셔도 되는 이름입니다.

python manage.py migrate
# 이 명령어는 우리가 짠 python 코드를 DB에 반영하는 코드입니다. 다만! 실무에서는 이 migrate라는 명령어를 초기 세팅이 다~~~ 끝나고 합니다. 특히 User나 Admin 가입 소스코드를 만지면 먼저 migrate를 하면 error가 나는 경우가 있습니다. 처음에 migrate를 하면 기본적으로 django에서 세팅해주는 소스코드를 DB에 생성, 반영합니다.

python manage.py runserver
# 파이썬 서버를 구동합니다. 이 명령어가 실행되는 동안에만 서버가 실행됩니다. Ctrl 누르고 서버 URL을 클릭해보세요.


################################
# tutorialdjango > settings.py

ALLOWED_HOSTS = ["*"] # 우리 웹 서비스에 접속할 수 있는 사람을 모든사람으로 설정

################################

# URL에 따라 보통 1개의 앱을 만듭니다. 이름만 앱입니다. 실제로 다른 애플리케이션이라는 얘기가 아닙니다. 이유는 권한, 그 안에 들어가는 로직 등을 별도로 관리하기 위해서 입니다. 예를 들어 회원 게시판이 있고 자유 게시판이 있다면 회원 게시판에는 회원만 글을 써야 합니다. 이런 식으로 URL에 따른 권한과 로직을 별도로 관리하기 위해서 앱을 만들어 관리합니다. 

# https://www.studyin.co.kr/ => A
# https://www.studyin.co.kr/offline/ => B
# https://www.studyin.co.kr/offline/1 => B
# https://www.studyin.co.kr/offline/100 => B
# https://www.studyin.co.kr/online => C

################################

# Terminal에서 Ctrl + C 눌러서 서버를 종료시켜 주세요! => 우리 서비스는 작동되지 않습니다!
# 아래 명령어는 main이라는 앱을 하나 만들겠다는 것입니다. 기획이 되어 있는 상태에서는 이 명령어를 수십번 쳐서 세팅하고 들어갑니다.
python manage.py startapp main

################################
# tutorialdjango > settings.py

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main", # 보통은 마지막에 넣는데 맨 위에 넣으시는 분도 있으십니다.
]
################################
# URL 구조 작성(기획 단계), 문서입니다. 
# 다른 곳에 작성하는 것이 아닙니다.

www.hojun.com/admin
www.hojun.com/   
www.hojun.com/blog   # blog_list (게시물 목록 보는 URL)
www.hojun.com/blog/1 # blog_details (게시물 상세 페이지)
www.hojun.com/blog/2 # blog_details (게시물 상세 페이지)
www.hojun.com/blog/3 # blog_details (게시물 상세 페이지)
www.hojun.com/accounts/hojun # accounts_details (유저 상세 페이지)
www.hojun.com/accounts/junho

################################
# URL 설계한 것을 반영하는 곳!
# tutorialdjango > urls.py에 반영!

from django.contrib import admin
from django.urls import path
from main.views import index, blog_list, blog_details, accounts_details

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("blog/", blog_list),
    path("blog/<int:pk>/", blog_details),
    path("accounts/<str:username>/", accounts_details),
]

################################
# 설계한 URL에 접속했을 때 실제 보게될 텍스트는 views.py에서!
# HttpResponse는 주로 테스트 용도로 사용합니다.
# 기본 세팅 코드
# main > views.py

from django.shortcuts import render
from django.http import HttpResponse

blog_list_db = [
    {
        "id": 1,
        "title": "장고는 너무 재미있어!!!",
        "content": "This is the content of blog 1",
        "author": "Author 1",
    },
    {
        "id": 2,
        "title": "파이썬도 너무 재미있어!!!!",
        "content": "This is the content of blog 2",
        "author": "Author 2",
    },
    {
        "id": 3,
        "title": "자바스크립트는 별로였어!!!",
        "content": "This is the content of blog 3",
        "author": "Author 3",
    },
]

user_list_db = [
    {
        "id": 1,
        "username": "hojun",
        "email": "hojun@gmail.com",
        "password": "1234",
    },
    {
        "id": 2,
        "username": "jihun",
        "email": "jihun@gmail.com",
        "password": "1234",
    },
    {
        "id": 3,
        "username": "junho",
        "email": "junho@gmail.com",
        "password": "1234",
    },
]

def index(request):
    return HttpResponse("index")


def blog_list(request):
    blog_list_html = ""
    for blog in blog_list_db:
        blog_list_html += f'<li><a href="/blog/{blog['id']}">{blog['title']}</a></li>'
    return HttpResponse(f"""
    <h1>Blog List</h1>
    <ul>
        {blog_list_html}
    </ul>
""")

# s = f'hello world' # 개행이 안되고
# ss = f'''hello world''' #개행이 됩니다.

def blog_details(request, pk):
    blog = blog_list_db[pk-1]
    return HttpResponse(f"""
    <h1>{blog['title']}</h1>
    <p>{blog['content']}</p>
    <p>{blog['author']}</p>
""")

def accounts_details(request, username):
    # all(filter(user_list_db, lambda x: x['username'] == user))
    finduser = None
    for user in user_list_db:
        if user['username'] == username:
            finduser = user
    if finduser is None:
        return HttpResponse("User not found")
    return HttpResponse(f"""
    <h1>{finduser['username']}</h1>
    <p>{finduser['email']}</p>
""")


################################

python manage.py runserver

# 모든 페이지 정상작동 확인 + 이상한 URL 입력시 애러 확인
# settings.py에 DEBUG도 False로 해봐서 출력되는 화면도 확인

################################
# views.py
from django.shortcuts import render
from django.http import HttpResponse

blog_list_db = [
    {
        "id": 1,
        "title": "장고는 너무 재미있어!!!",
        "content": "This is the content of blog 1",
        "author": "Author 1",
    },
    {
        "id": 2,
        "title": "파이썬도 너무 재미있어!!!!",
        "content": "This is the content of blog 2",
        "author": "Author 2",
    },
    {
        "id": 3,
        "title": "자바스크립트는 별로였어!!!",
        "content": "This is the content of blog 3",
        "author": "Author 3",
    },
]

user_list_db = [
    {
        "id": 1,
        "username": "hojun",
        "email": "hojun@gmail.com",
        "password": "1234",
    },
    {
        "id": 2,
        "username": "jihun",
        "email": "jihun@gmail.com",
        "password": "1234",
    },
    {
        "id": 3,
        "username": "junho",
        "email": "junho@gmail.com",
        "password": "1234",
    },
]


def index(request):
    return HttpResponse("index")


def blog_list(request):
    context = {"blog_list": blog_list_db, "hello": [10, 20, 30]}
    return render(request, "main/blog_list.html", context)


def blog_details(request, pk):
    blog = blog_list_db[pk - 1]
    context = {"blog": blog}
    return render(request, "main/blog_details.html", context)


def accounts_details(request, username):
    finduser = None
    for user in user_list_db:
        if user["username"] == username:
            finduser = user
            break
    if finduser is None:
        return HttpResponse("User not found")
    context = {"user": finduser}
    return render(request, "main/accounts_details.html", context)


################################

main > templates > main > blog_list.html
main > templates > main > blog_details.html
main > templates > main > accounts_details.html


################################
# blog_list.html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>blog_list</title>
</head>
<body>
    <h1>blog_list 페이지 입니다.</h1>
    <ul>
        <li><a href="/blog/1">게시물1</a></li>
        <li><a href="/blog/2">게시물2</a></li>
        <li><a href="/blog/3">게시물3</a></li>
    </ul>
</body>
</html>

################################

https://docs.djangoproject.com/en/5.0/ref/templates/builtins/

################################
# 위에 코드를 업데이트!!
# 중괄호 2개는 변수!! {{value}}, dict자료형도 .으로 접근합니다. 대괄호로 접근하지 않아요!
# 중괄호+%면 문법!! {% if value %}
# 다른 프레임웤에서도 이런 패턴이 쓰입니다! 예를 들어 Node + 넌적스!

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>blog_list</title>
</head>
<body>
    <h1>blog_list 페이지 입니다.</h1>
    {# 주석 입니다! #}

    {# {% '파이썬 문법 사용!' %} #}
    {# {{ '파이썬 변수 사용!' }} #}

    {# 다만 이런 식으로 실무에서 사용하지 않고, {% url 함수명 아규먼트 %} 형태로 사용합니다. #}
    {# 지금은 쉽게 가르쳐 드리기 위해 이 방식을 사용하겠습니다. #}
    <ul>
        {% for blog in blog_list %}
        <li><a href="/blog/{{blog.id}}">{{blog.title}}</a></li>
        {% endfor %}
    </ul>

    {% for i in hello %}
    <p>{{i}}</p>
    {% endfor %}
</body>
</html>
################################
# blog_details.html

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>blog_details</title>
</head>
<body>
    <h1>blog_details</h1>
    <h2>{{ blog.title }}</h2>
    <p>{{ blog.author }}</p>
    <p>{{ blog.content }}</p>
</body>
</html>

################################
# account_details.html

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>userinfo</title>
</head>
<body>
    <h1>userinfo 페이지</h1>
    <p>{{user.username}}</p>
    <p>{{user.email}}</p>
</body>
</html>


################################
# main > views.py

def index(request):
    mock_data = [
        {
            "_id": "40ed5f5d-1479-4cff-A8db-50cd925358d1",
            "index": "1",
            "name": "탁민재",
            "email": "user-okckofi@molestie.net",
            "phone": "010-3275-8617",
            "country": "감비아",
            "address": "용두동 86-3",
            "job": "메이크업아티스트",
            "age": "29",
        },
        {
            "_id": "c802171f-5661-43d8-C146-29d60cb097ab",
            "index": "2",
            "name": "류정민",
            "email": "user-98i0esc@Ornare.com",
            "phone": "010-7740-8505",
            "country": "칠레",
            "address": "성동로 89-4",
            "job": "메이크업아티스트",
            "age": "61",
        },
        {
            "_id": "8f605ef8-98fe-43ab-A234-e7882745254e",
            "index": "3",
            "name": "대재은",
            "email": "user-rj5sqf1@finibus.com",
            "phone": "010-2930-6436",
            "country": "가나",
            "address": "공덕로 9-3",
            "job": "은행출납사무원",
            "age": "30",
        },
        {
            "_id": "63d288ca-81ee-4689-Af9d-e3d20e8a8b2e",
            "index": "4",
            "name": "등예건",
            "email": "user-0crjbbk@montes.io",
            "phone": "010-6523-7033",
            "country": "세인트루시아",
            "address": "행운동 87-5",
            "job": "국제회의전문가",
            "age": "57",
        },
        {
            "_id": "acb7bc4b-b99e-4cff-Cd1f-ce14b4572773",
            "index": "5",
            "name": "담누리",
            "email": "user-ay8ycrv@Nam.co.kr",
            "phone": "010-6276-4787",
            "country": "수리남",
            "address": "잠원로 25-9",
            "job": "영화감독",
            "age": "47",
        },
        {
            "_id": "488f4267-3f06-432f-B3bd-7f9f5f793a5e",
            "index": "6",
            "name": "동진성",
            "email": "user-k285yz7@sagittis.biz",
            "phone": "010-4826-4141",
            "country": "그레나다",
            "address": "서소문로 76-7",
            "job": "심리학연구원",
            "age": "53",
        },
        {
            "_id": "ba473db8-1d12-4241-Ce5c-66348452eec9",
            "index": "7",
            "name": "근승리",
            "email": "user-a1txn3z@tempus.io",
            "phone": "010-2148-4195",
            "country": "앤티가 바부다",
            "address": "대림로 35-6",
            "job": "로봇연구원",
            "age": "20",
            "contents": "각급 선거관리위원회의 조직·직무범위 기타 필요한 사항은 법률로 정한다. 국가는 법률이 정하는 바에 의하여 재외국민을 보호할 의무를 진다. 국회의원의 수는 법률로 정하되, 200인 이상으로 한다.\n\n\n대통령이 임시회의 집회를 요구할 때에는 기간과 집회요구의 이유를 명시하여야 한다. 이 헌법공포 당시의 국회의원의 임기는 제1항에 의한 국회의 최초의 집회일 전일까지로 한다.",
        },
    ]
    context = {"mock_data": mock_data}
    return render(request, "main/index.html", context)

################################
# main > index.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {% for i in mock_data %}
    <section>
        <h2>{{i.name}}</h2>
        <p>{{i.email}}</p>
        <!-- 개행이 안되어 있는 것을 확인! -->
        <p>{{ i.contents }}</p>
        
        <!-- 개행이 된 것을 확인! -->
        <p>{{ i.contents |linebreaks }}</p> 

        <hr>

        <p>{{ i.contents|truncatewords:5 }}</p>
        <p>{{ i.contents|length }}
        <p>{{ i.contents|slice:":10" }}

        <hr>

        <p>{{ forloop.counter }}번째 반복문</p>
        <p>{{ forloop.counter0 }}</p>
        <p>{{ forloop.revcounter }}</p>

    </section>
    {% endfor %}

    {% for i in mock_data %}
        <h2>{{i.name}}</h2>
        <p>{{ forloop.counter }}</p>
        <p>{{ i.age }}</p>
        {% if i.age|add:"0" >= 20 and i.age|add:"0" <= 35 %}
            <p>청년입니다.</p>
        {% elif i.age|add:"0" >= 35 and i.age|add:"0" <= 60 %}
            <p>중년입니다.</p>
        {% else %}
            <p>장년입니다.</p>
        {% endif %}
    {% endfor %}

    {% with value='hello world' %}
        <p>{{value}}</p>
        <p>이 안에서 for나 if를 사용할 수 있습니다.</p>
    {% endwith %}

    {% lorem 3 p %}

    <p>It is {% now "jS F Y H:i" %}</p>
    <p>It is {% now "Y/M/D" %}</p>
</body>
</html>

```