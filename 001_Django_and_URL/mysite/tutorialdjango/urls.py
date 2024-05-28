from django.contrib import admin
from django.urls import path
from main.views import index, a, b

urlpatterns = [
    # path('원하는URL/', 함수명),
    path("admin/", admin.site.urls),
    path("", index),
    path("a/", a),
    path("b/", b),
]
