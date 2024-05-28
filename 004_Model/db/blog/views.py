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


def blog_detail(request, pk):
    blogs = Post.objects.get(pk=pk)
    context = {
        "object": blogs,
    }
    return render(request, "blog/blog_detail.html", context)


def blog_create(request, title):
    q = Post.objects.create(title=title, content="내용")
    q.save()
    return redirect("blog_list")


def blog_delete(request, pk):
    q = Post.objects.get(pk=pk)
    q.delete()
    return redirect("blog_list")
