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
